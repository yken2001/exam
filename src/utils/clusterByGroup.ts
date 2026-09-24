import type { Question } from '../types';

/** Consecutive questions sharing a groupId share one image (a group's
 * question/explanation bank was cropped as a single shared-passage
 * picture), so callers render them as one card with the image shown once
 * and each sub-question's own answer row underneath. */
export function clusterByGroup(qs: Question[]): Question[][] {
  const clusters: Question[][] = [];
  for (const q of qs) {
    const last = clusters[clusters.length - 1];
    if (q.groupId && last && last[0].groupId === q.groupId) {
      last.push(q);
    } else {
      clusters.push([q]);
    }
  }
  return clusters;
}
