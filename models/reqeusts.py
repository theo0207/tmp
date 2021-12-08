from typing import List, Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    from_: int
    size: int
    search_field: Optional[str] = None
    search_keyword: Optional[str] = None
    sort_field: Optional[str] = None
    order: Optional[str] = None


class ExportReqeust(SearchRequest):
    columns: Optional[List[str]] = None