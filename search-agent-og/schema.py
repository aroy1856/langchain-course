from pydantic import BaseModel, Field
from typing import List

class Source(BaseModel):
    """Schema for a source of information used by agent."""
    url: str = Field(description="URL of the source")

class Result(BaseModel):
    """Schema for a result of a search query."""
    result: str = Field(description="Result of the search query")
    sources: List[Source] = Field(
        default_factory=list,
        description="Sources of the result"
    )
