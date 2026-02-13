from pydantic import BaseModel


class Card(BaseModel):
    pan_fragment: str | None = None
    type: str | None = None
