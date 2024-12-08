from enum import StrEnum
from typing import Any, Callable, Generic, Iterable, List, Optional, Tuple, TypeVar
from fastapi import Request, Response
from sqlalchemy.orm import Query

T = TypeVar("T")


class FilteringOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"

    @classmethod
    def from_str(cls, s: str) -> "FilteringOrder":
        if s == cls.ASC:
            return cls.ASC
        if s == cls.DESC:
            return cls.DESC
        raise ValueError


class FilteringQuery:
    search: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort_by: Optional[Tuple[str, FilteringOrder]] = None


class FilteringResult(Generic[T]):
    items: Iterable[T]
    total: int


def apply_filter_to_db_query(
    filtering_query: FilteringQuery,
    q: Query,
    sort_to_col: Optional[Callable[[str], Any]],
    apply_search: Optional[Callable[[Any, str], Any]],
    q_total: Optional[Query] = None,
    map_item: Optional[Callable[[Iterable[Any]], Iterable[T]]] = None,
) -> FilteringResult[T]:
    if filtering_query.page != None and filtering_query.page < 1:
        raise ValueError(f"Page must start from 1")

    if filtering_query.search and apply_search != None:
        q = apply_search(q, filtering_query.search)
        if q_total:
            q_total = apply_search(q_total, filtering_query.search)

    ret = FilteringResult()
    ret.total = (q_total or q).count()

    if filtering_query.sort_by != None and sort_to_col != None:
        key, order = filtering_query.sort_by
        sort_column = sort_to_col(key)
        if order == FilteringOrder.ASC:
            q = q.order_by(sort_column.asc())
        else:
            q = q.order_by(sort_column.desc())

    if filtering_query.page != None and filtering_query.per_page != None:
        q = q.offset((filtering_query.page - 1) * filtering_query.per_page).limit(
            filtering_query.per_page
        )
    items = q.all()
    ret.items = map_item(items) if map_item != None else items
    return ret


def apply_filtering_result_to_response(
    filtering_result: FilteringResult[T], response: Response
) -> Iterable[T]:
    response.headers["X-Total"] = str(filtering_result.total)
    return filtering_result.items


def create_filter_from_request(request: Request) -> FilteringQuery:
    ret = FilteringQuery()
    params = request.query_params

    if "page" in params:
        ret.page = int(params["page"])
    if "perPage" in params:
        ret.per_page = int(params["perPage"])
    if "search" in params:
        ret.search = str(params["search"])[0:255]
    if "sortBy" in params:
        key, order = str(params["sortBy"]).split(",")
        ret.sort_by = (key, FilteringOrder.from_str(order))

    return ret
