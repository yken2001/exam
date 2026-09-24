import { useEffect, useState } from 'react';

export function useWindowWidth(): number {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const onResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);

  return width;
}

/** Phone landscape -> 1 question, small tablet portrait -> 2 stacked,
 * large tablet portrait -> 3 stacked. Breakpoints are on width since that is
 * what actually constrains how many question cards fit without crowding. */
export function pageSizeForWidth(width: number): 1 | 2 | 3 {
  if (width < 600) return 1;
  if (width < 900) return 2;
  return 3;
}
