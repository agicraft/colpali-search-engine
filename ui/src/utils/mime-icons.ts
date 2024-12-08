import { MimeType } from '@/utils/files';
import {
  mdiFileGifBox,
  mdiFileJpgBox,
  mdiFilePdfBox,
  mdiFilePngBox,
  mdiFilePresentationBox,
  mdiFileTableBox,
  mdiFileWordBox,
  mdiTextBox,
} from '@mdi/js';

export const mimeIconDefault = { icon: mdiTextBox, color: 'grey' };

export const mimeIconMap: Record<string, { icon: string; color: string }> = {
  [MimeType.PDF]: { icon: mdiFilePdfBox, color: '#dc1d23' },
  [MimeType.DOCX]: { icon: mdiFileWordBox, color: '#295294' },
  [MimeType.XLSX]: { icon: mdiFileTableBox, color: '#006f39' },
  [MimeType.PPTX]: { icon: mdiFilePresentationBox, color: '#ca4223' },
  [MimeType.JPEG]: { icon: mdiFileJpgBox, color: '#e4ba29' },
  [MimeType.PNG]: { icon: mdiFilePngBox, color: '#e4ba29' },
};

export const mimeToIcon = (mime: string) => {
  return mimeIconMap[mime] || mimeIconDefault;
};
