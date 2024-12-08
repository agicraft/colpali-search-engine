import type { MimeType } from '@/utils/files';

export interface SearchDocumentDto {
  docId: number;
  name: string;
  mime: MimeType;
  createdAt: number;
  chunkId: number;
  pageId: number;
}

export interface DocumentDto {
  id: number;
  name: string;
  mime: MimeType;
  createdAt: number;
  indexed: boolean;
  numPages?: number;
  numChunks?: number;
}

export interface SearchResponseDto {
  documents: SearchDocumentDto[];
}

export interface RagResponseDto {
  requestId: number;
  answer: string;
}

export interface DocPreviewDto {
  id: number;
  name: string;
  pages: number[];
}
