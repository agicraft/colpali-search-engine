import { injectable } from 'inversify';
import { type DocumentDto, type SearchDocumentDto, type SearchResponseDto } from './classifier-dto';
import { ClassifierApiService } from './ClassifierApiService';
import { sleep } from '@/utils/async';
import { MimeType } from '@/utils/files';
import type { FilteringQuery, FilteringResult } from '@/core/ApiService';

const documents: (DocumentDto & SearchDocumentDto)[] = [
  { numPages: 42, indexed: true, mime: MimeType.PDF, name: 'ИИ: Полный справочник' },
  { numPages: 10, indexed: false, mime: MimeType.DOCX, name: 'Почему ИИ это миф?' },
  { numPages: 33, indexed: true, mime: MimeType.XLSX, name: 'Базовая оценка производительности' },
  { numPages: 1, indexed: false, mime: MimeType.PNG, name: 'Опасность ИИ' },
  { numPages: 12, indexed: true, mime: MimeType.MD, name: 'Я и мои роботы' },
  { numPages: 55, indexed: true, mime: MimeType.PPTX, name: 'Как заработать на ИИ' },
].map((item, idx) => ({
  ...item,
  chunkId: 1,
  docId: 1,
  pageId: 1,
  numChunks: Number(item.indexed) * item.numPages * 3,
  createdAt: Date.now() - Math.random() * 1000000,
  id: idx + 1,
}));

@injectable()
export class MockClassifierApiService extends ClassifierApiService {
  public getUploadEndpoint() {
    return 'mock-upload';
  }

  public async getDocuments(query: FilteringQuery): Promise<FilteringResult<DocumentDto[]>> {
    await sleep(500);
    return {
      items: documents,
      total: documents.length * 100,
    };
  }

  public async search(data: string): Promise<SearchResponseDto> {
    // console.log(`Searching for ${data}`);
    await sleep(500);
    // answer: `
    // Искусственный интеллект (ИИ) — это область компьютерных наук, которая занимается разработкой систем, способных выполнять задачи, требующие человеческого интеллекта. Примеры таких задач включают:
    // - Распознавание речи и изображений.
    // - Принятие решений.

    // ## Категории ИИ
    // 1. **Узкий ИИ (Narrow AI):** Выполняет одну конкретную задачу, например, поиск в интернете или распознавание лиц.
    // 2. **Общий ИИ (General AI):** Теоретическая концепция системы, способной выполнять любые интеллектуальные задачи на уровне человека.
    // `,
    return {
      documents,
    };
  }
}
