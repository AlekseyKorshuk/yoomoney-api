from pydantic import BaseModel


class DigitalBonus(BaseModel):
    serial: str
    secret: str
