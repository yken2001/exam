import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { db } from '../db';
import { QUESTION_BY_ID, SAMPLE_QUESTIONS } from '../data/sampleQuestions';
import type { AttemptRecord, ExamPaper } from '../types';
import { backupFile, buildBackup, canShareFile, downloadFile, importBackup } from '../utils/backup';
import { computePoints, type AttemptPoints, type PointsSummary } from '../engine/points';
import { gradeAttempt } from '../engine/grade';
import PointsPanel from '../components/PointsPanel';
import { yearLabel } from '../utils/yearLabel';

interface Row {
  attempt: AttemptRecord;
  paper: ExamPaper;
  correctCount: number;
  total: number;
  /** e.g. "國文 B+・英文 約A" -- subjects that got a level */
  grades: string;
}

export default function History() {
  const [rows, setRows] = useState<Row[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [summary, setSummary] = useState<PointsSummary | null>(null);
  const [pointsDetail, setPointsDetail] = useState<AttemptPoints | null>(null);
  const [confirmDialog, setConfirmDialog] = useState<{ message: string; onConfirm: () => void } | null>(
    null
  );
  const [notice, setNotice] = useState<string | null>(null);
  const [shareable, setShareable] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  const load = async () => {
    const attempts = await db.attempts.orderBy('startedAt').reverse().toArray();
    const finished = attempts.filter((a) => a.finishedAt);
    const built: Row[] = [];
    for (const attempt of finished) {
      const paper = await db.examPapers.get(attempt.examPaperId);
      if (!paper) continue;
      const correctCount = attempt.answers.filter((a) => {
        const q = QUESTION_BY_ID.get(a.questionId);
        return q && a.selected === q.correctAnswer;
      }).length;
      const qs = paper.questionIds.map((id) => QUESTION_BY_ID.get(id)).filter((q) => q !== undefined);
      const answers = Object.fromEntries(attempt.answers.map((a) => [a.questionId, a.selected]));
      const grades = gradeAttempt(qs, answers)
        .filter((g) => g.level)
        .map((g) => `${g.name} ${g.kind === 'estimate' ? '約' : ''}${g.level}`)
        .join('・');
      built.push({ attempt, paper, correctCount, total: paper.questionIds.length, grades });
    }
    setRows(built);
    setSummary(computePoints(finished, QUESTION_BY_ID));
    setLoaded(true);
  };

  useEffect(() => {
    load();
    // probe once whether this device's share sheet takes files (Android does)
    buildBackup().then((b) => setShareable(canShareFile(backupFile(b))));
  }, []);

  const exportRecords = async () => {
    downloadFile(backupFile(await buildBackup()));
  };

  const shareRecords = async () => {
    const file = backupFile(await buildBackup());
    try {
      await navigator.share({ files: [file], title: file.name, text: '會考練習紀錄' });
    } catch (e) {
      if ((e as Error).name !== 'AbortError') downloadFile(file);    // cancelled: do nothing
    }
  };

  const importRecords = async (file: File) => {
    try {
      const r = await importBackup(await file.text(), file.name);
      await load();
      setNotice(
        `已匯入 ${r.added} 筆作答紀錄` +
          (r.alreadyHad ? `（另有 ${r.alreadyHad} 筆先前已匯入過，略過）` : '') +
          `。\n紀錄檔匯出時間：${new Date(r.exportedAt).toLocaleString()}，App 版本：${r.appVersion}` +
          (r.unknownQuestions ? `\n注意：有 ${r.unknownQuestions} 題不在目前的題庫中，這些題不會計分。` : '')
      );
    } catch (e) {
      setNotice((e as Error).message);
    }
  };

  const deleteOne = (attemptId: string, examPaperId: string) => {
    setConfirmDialog({
      message: '確定要刪除這筆作答紀錄嗎？此動作無法復原。',
      onConfirm: async () => {
        await db.attempts.delete(attemptId);
        await db.examPapers.delete(examPaperId);
        load();
      },
    });
  };

  const deleteAll = () => {
    setConfirmDialog({
      message: `確定要清除全部 ${rows.length} 筆作答紀錄嗎？此動作無法復原。`,
      onConfirm: async () => {
        await db.attempts.bulkDelete(rows.map((r) => r.attempt.id));
        await db.examPapers.bulkDelete(rows.map((r) => r.paper.id));
        load();
      },
    });
  };

  return (
    <div>
      <div className="history-toolbar">
        <button onClick={exportRecords}>匯出紀錄</button>
        {shareable && <button onClick={shareRecords}>分享（Email／LINE）</button>}
        <button onClick={() => fileInput.current?.click()}>匯入紀錄</button>
        <input
          ref={fileInput}
          type="file"
          accept=".json,application/json"
          style={{ display: 'none' }}
          onChange={(e) => {
            const f = e.target.files?.[0];
            e.target.value = '';                      // allow picking the same file again
            if (f) importRecords(f);
          }}
        />
        {rows.length > 0 && (
          <button className="toolbar-right" onClick={deleteAll}>
            清除全部紀錄
          </button>
        )}
      </div>

      {summary && rows.length > 0 && <PointsPanel summary={summary} totalQuestions={SAMPLE_QUESTIONS.length} />}

      {!loaded ? (
        <div className="empty-state">載入中…</div>
      ) : rows.length === 0 ? (
        <div className="empty-state">還沒有作答紀錄，先去「建立考卷」開始一次測驗吧。</div>
      ) : (
        <table className="history-table">
          <thead>
            <tr>
              <th>#</th>
              <th>科目/年度</th>
              <th>開始時間</th>
              <th>時長</th>
              <th>正確率</th>
              <th>評級</th>
              <th>積分</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => {
              const started = new Date(r.attempt.startedAt);
              const durationMin = r.attempt.finishedAt
                ? Math.round((r.attempt.finishedAt - r.attempt.startedAt) / 60000)
                : 0;
              const rate = r.total > 0 ? Math.round((r.correctCount / r.total) * 100) : 0;
              return (
                <tr key={r.attempt.id}>
                  <td>{rows.length - i}</td>
                  <td>
                    {r.paper.subjects.join('+')} {r.paper.years.map(yearLabel).join('、')}
                    {r.attempt.importedFrom && (
                      <span className="q-tag" title={r.attempt.importedFrom}>
                        匯入
                      </span>
                    )}
                  </td>
                  <td>
                    {started.toLocaleDateString()}{' '}
                    {started.getHours().toString().padStart(2, '0')}:
                    {started.getMinutes().toString().padStart(2, '0')}
                  </td>
                  <td>{durationMin} 分</td>
                  <td>
                    {r.correctCount}/{r.total} · {rate}%
                  </td>
                  <td className="grade-note">{r.grades || '—'}</td>
                  <td>
                    {(() => {
                      const p = summary?.perAttempt.get(r.attempt.id);
                      return p ? (
                        <button className="points-chip" onClick={() => setPointsDetail(p)}>
                          +{p.total}
                        </button>
                      ) : null;
                    })()}
                  </td>
                  <td>
                    <Link to={`/review/${r.attempt.id}`}>
                      <button>查看結果</button>
                    </Link>
                  </td>
                  <td>
                    <button onClick={() => deleteOne(r.attempt.id, r.paper.id)}>刪除</button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      {pointsDetail && (
        <div className="modal-overlay" onClick={() => setPointsDetail(null)}>
          <div className="modal-box" onClick={(e) => e.stopPropagation()}>
            <p className="modal-message">這次得到 {pointsDetail.total} 積分</p>
            <table className="confirm-table">
              <tbody>
                {pointsDetail.lines.map((l) => (
                  <tr key={l.label}>
                    <th>{l.label}</th>
                    <td>+{l.points}</td>
                  </tr>
                ))}
                {pointsDetail.lines.length === 0 && (
                  <tr>
                    <td>這份卷沒有新題、訂正或精熟，所以沒有積分。</td>
                  </tr>
                )}
              </tbody>
            </table>
            <div className="modal-actions">
              <button className="primary" onClick={() => setPointsDetail(null)}>
                確定
              </button>
            </div>
          </div>
        </div>
      )}

      {notice && (
        <div className="modal-overlay" onClick={() => setNotice(null)}>
          <div className="modal-box" onClick={(e) => e.stopPropagation()}>
            <p className="modal-message" style={{ whiteSpace: 'pre-line' }}>
              {notice}
            </p>
            <div className="modal-actions">
              <button className="primary" onClick={() => setNotice(null)}>
                確定
              </button>
            </div>
          </div>
        </div>
      )}

      {confirmDialog && (
        <div className="modal-overlay" onClick={() => setConfirmDialog(null)}>
          <div className="modal-box" onClick={(e) => e.stopPropagation()}>
            <p className="modal-message">{confirmDialog.message}</p>
            <div className="modal-actions">
              <button onClick={() => setConfirmDialog(null)}>取消</button>
              <button
                className="primary"
                onClick={() => {
                  const { onConfirm } = confirmDialog;
                  setConfirmDialog(null);
                  onConfirm();
                }}
              >
                確定
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
