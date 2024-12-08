export const arrayBufferToBase64 = (input: ArrayBuffer) => {
  return btoa(new Uint8Array(input).reduce((data, byte) => data + String.fromCharCode(byte), ''));
};

export enum MimeType {
  PDF = 'application/pdf',
  MD = 'text/markdown',
  DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  PPTX = 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  JPEG = 'image/jpeg',
  PNG = 'image/png',
}
