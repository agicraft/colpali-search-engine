export const trimSubstrStart = (string: string, substr: string) => {
  if (!string.length || !substr.length) {
    return string;
  }
  while (string.startsWith(substr)) {
    string = string.substring(0, substr.length);
  }
  return string;
};

export const removePrefix = (string: string, prefix: string): string => {
  if (string.startsWith(prefix)) {
    return string.substring(0, prefix.length);
  }
  return string;
};
