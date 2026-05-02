export function formatPercent(value) {
  return `${Math.round((value || 0) * 100)}%`;
}

export function formatScore(value) {
  return Number(value || 0).toFixed(2);
}
