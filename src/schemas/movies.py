import datetime as dt
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from database.models import MovieStatusEnum


class CountrySchema(BaseModel):
    id: int
    code: str
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class NamedEntitySchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MovieListItemSchema(BaseModel):
    id: int
    name: str
    date: dt.date
    score: float
    overview: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedMovieListSchema(BaseModel):
    movies: List[MovieListItemSchema]
    total_pages: int
    total_items: int
    prev_page: Optional[str]
    next_page: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class MovieDetailSchema(BaseModel):
    id: int
    name: str
    date: dt.date
    score: float
    overview: Optional[str] = None
    status: MovieStatusEnum
    budget: float
    revenue: float
    country: CountrySchema
    genres: List[NamedEntitySchema]
    actors: List[NamedEntitySchema]
    languages: List[NamedEntitySchema]

    model_config = ConfigDict(from_attributes=True)


class MovieCreateSchema(BaseModel):
    name: str = Field(..., max_length=255)
    date: dt.date
    score: float = Field(..., ge=0, le=100)
    overview: Optional[str] = None
    status: MovieStatusEnum
    budget: float = Field(..., ge=0)
    revenue: float = Field(..., ge=0)
    country: str = Field(..., min_length=2, max_length=3)
    genres: List[str] = Field(...)
    actors: List[str] = Field(...)
    languages: List[str] = Field(...)

    @field_validator("date")
    @classmethod
    def _date_not_too_future(cls, v: dt.date) -> dt.date:
        if v > dt.date.today() + dt.timedelta(days=365):
            raise ValueError("date too far")
        return v


class MovieUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    date: Optional[dt.date] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[MovieStatusEnum] = None
    budget: Optional[float] = Field(None, ge=0)
    revenue: Optional[float] = Field(None, ge=0)

    model_config = ConfigDict(extra="forbid")

    @field_validator("date")
    @classmethod
    def _date_not_too_future_update(cls, v: Optional[dt.date]) -> Optional[dt.date]:
        if v is not None and v > dt.date.today() + dt.timedelta(days=365):
            raise ValueError("date too far")
        return v


MovieShortSchema = MovieListItemSchema
MovieListResponseSchema = PaginatedMovieListSchema
MovieResponseSchema = MovieDetailSchema
