from __future__ import annotations

import datetime as dt
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from database.models import MovieStatusEnum


date = dt.date


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
    date: date
    score: float
    overview: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedMovieListSchema(BaseModel):
    movies: List[MovieListItemSchema]
    total_pages: int
    total_items: int
    prev_page: Optional[str]
    next_page: Optional[str]


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
    genres: List[str] = Field(default_factory=list)
    actors: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)


class MovieUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    date: Optional[dt.date] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    overview: Optional[str] = None
    status: Optional[MovieStatusEnum] = None
    budget: Optional[float] = Field(None, ge=0)
    revenue: Optional[float] = Field(None, ge=0)
    country: Optional[str] = Field(default=None, min_length=2, max_length=3)
    genres: Optional[List[str]] = None
    actors: Optional[List[str]] = None
    languages: Optional[List[str]] = None

    model_config = ConfigDict(extra="forbid")


MovieShortSchema = MovieListItemSchema
MovieListResponseSchema = PaginatedMovieListSchema
MovieResponseSchema = MovieDetailSchema
