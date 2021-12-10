from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel



class ClauseFilter(BaseModel):
    exist: Optional[bool] = True
    clauses: Optional[List[str]] = None

class DateFilter(BaseModel):
    from_: Optional[date] = None
    to: Optional[date] = None

class Filter(BaseModel):
    vehl_nm: Optional[ClauseFilter] = None
    parts_cd: Optional[ClauseFilter] = None
    prd_dt: Optional[DateFilter] = None
    cfrm_dt: Optional[DateFilter] = None
    used_time: Optional[DateFilter] = None
    occur_area: Optional[str] = None
    occur_country: Optional[str] = None

class TestFilter(BaseModel):
    publisher: Optional[ClauseFilter]
    registerd: Optional[DateFilter]

class SearchRequest(BaseModel):
    from_: int
    size: int
    search_field: Optional[str] = None
    search_keyword: Optional[str] = None
    synonym: Optional[str] = None
    sort_field: Optional[str] = None
    filters: Optional[TestFilter] = None


class ExportReqeust(SearchRequest):
    columns: Optional[List[str]] = None