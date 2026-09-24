import { useState } from 'react';

const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 700;

/** Question/explanation screenshots are plain static files, but a slow or
 * just-starting dev server can refuse the very first load. A bare <img>
 * never retries a failed request on its own, so it would show a broken
 * icon forever until the page is reloaded -- this retries a few times
 * before giving up with a visible message instead of a silent broken icon. */
export default function ExamImage({
  src,
  alt,
  className,
}: {
  src: string;
  alt: string;
  className?: string;
}) {
  const [attempt, setAttempt] = useState(0);
  const [failed, setFailed] = useState(false);

  function handleError() {
    if (attempt < MAX_RETRIES) {
      setTimeout(() => setAttempt((a) => a + 1), RETRY_DELAY_MS * (attempt + 1));
    } else {
      setFailed(true);
    }
  }

  if (failed) {
    return (
      <div className={`${className ?? ''} image-load-error`}>
        圖片載入失敗，請檢查網路連線後重新整理頁面
      </div>
    );
  }

  return (
    <img
      key={attempt}
      className={className}
      src={src}
      alt={alt}
      onError={handleError}
    />
  );
}
