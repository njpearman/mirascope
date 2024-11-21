from typing import Literal
from pydantic import BaseModel


class ToolCallNameResponseChunk(BaseModel):
    """
    A chunk that contains the name and ID of a streamed tool call.
    """

    name: str
    id: str

    @property
    def name(self) -> str:
        return self.name

    @property
    def id(self) -> str:
        return self.id


class ToolCallArgumentsResponseChunk(BaseModel):
    """
    A chunk that contains a delta in the function arguments of a streamed tool call.
    """

    delta: str

    @property
    def delta(self) -> str:
        return self.delta
