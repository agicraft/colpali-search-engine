import { computed, ref } from 'vue';

export const persistentValue = <T>(key: string, value: T) => {
  const storage = window.localStorage;
  const storedValue = storage.getItem(key);
  if (storedValue !== null) {
    value = JSON.parse(storedValue);
  }
  return {
    get value(): T {
      return value;
    },
    set value(v: T) {
      value = v;
      storage.setItem(key, JSON.stringify(v));
    },
  };
};

export const refPersistent = <T>(key: string, value: T) => {
  const persistentVal = persistentValue(key, value);
  const r = ref(persistentVal.value);
  return computed({
    get: () => r.value,
    set: (v) => {
      r.value = v;
      persistentVal.value = v as T;
    },
  });
};
