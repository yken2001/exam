import { useEffect, useRef, useState } from 'react';

const SPEEDS = [0.5, 0.75, 1, 1.25];

function fmt(sec: number): string {
  if (!isFinite(sec)) return '0:00';
  const s = Math.floor(sec);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
}

/** Practice player for a listening question: play/pause, replay from the
 * start, seek, and slower/faster playback. Starting one player pauses any
 * other on the page, since a page can hold two listening questions. */
export default function AudioPlayer({ src }: { src: string }) {
  const ref = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const [time, setTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [rate, setRate] = useState(1);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    const a = ref.current;
    if (a) {
      a.playbackRate = rate;
      a.defaultPlaybackRate = rate;
    }
  }, [rate]);

  function toggle() {
    const a = ref.current;
    if (!a) return;
    if (a.paused) a.play().catch(() => setFailed(true));
    else a.pause();
  }

  function replay() {
    const a = ref.current;
    if (!a) return;
    a.currentTime = 0;
    a.play().catch(() => setFailed(true));
  }

  function onPlay() {
    setPlaying(true);
    document.querySelectorAll('audio').forEach((other) => {
      if (other !== ref.current) other.pause();
    });
  }

  return (
    <div className="audio-player">
      <audio
        ref={ref}
        src={src}
        preload="metadata"
        onPlay={onPlay}
        onPause={() => setPlaying(false)}
        onEnded={() => setPlaying(false)}
        onTimeUpdate={(e) => setTime(e.currentTarget.currentTime)}
        onLoadedMetadata={(e) => {
          setDuration(e.currentTarget.duration);
          e.currentTarget.playbackRate = rate;
        }}
        onError={() => setFailed(true)}
      />
      {failed ? (
        <div className="image-load-error">音檔載入失敗</div>
      ) : (
        <>
          <div className="audio-row">
            <button className="primary audio-main" onClick={toggle}>
              {playing ? '⏸ 暫停' : '▶ 播放'}
            </button>
            <button onClick={replay}>↺ 重播</button>
            <input
              className="audio-seek"
              type="range"
              min={0}
              max={duration || 0}
              step={0.1}
              value={time}
              onChange={(e) => {
                if (ref.current) ref.current.currentTime = Number(e.target.value);
              }}
            />
            <span className="audio-time">
              {fmt(time)} / {fmt(duration)}
            </span>
          </div>
          <div className="audio-row">
            <span className="audio-label">速度</span>
            {SPEEDS.map((s) => (
              <span key={s} className={`chip ${rate === s ? 'selected' : ''}`} onClick={() => setRate(s)}>
                {s}x
              </span>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
