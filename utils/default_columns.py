from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy import String, Column, Float, Boolean, Text, Integer, Date

default_cols = {
    'timestamp' : Column(TIMESTAMP(timezone=True), nullable=False),
    'date' : Column(Date, nullable=False, primary_key=True),
    'id' : Column(String, nullable=False, primary_key=True),
    'title' : Column(String, nullable=False),
    'product_name' : Column(Text, nullable=False),
    'coming_soon' : Column(Boolean, nullable=False),
    'eci_exclusive' : Column(Boolean, nullable=False),
    'exclusive' : Column(Boolean, nullable=False),
    'express' : Column(Boolean, nullable=False),
    'express_delivery' : Column(Boolean, nullable=False),
    'new' : Column(Boolean, nullable=False),
    'brand' : Column(String, nullable=False),
    'official_price' : Column(Float, nullable=False),
    'current_price' : Column(Float, nullable=False),
    'discount_percent' : Column(Integer, nullable=False),
    'currency' : Column(String, nullable=False),
    'provider' : Column(String, nullable=False),
    'link' : Column(String, nullable=False),
    'image_link' : Column(String, nullable=False),
}