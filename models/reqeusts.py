from typing import Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    pass
    # name: str
    # description: Optional[str] = None


class ExportReqeust(BaseModel):
    pass