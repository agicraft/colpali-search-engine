import type { FilteringQuery } from '@/core/ApiService';

export class FilteringQueryDt {
  public page = 1;
  public perPage = 10;
  public search = '';
  public sortBy: readonly any[] = [];
}

export const mapDtToApiQuery = ({
  page,
  perPage,
  sortBy,
  search,
}: FilteringQueryDt): FilteringQuery => {
  const ret: FilteringQuery = {
    page,
    perPage,
  };
  if (search) {
    ret.search = search;
  }
  if (sortBy && sortBy.length) {
    ret.sortBy = `${sortBy[0].key},${sortBy[0].order}`;
  }
  return ret;
};
