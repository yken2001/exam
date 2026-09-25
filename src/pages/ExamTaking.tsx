import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { db } from '../db';
import { QUESTION_BY_ID } from '../data/sampleQuestions';
import { pageSizeForWidth, useWindowWidth } from '../hooks/useWindowWidth';
import type { AttemptRecord, ExamPaper, Question } from '../types';
import { clusterByGroup } from '../utils/clusterByGroup';
import { newId } from '../utils/newId';
import ExamImage from '../components/ExamImage';
import AudioPlayer from '../components/AudioPlayer';

/** Packs whole clusters (shared-passage groups stay intact) onto pages of
 * roughly `pageSize` questions each. A cluster bigger than pageSize just
 * gets its own oversized page rather than being split. */
function chunkKeepingGroups(qs: Question[], pageSize: number): Question[][] {
  const clusters = clusterByGroup(qs);
  const pages: Question[][] = [];
  let current: Question[] = [];
  for (const cluster of clusters) {
    if (current.length > 0 && current.length + cluster.length > pageSize) {
      pages.push(current);
      current = [];
    }
    current.push(...cluster);
  }
  if (current.length > 0) pages.push(current);
  return pages;
}

function formatTime(totalSec: number): string {
  const m = Math.floor(totalSec / 60).toString().padStart(2, '0');
  const s = Math.floor(totalSec % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

export default function ExamTaking() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const width = useWindowWidth();
  const pageSize = pageSizeForWidth(width);

  const [paper, setPaper] = useState<ExamPaper | null>(null);
  const [attemptId] = useState(() => newId());
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [pageIndex, setPageIndex] = useState(0);
  const [remaining, setRemaining] = useState<number | null>(null);
  const [finished, setFinished] = useState(false);
  const [confirmDialog, setConfirmDialog] = useState<{ message: string; onConfirm: () => void } | null>(
    null
  );

  useEffect(() => {
    if (!examId) return;
    db.examPapers.get(examId).then((p) => {
      if (!p) return;
      setPaper(p);
      setRemaining(p.timeBudgetSec);
      const attempt: AttemptRecord = {
        id: attemptId,
        examPaperId: p.id,
        startedAt: Date.now(),
        answers: [],
      };
      db.attempts.add(attempt);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [examId]);

  const questions: Question[] = useMemo(() => {
    if (!paper) return [];
    return paper.questionIds.map((id) => QUESTION_BY_ID.get(id)!).filter(Boolean);
  }, [paper]);

  function handleFinishClick() {
    const unanswered = questions.filter((q) => !answers[q.id]).length;
    const message =
      unanswered === 0
        ? '全部都已作答，確定要交卷嗎？'
        : `還有 ${unanswered} 題沒有作答，確定要交卷嗎？`;
    setConfirmDialog({ message, onConfirm: handleFinish });
  }

  async function handleFinish() {
    setFinished((already) => {
      if (already) return already;
      const answerList = questions.map((q) => ({ questionId: q.id, selected: answers[q.id] }));
      db.attempts.update(attemptId, { finishedAt: Date.now(), answers: answerList }).then(() => {
        navigate(`/review/${attemptId}`);
      });
      return true;
    });
  }

  // Guard against losing in-progress answers to an accidental tab close/
  // refresh (native browser prompt -- browsers ignore any custom message
  // here and always show their own generic text, which is expected) or an
  // in-app back navigation (our own modal below, since HashRouter has no
  // built-in navigation blocker and native confirm() is unreliable in some
  // embedded/automated browser contexts, which always resolve it to
  // "cancel").
  useEffect(() => {
    if (finished) return;
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = '';
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [finished]);

  useEffect(() => {
    if (finished) return;
    window.history.pushState(null, '', window.location.href);
    const handlePopState = () => {
      // Immediately cancel the browser's default back navigation by
      // re-pushing our marker state, then ask via our own modal; only a
      // confirmed "leave" actually pops back out.
      window.history.pushState(null, '', window.location.href);
      setConfirmDialog({
        message: '作答尚未完成，離開將遺失作答記錄，確定要離開嗎？',
        onConfirm: () => {
          window.removeEventListener('popstate', handlePopState);
          window.history.back();
        },
      });
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [finished]);

  useEffect(() => {
    if (remaining === null || finished) return;
    if (remaining <= 0) {
      handleFinish();
      return;
    }
    const t = setTimeout(() => setRemaining((r) => (r !== null ? r - 1 : r)), 1000);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [remaining, finished]);

  const pages = useMemo(() => chunkKeepingGroups(questions, pageSize), [questions, pageSize]);
  const currentPage = pages[pageIndex] ?? [];

  const pageIndexOfQuestion = useMemo(() => {
    const m = new Map<string, number>();
    pages.forEach((page, pi) => page.forEach((q) => m.set(q.id, pi)));
    return m;
  }, [pages]);

  function selectAnswer(questionId: string, option: string) {
    setAnswers((prev) => ({ ...prev, [questionId]: option }));
  }

  function jumpToQuestion(questionId: string) {
    const pi = pageIndexOfQuestion.get(questionId);
    if (pi !== undefined) setPageIndex(pi);
  }

  if (!paper) return <div className="empty-state">載入中…</div>;

  const low = remaining !== null && remaining < 60;

  return (
    <div>
      <div className="topbar">
        <span>科目：{paper.subjects.join('、')}</span>
        <span className={`timer ${low ? 'low' : ''}`}>
          <span aria-hidden="true">⏱</span> {remaining !== null ? formatTime(remaining) : '--:--'}
        </span>
      </div>

      <div className="nav-strip">
        <button className="nav-arrow" onClick={() => setPageIndex((p) => Math.max(0, p - 1))}>
          ‹
        </button>
        {questions.map((q, i) => (
          <span
            key={q.id}
            className={`q-num ${answers[q.id] ? 'done' : ''} ${
              pageIndexOfQuestion.get(q.id) === pageIndex ? 'current' : ''
            } ${q.groupId ? 'grouped' : ''}`}
            onClick={() => jumpToQuestion(q.id)}
          >
            {i + 1}
          </span>
        ))}
        <button
          className="nav-arrow"
          onClick={() => setPageIndex((p) => Math.min(pages.length - 1, p + 1))}
        >
          ›
        </button>
      </div>

      <div className="q-stack">
        {clusterByGroup(currentPage).map((cluster) => {
          const first = cluster[0];
          const isGroup = cluster.length > 1;
          const firstIndex = questions.indexOf(first);
          const lastIndex = questions.indexOf(cluster[cluster.length - 1]);
          return (
            <div className="q-card" key={first.id}>
              <div className="q-card-title">
                {isGroup ? `第 ${firstIndex + 1}~${lastIndex + 1} 題` : `第 ${firstIndex + 1} 題`}
                {first.groupId && <span className="q-tag">題組</span>}
                {first.audioPath && <span className="q-tag">英聽</span>}
              </div>
              {first.audioPath && <AudioPlayer key={first.id} src={first.audioPath} />}
              <ExamImage
                className="q-image"
                src={first.imagePath}
                alt={`${first.subject} ${first.year} 第${first.qNo}題`}
              />
              {cluster.map((q) => {
                const qGlobalIndex = questions.indexOf(q);
                return (
                  <div className="q-subblock" key={q.id}>
                    {isGroup && <div className="q-sub-label">第 {qGlobalIndex + 1} 題</div>}
                    <div className="q-options">
                      {Array.from({ length: q.optionCount }, (_, i) => String.fromCharCode(65 + i)).map(
                        (opt) => (
                          <span
                            key={opt}
                            className={`q-option ${answers[q.id] === opt ? 'selected' : ''}`}
                            onClick={() => selectAnswer(q.id, opt)}
                          >
                            {opt}
                          </span>
                        )
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>

      <button className="primary" onClick={handleFinishClick}>
        交卷
      </button>

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
