import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AVAILABLE_YEARS, SAMPLE_QUESTIONS, yearsWithData } from '../data/sampleQuestions';
import { FRACTIONS, SUBJECTS } from '../data/subjectConfig';
import { selectExam } from '../engine/selectExam';
import { db } from '../db';
import { newId } from '../utils/newId';
import type { ExamPaper, OrderMode, Subject } from '../types';

/** 1050 -> "17 分 30 秒", 4200 -> "70 分鐘" */
function formatMinutes(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return s ? `${m} 分 ${s} 秒` : `${m} 分鐘`;
}

export default function ExamBuilder() {
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [years, setYears] = useState<number[]>([]);
  const [fraction, setFraction] = useState(1);
  const [orderMode, setOrderMode] = useState<OrderMode>('original');
  const [confirming, setConfirming] = useState(false);

  const preview = useMemo(
    () =>
      selectExam({
        allQuestions: SAMPLE_QUESTIONS,
        subjects,
        years,
        fraction,
        orderMode,
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [subjects, years, fraction, orderMode]
  );

  function toggleSubject(s: Subject) {
    setSubjects((prev) => (prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]));
  }
  function toggleYear(y: number) {
    setYears((prev) => (prev.includes(y) ? prev.filter((x) => x !== y) : [...prev, y]));
  }

  const ready = subjects.length > 0 && years.length > 0 && preview.questionIds.length > 0;
  const subjectText = SUBJECTS.filter((s) => subjects.includes(s)).join('、');
  const yearText = [...years].sort((a, b) => a - b).join('、');
  const fractionText = FRACTIONS.find((f) => f.value === fraction)?.label ?? '';
  const minutesText = formatMinutes(preview.timeBudgetSec);

  async function handleStart() {
    setConfirming(false);
    if (!ready) return;
    const paper: ExamPaper = {
      id: newId(),
      createdAt: Date.now(),
      subjects,
      years,
      totalMinutes: Math.round(preview.timeBudgetSec / 60),
      fraction,
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
        {subjects
          .filter((s) => !yearsWithData(s).some((y) => years.includes(y)) && years.length > 0)
          .map((s) => (
            <div key={s} className="field-hint">
              {s}只有 {yearsWithData(s).join('、')} 年的題目，目前選的年度沒有{s}題。
            </div>
          ))}
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
        <div className="field-label">份量（每一科都照會考的題數與時間比例）</div>
        <div className="chip-row">
          {FRACTIONS.map((f) => (
            <span
              key={f.value}
              className={`chip ${fraction === f.value ? 'selected' : ''}`}
              onClick={() => setFraction(f.value)}
            >
              {f.label}
            </span>
          ))}
        </div>
        <div className="field-note">
          全卷＝會考一整份（國文、社會、自然 70 分鐘，英語閱讀 60、聽力 25、數學 80）；只有「全卷＋單一年度」會給官方等級，
          半卷以上給估計等級，1/4 卷只看正確率。
        </div>
      </div>

      <div className="estimate-box">
        <div className="label">預估作答題數 / 時間</div>
        <div className="value">
          {subjects.length === 0 || years.length === 0
            ? '請先選科目與年度'
            : `共 ${preview.questionIds.length} 題 · ${minutesText}`}
        </div>
      </div>

      {ready && (
        <div className="breakdown-row">
          {preview.breakdown.map((b) => (
            <span key={b.subject} className="breakdown-item">
              {b.subject} <b>{b.count}題</b> · {formatMinutes(b.sec)}
            </span>
          ))}
        </div>
      )}

      <button className="primary" onClick={() => setConfirming(true)} disabled={!ready}>
        開始測驗
      </button>

      {confirming && (
        <div className="modal-overlay" onClick={() => setConfirming(false)}>
          <div className="modal-box" onClick={(e) => e.stopPropagation()}>
            <p className="modal-message">確認開始測驗？</p>
            <table className="confirm-table">
              <tbody>
                <tr><th>科目</th><td>{subjectText}</td></tr>
                <tr><th>年度</th><td>{yearText}</td></tr>
                <tr><th>排序</th><td>{orderMode === 'original' ? '原始順序' : '亂數'}</td></tr>
                <tr><th>份量</th><td>{fractionText}</td></tr>
                <tr><th>題數</th><td>{preview.questionIds.length} 題</td></tr>
                <tr><th>時間</th><td>{minutesText}</td></tr>
              </tbody>
            </table>
            <div className="modal-actions">
              <button onClick={() => setConfirming(false)}>取消</button>
              <button className="primary" onClick={handleStart}>
                開始
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
