// crypto.randomUUID only exists in secure contexts (https, localhost) -- not
// when the app is served over plain http on a home network.
export function newId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}
