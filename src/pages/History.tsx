import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { db } from '../db';
import { QUESTION_BY_ID } from '../data/sampleQuestions';
import type { AttemptRecord, ExamPaper } from '../types';

interface Row {
  attempt: AttemptRecord;
  paper: ExamPaper;
  correctCount: number;
  total: number;
}

export default function History() {
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    (async () => {
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
        built.push({ attempt, paper, correctCount, total: paper.questionIds.length });
      }
      setRows(built);
    })();
  }, []);

  if (rows.length === 0) {
    return <div className="empty-state">還沒有作答紀錄，先去「建立考卷」開始一次測驗吧。</div>;
  }

  return (
    <table className="history-table">
      <thead>
        <tr>
          <th>#</th>
          <th>科目/年度</th>
          <th>開始時間</th>
          <th>時長</th>
          <th>正確率</th>
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
                {r.paper.subjects.join('+')} {r.paper.years.join('、')}
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
              <td>
                <Link to={`/review/${r.attempt.id}`}>
                  <button>查看結果</button>
                </Link>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
