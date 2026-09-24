import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AVAILABLE_YEARS, SAMPLE_QUESTIONS } from '../data/sampleQuestions';
import { SUBJECTS, TIME_OPTIONS_MIN } from '../data/subjectConfig';
import { selectExam } from '../engine/selectExam';
import { db } from '../db';
import type { ExamPaper, OrderMode, Subject } from '../types';

function nextId(): string {
  return crypto.randomUUID();
}

export default function ExamBuilder() {
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState<Subject[]>(['數學']);
  const [years, setYears] = useState<number[]>([AVAILABLE_YEARS[AVAILABLE_YEARS.length - 1]]);
  const [totalMinutes, setTotalMinutes] = useState(70);
  const [orderMode, setOrderMode] = useState<OrderMode>('shuffled');

  const preview = useMemo(
    () =>
      selectExam({
        allQuestions: SAMPLE_QUESTIONS,
        subjects,
        years,
        totalMinutes,
        orderMode,
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [subjects, years, totalMinutes, orderMode]
  );

  function toggleSubject(s: Subject) {
    setSubjects((prev) => (prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]));
  }
  function toggleYear(y: number) {
    setYears((prev) => (prev.includes(y) ? prev.filter((x) => x !== y) : [...prev, y]));
  }

  async function handleStart() {
    if (subjects.length === 0 || years.length === 0 || preview.questionIds.length === 0) return;
    const paper: ExamPaper = {
      id: nextId(),
      createdAt: Date.now(),
      subjects,
      years,
      totalMinutes,
      orderMode,
      questionIds: preview.questionIds,
      breakdown: preview.breakdown,
      timeBudgetSec: preview.timeBudgetSec,
    };
    await db.examPapers.add(paper);
    navigate(`/exam/${paper.id}`);
  }

  return (
    <div className="card">
      <div className="field">
        <div className="field-label">科目（可多選）</div>
        <div className="chip-row">
          {SUBJECTS.map((s) => (
            <span
              key={s}
              className={`chip ${subjects.includes(s) ? 'selected' : ''}`}
              onClick={() => toggleSubject(s)}
            >
              {s}
            </span>
          ))}
        </div>
      </div>

      <div className="field">
        <div className="field-label">年度（可多選）</div>
        <div className="chip-row">
          {AVAILABLE_YEARS.map((y) => (
            <span
              key={y}
              className={`chip ${years.includes(y) ? 'selected' : ''}`}
              onClick={() => toggleYear(y)}
            >
              {y}
            </span>
          ))}
        </div>
      </div>

      <div className="field">
        <div className="field-label">排序方式</div>
        <div className="chip-row">
          <span
            className={`chip ${orderMode === 'original' ? 'selected' : ''}`}
            onClick={() => setOrderMode('original')}
          >
            原始順序
          </span>
          <span
            className={`chip ${orderMode === 'shuffled' ? 'selected' : ''}`}
            onClick={() => setOrderMode('shuffled')}
          >
            亂數
          </span>
        </div>
      </div>

      <div className="field">
        <div className="field-label">總時間預算（{totalMinutes}分鐘，選多科時平均分配）</div>
        <div className="chip-row">
          {TIME_OPTIONS_MIN.map((m) => (
            <span
              key={m}
              className={`chip ${totalMinutes === m ? 'selected' : ''}`}
              onClick={() => setTotalMinutes(m)}
            >
              {m}分鐘
            </span>
          ))}
        </div>
      </div>

      <div className="estimate-box">
        <div className="label">預估作答題數 / 時間</div>
        <div className="value">
          {subjects.length === 0
            ? '請先選科目'
            : `共 ${preview.questionIds.length} 題 · 約 ${Math.round(preview.timeBudgetSec / 60)} 分鐘`}
        </div>
      </div>

      <div className="breakdown-row">
        {preview.breakdown.map((b) => (
          <span key={b.subject} className="breakdown-item">
            {b.subject} <b>{b.count}題</b> · {Math.round(b.sec / 60)}分
          </span>
        ))}
      </div>

      <button className="primary" onClick={handleStart} disabled={preview.questionIds.length === 0}>
        開始測驗
      </button>
    </div>
  );
}
