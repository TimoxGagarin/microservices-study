from typing import List, Optional

from pydantic import BaseModel


class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[int]


class MovieOut(MovieIn):
    id: int


class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts: Optional[List[int]] = None
