const rtf = new Intl.RelativeTimeFormat('en', {
  localeMatcher: 'best fit',
  numeric: 'always',
  style: 'short',
});

const unitBounds: readonly [number, number, Intl.RelativeTimeFormatUnit][] = [
  [60, 1, 'second'],
  [3600, 60, 'minute'],
  [86400, 3600, 'hour'],
  [86400 * 30, 86400, 'day'],
  [86400 * 365, 86400 * 30, 'month'],
  [Infinity, 86400 * 365, 'year'],
];

export const formatDate = (d: Date | number) =>
  (d instanceof Date ? d : new Date(d)).toISOString().split('T')[0];

export const formatDateTime = (d: Date | number) =>
  (d instanceof Date ? d : new Date(d)).toISOString().split('T').join(' ').split('.')[0];

export const relativeTime = (d: Date | number) => {
  const delta = ((d instanceof Date ? d.getTime() : d) - Date.now()) / 1000;
  const absDelta = Math.abs(delta);
  for (const [upperBound, ratio, unit] of unitBounds) {
    if (absDelta < upperBound) {
      return rtf.format(Math.round(delta / ratio), unit);
    }
  }
  return 'err';
};
