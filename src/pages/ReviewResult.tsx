import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { db } from '../db';
import { QUESTION_BY_ID } from '../data/sampleQuestions';
import type { AttemptRecord, ExamPaper, Question } from '../types';
import { clusterByGroup, inUnitOrder } from '../utils/clusterByGroup';
import ExamImage from '../components/ExamImage';
import AudioPlayer from '../components/AudioPlayer';
import { gradeAttempt, levelText } from '../engine/grade';
import { Passage, TextStem } from '../components/TextQuestion';
import { yearLabel } from '../utils/yearLabel';

/** Splits a cluster into runs of consecutive questions sharing one
 * explanation image: each question gets its own run when every item has its
 * own 解析, while a 題組 whose 解析卷 explains the whole group in one block
 * becomes a single run (all items' answers, then that one explanation). */
function runsByExplanation(cluster: Question[]): Question[][] {
  const runs: Question[][] = [];
  for (const q of cluster) {
    const last = runs[runs.length - 1];
    if (last && q.explanationImagePath && last[0].explanationImagePath === q.explanationImagePath) {
      last.push(q);
    } else {
      runs.push([q]);
    }
  }
  return runs;
}

export default function ReviewResult() {
  const { attemptId } = useParams();
  const [attempt, setAttempt] = useState<AttemptRecord | null>(null);
  const [paper, setPaper] = useState<ExamPaper | null>(null);

  useEffect(() => {
    if (!attemptId) return;
    db.attempts.get(attemptId).then(async (a) => {
      if (!a) return;
      setAttempt(a);
      const p = await db.examPapers.get(a.examPaperId);
      setPaper(p ?? null);
    });
  }, [attemptId]);

  const questions: Question[] = useMemo(() => {
    if (!paper) return [];
    return inUnitOrder(paper.questionIds.map((id) => QUESTION_BY_ID.get(id)!).filter(Boolean));
  }, [paper]);

  const answerMap = useMemo(() => {
    const m: Record<string, string | undefined> = {};
    attempt?.answers.forEach((a) => (m[a.questionId] = a.selected));
    return m;
  }, [attempt]);

  if (!attempt || !paper) return <div className="empty-state">載入中…</div>;

  const correctCount = questions.filter((q) => answerMap[q.id] === q.correctAnswer).length;
  const grades = gradeAttempt(questions, answerMap);
  const total = questions.length;
  const rate = total > 0 ? Math.round((correctCount / total) * 100) : 0;
  const durationMin = attempt.finishedAt
    ? Math.round((attempt.finishedAt - attempt.startedAt) / 60000)
    : null;

  return (
    <div>
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="field-label">
          {paper.subjects.join('、')} · {paper.years.map(yearLabel).join('、')} 年度
        </div>
        <div className="estimate-box" style={{ margin: 0 }}>
          <div className="label">正確率</div>
          <div className="value">
            {correctCount}/{total} · {rate}%
          </div>
        </div>
        {durationMin !== null && (
          <div style={{ marginTop: 8, fontSize: 13, color: 'var(--text-secondary)' }}>
            作答時間：約 {durationMin} 分鐘
          </div>
        )}
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <div className="field-label">評級（依心測中心各年等級對照表）</div>
        <table className="grade-table">
          <tbody>
            {grades.map((g) => (
              <tr key={g.name}>
                <th>{g.name}</th>
                <td>
                  {g.correct}/{g.total}
                </td>
                <td className={`grade-level ${g.level ? 'lv-' + g.level[0] : ''}`}>
                  {g.level ? `${g.kind === 'estimate' ? '約 ' : ''}${levelText(g.level)}` : '—'}
                </td>
                <td className="grade-note">
                  {g.kind === 'official' ? '官方等級' : g.kind === 'estimate' ? '估計' : ''}
                  {g.note ? `${g.kind === 'none' ? '' : '・'}${g.note}` : ''}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="q-stack">
        {clusterByGroup(questions).map((cluster) => {
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
                {first.text && <span className="q-tag ai">AI 題</span>}
              </div>
              {first.audioPath && <AudioPlayer key={first.id} src={first.audioPath} />}
              {first.imagePath && (
                <ExamImage
                  className="q-image"
                  src={first.imagePath}
                  alt={`${first.subject} ${first.year} 第${first.qNo}題`}
                />
              )}
              {first.text?.passage && (
                <>
                  <Passage
                    text={first.text.passage}
                    numberOf={(n) => {
                      const i = cluster.findIndex((c) => c.qNo === n);
                      return i < 0 ? undefined : questions.indexOf(cluster[i]) + 1;
                    }}
                  />
                  {first.text.passageTranslation && (
                    <details className="passage-translation">
                      <summary>文章翻譯</summary>
                      <div>{first.text.passageTranslation}</div>
                    </details>
                  )}
                </>
              )}
              {runsByExplanation(cluster).map((run) => (
                <div key={run[0].id}>
                  {run.map((q) => {
                    const qGlobalIndex = questions.indexOf(q);
                    const selected = answerMap[q.id];
                    const isCorrect = selected === q.correctAnswer;
                    return (
                      <div className="q-subblock" key={q.id}>
                        {q.text && <TextStem q={q} number={qGlobalIndex + 1} />}
                        <div className="q-sub-label">
                          {isGroup && !q.text ? `第 ${qGlobalIndex + 1} 題　` : ''}
                          <span style={{ color: isCorrect ? '#3b6d11' : '#a32d2d' }}>
                            {selected ? (isCorrect ? '答對' : '答錯') : '未作答'}
                          </span>
                        </div>
                        <div className="q-options">
                          {Array.from({ length: q.optionCount }, (_, i) => String.fromCharCode(65 + i)).map(
                            (opt) => {
                              let cls = 'q-option';
                              if (opt === q.correctAnswer) cls += ' correct';
                              else if (opt === selected) cls += ' incorrect';
                              return (
                                <span key={opt} className={cls}>
                                  {opt}
                                </span>
                              );
                            }
                          )}
                        </div>
                      </div>
                    );
                  })}
                  {run[0].explanationImagePath ? (
                    <ExamImage
                      className="q-image explanation-image"
                      src={run[0].explanationImagePath}
                      alt={`第${questions.indexOf(run[0]) + 1}題詳解`}
                    />
                  ) : (
                    run[0].explanation && <div className="explanation text-explanation">{run[0].explanation}</div>
                  )}
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
}
