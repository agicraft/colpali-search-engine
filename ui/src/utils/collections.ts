export function range(end: number): IterableIterator<number>;
export function range(start: number, end: number): IterableIterator<number>;

export function* range(arg1: number, arg2?: number): IterableIterator<number> {
  const start = arg2 !== undefined ? arg1 : 0;
  const end = arg2 !== undefined ? arg2 : arg1;
  for (let i = start; i <= end; i++) {
    yield i;
  }
}

export const sortBy = <T>(key: keyof T): ((a: T, b: T) => number) => {
  return (a, b) => (a[key] > b[key] ? 1 : b[key] > a[key] ? -1 : 0);
};

export const without = <T>(items: T[], key: keyof T, value: T[keyof T]) => {
  return items.filter((item) => item[key] !== value);
};

export const remove = <T>(items: T[], key: keyof T, value: T[keyof T]) => {
  const item = find(items, key, value);
  if (item) {
    items.splice(items.indexOf(item), 1);
  }
};

export const find = <T>(items: T[], key: keyof T, value: T[keyof T]) => {
  return items.find((item) => item[key] === value);
};

export const replace = <T>(items: T[], key: keyof T, item: T) => {
  const oldItem = find(items, key, item[key]);
  if (oldItem) {
    items.splice(items.indexOf(oldItem), 1, item);
  }
};

export const indexBy = <T>(items: T[], key: keyof T) =>
  items.reduce((r, x) => ({ ...r, [String(x[key])]: x }), {} as { [k: string]: T });

export const groupBy = <T>(items: T[], key: keyof T) =>
  items.reduce((r, x) => {
    const kv = String(x[key]);
    if (!r[kv]) {
      r[kv] = [];
    }
    r[kv].push(x);
    return r;
  }, {} as { [k: string]: T[] });
