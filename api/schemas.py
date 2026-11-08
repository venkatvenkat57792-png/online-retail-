from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class InvoiceFeatures(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    line_count: int = Field(gt=0, le=100_000, description="Number of purchased transaction lines")
    distinct_products: int = Field(gt=0, le=100_000, description="Number of distinct stock codes")
    total_quantity: float = Field(gt=0, le=10_000_000, description="Total units in the invoice")
    country: str = Field(min_length=1, max_length=100)

    @field_validator("country")
    @classmethod
    def country_not_blank(cls, value):
        if not value.strip():
            raise ValueError("country cannot be blank")
        return value.strip()

    @model_validator(mode="after")
    def products_fit_lines(self):
        if self.distinct_products > self.line_count:
            raise ValueError("distinct_products cannot exceed line_count")
        return self

class Prediction(BaseModel):
    predicted_invoice_revenue: float = Field(ge=0)
    currency: str = "GBP"
    model_version: str
    request_id: str
