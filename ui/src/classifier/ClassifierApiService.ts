import { injectable, inject } from 'inversify';
import { ApiService, type FilteringQuery, type FilteringResult } from '@/core/ApiService';
import type {
  DocPreviewDto,
  DocumentDto,
  RagResponseDto,
  SearchResponseDto,
} from './classifier-dto';

@injectable()
export class ClassifierApiService {
  public constructor(@inject(ApiService) private apiService: ApiService) {}

  public getUploadEndpoint() {
    return this.apiService.makeUrl('documents/upload');
  }

  public getChunkInterpretUrl(id: number, query: string) {
    return this.apiService.makeUrl(
      `documents/chunk/${id}/interpret?q=${decodeURIComponent(query)}`,
    );
  }

  public getChunkImageUrl(id: number) {
    return this.apiService.makeUrl(`documents/chunk/${id}/image`);
  }

  public getPageImageUrl(id: number) {
    return this.apiService.makeUrl(`documents/page/${id}/image`);
  }

  public getDocDownloadUrl(id: number) {
    return this.apiService.makeUrl(`documents/${id}/download`);
  }

  public async previewDocument(id: number): Promise<DocPreviewDto> {
    return this.apiService.fetch({
      method: 'GET',
      endpoint: `documents/${id}/preview`,
    });
  }

  public async getDocuments(query: FilteringQuery): Promise<FilteringResult<DocumentDto[]>> {
    return this.apiService.fetch({
      method: 'GET',
      endpoint: 'documents',
      query: { ...query },
      fetchTotal: true,
    });
  }

  public async ragRequest(data: {
    query: string;
    chunks: number[];
    requestId: number;
  }): Promise<RagResponseDto> {
    return this.apiService.fetch({
      method: 'POST',
      endpoint: 'documents/rag',
      data,
    });
  }

  public async search(query: string): Promise<SearchResponseDto> {
    // console.log(`Searching for ${data}`);
    return this.apiService.fetch({ method: 'POST', endpoint: 'documents/search', data: { query } });
  }

  public async deleteDocument(docId: number): Promise<void> {
    return this.apiService.fetch({ method: 'DELETE', endpoint: `documents/${docId}` });
  }
}
