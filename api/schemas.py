"""
schemas.py
==========
Pydantic models for request validation and response formatting.
"""

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    property_type : str   = Field(..., example="House",       description="Type: House, Flat, Farm House")
    location      : str   = Field(..., example="DHA Defence", description="Islamabad area or sector")
    area_marla    : float = Field(..., example=10.0,          description="Size in Marla (1-100)")
    bedrooms      : int   = Field(..., example=4,             description="Number of bedrooms")
    bathrooms     : int   = Field(..., example=3,             description="Number of bathrooms")

    @field_validator("area_marla")
    @classmethod
    def validate_area(cls, v):
        if v <= 0 or v > 100:
            raise ValueError("area_marla must be between 1 and 100")
        return v

    @field_validator("bedrooms")
    @classmethod
    def validate_bedrooms(cls, v):
        if v < 1 or v > 11:
            raise ValueError("bedrooms must be between 1 and 11")
        return v

    @field_validator("bathrooms")
    @classmethod
    def validate_bathrooms(cls, v):
        if v < 1 or v > 9:
            raise ValueError("bathrooms must be between 1 and 9")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "property_type": "House",
                "location"     : "DHA Defence",
                "area_marla"   : 10.0,
                "bedrooms"     : 4,
                "bathrooms"    : 3,
            }
        }
    }


class PredictionResponse(BaseModel):
    predicted_price_pkr   : float
    predicted_price_label : str
    price_per_marla_pkr   : float
    price_per_marla_label : str
    input_summary         : dict
    model_r2              : float


class HealthResponse(BaseModel):
    status       : str
    model_loaded : bool
    api_version  : str


class InfoResponse(BaseModel):
    model_type     : str
    total_rows     : int
    r2_score       : float
    mae_pkr        : float
    locations      : list
    property_types : list
    area_min_marla : float
    area_max_marla : float