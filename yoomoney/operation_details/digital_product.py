from pydantic import BaseModel, Field


class DigitalProduct(BaseModel):
    merchant_article_id: str | None = Field(default=None, alias="merchantArticleId")
    serial: str
    secret: str

    model_config = {"populate_by_name": True}
