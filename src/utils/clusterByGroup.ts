import type { Question } from '../types';

/** Splits an exam into units: a standalone question, or a whole 題組. A
 * group's question bank image is one shared-passage picture, so callers show
 * a unit as one card -- the image once, then each item's own answer row.
 *
 * selectExam already keeps a group's items together, but this does not rely
 * on it: every item of a group is gathered into the unit where the group
 * first appears, in its original question order, so a group can never be
 * scattered across the exam (e.g. by an old saved paper). */
export function clusterByGroup(qs: Question[]): Question[][] {
  const clusters: Question[][] = [];
  const byGroup = new Map<string, Question[]>();
  for (const q of qs) {
    if (!q.groupId) {
      clusters.push([q]);
      continue;
    }
    const unit = byGroup.get(q.groupId);
    if (unit) {
      unit.push(q);
    } else {
      const fresh = [q];
      byGroup.set(q.groupId, fresh);
      clusters.push(fresh);
    }
  }
  for (const unit of byGroup.values()) unit.sort((a, b) => a.qNo - b.qNo);
  return clusters;
}

/** The exam's questions in unit order (see clusterByGroup): the order every
 * page numbers and shows them in. */
export function inUnitOrder(qs: Question[]): Question[] {
  return clusterByGroup(qs).flat();
}
