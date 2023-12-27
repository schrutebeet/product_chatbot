from sqlalchemy import Boolean, Column, Date, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP

default_cols = {
    "timestamp": Column(TIMESTAMP(timezone=True), nullable=False),
    "date": Column(Date, nullable=False, primary_key=True),
    "id": Column(String, nullable=False, primary_key=True),
    "title": Column(String, nullable=False),
    "product_name": Column(Text),
    "coming_soon": Column(Boolean),
    "eci_exclusive": Column(Boolean),
    "exclusive": Column(Boolean),
    "express": Column(Boolean),
    "express_delivery": Column(Boolean),
    "new": Column(Boolean),
    "brand": Column(String),
    "official_price": Column(Float),
    "current_price": Column(Float),
    "discount_percent": Column(Integer),
    "currency": Column(String),
    "provider": Column(String),
    "link": Column(String),
    "image_link": Column(String),
}
