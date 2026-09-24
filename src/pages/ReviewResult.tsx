import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { db } from '../db';
import { QUESTION_BY_ID } from '../data/sampleQuestions';
import type { AttemptRecord, ExamPaper, Question } from '../types';
import { clusterByGroup } from '../utils/clusterByGroup';
import ExamImage from '../components/ExamImage';

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
    return paper.questionIds.map((id) => QUESTION_BY_ID.get(id)!).filter(Boolean);
  }, [paper]);

  const answerMap = useMemo(() => {
    const m: Record<string, string | undefined> = {};
    attempt?.answers.forEach((a) => (m[a.questionId] = a.selected));
    return m;
  }, [attempt]);

  if (!attempt || !paper) return <div className="empty-state">載入中…</div>;

  const correctCount = questions.filter((q) => answerMap[q.id] === q.correctAnswer).length;
  const total = questions.length;
  const rate = total > 0 ? Math.round((correctCount / total) * 100) : 0;
  const durationMin = attempt.finishedAt
    ? Math.round((attempt.finishedAt - attempt.startedAt) / 60000)
    : null;

  return (
    <div>
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="field-label">
          {paper.subjects.join('、')} · {paper.years.join('、')} 年度
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
              </div>
              {first.imagePath.startsWith('placeholder://') ? (
                <div className="q-body">
                  題目內容（{first.subject} {first.year} 第{first.qNo}題，截圖區）
                </div>
              ) : (
                <ExamImage
                  className="q-image"
                  src={first.imagePath}
                  alt={`${first.subject} ${first.year} 第${first.qNo}題`}
                />
              )}
              {cluster.map((q) => {
                const qGlobalIndex = questions.indexOf(q);
                const selected = answerMap[q.id];
                const isCorrect = selected === q.correctAnswer;
                return (
                  <div className="q-subblock" key={q.id}>
                    <div className="q-sub-label">
                      {isGroup ? `第 ${qGlobalIndex + 1} 題　` : ''}
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
              {first.explanationImagePath ? (
                <ExamImage
                  className="q-image explanation-image"
                  src={first.explanationImagePath}
                  alt={`第${firstIndex + 1}題詳解`}
                />
              ) : (
                first.explanation && <div className="explanation">{first.explanation}</div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
