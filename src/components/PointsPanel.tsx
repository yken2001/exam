import { useEffect, useState } from 'react';
import type { PointsSummary } from '../engine/points';

const SEEN_LEVEL_KEY = 'exam-app:seen-level';

function readSeenLevel(): number {
  try {
    return Number(localStorage.getItem(SEEN_LEVEL_KEY)) || 0;
  } catch {
    return 0;
  }
}

/** Level, experience bar and progress; the bar fills up when shown, and a
 * level reached since the last visit is celebrated once. */
export default function PointsPanel({ summary, totalQuestions }: { summary: PointsSummary; totalQuestions: number }) {
  const [filled, setFilled] = useState(false);
  const [levelUp, setLevelUp] = useState<number | null>(null);

  useEffect(() => {
    const t = setTimeout(() => setFilled(true), 80);
    const seen = readSeenLevel();
    if (summary.level > seen && seen > 0) setLevelUp(summary.level);
    try {
      localStorage.setItem(SEEN_LEVEL_KEY, String(summary.level));
    } catch {
      /* storage blocked: just no celebration next time */
    }
    return () => clearTimeout(t);
  }, [summary.level]);

  const inLevel = summary.total - summary.levelStart;
  const cost = summary.levelNext - summary.levelStart;
  const pct = Math.min(100, (inLevel / cost) * 100);
  const seenPct = (summary.seen / totalQuestions) * 100;

  return (
    <div className="card points-panel">
      {levelUp && (
        <div className="level-up" onAnimationEnd={() => setLevelUp(null)}>
          升級！Lv.{levelUp}
        </div>
      )}
      <div className="points-head">
        <div className="level-badge">Lv.{summary.level}</div>
        <div className="points-main">
          <div className="points-total">
            {summary.total.toLocaleString()} <span>積分</span>
          </div>
          <div className="xp-bar">
            <div className="xp-fill" style={{ width: filled ? `${pct}%` : 0 }} />
          </div>
          <div className="points-sub">
            距離 Lv.{summary.level + 1} 還差 {summary.levelNext - summary.total} 分
          </div>
        </div>
      </div>
      <div className="points-stats">
        <div>
          <b>{summary.seen}</b> / {totalQuestions} 題 已做過
          <div className="mini-bar">
            <div style={{ width: filled ? `${seenPct}%` : 0 }} />
          </div>
        </div>
        <div>
          <b>{summary.mastered}</b> 題 精熟
          <div className="points-sub">不同的兩天都答對</div>
        </div>
      </div>
    </div>
  );
}
