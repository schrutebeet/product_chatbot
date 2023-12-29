from sqlalchemy import Boolean, Column, Date, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP

from database.connection import Base

# this Item model (table) stems from the Base class and has its properties
# named in an object-oriented style


class ECISupermarket(Base):
    __tablename__ = "ECIsupermarket"
    __table_args__ = {"schema": "elCorteIngles"}
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    date = Column(Date, nullable=False, primary_key=True)
    id = Column(String, nullable=False, primary_key=True)
    product_name = Column(Text, nullable=False)
    category_1 = Column(Text, nullable=False, primary_key=True)
    category_2 = Column(Text, primary_key=True)
    category_3 = Column(Text, primary_key=True)
    category_4 = Column(Text, primary_key=True)
    brand = Column(String)
    original_price = Column(Float)
    final_price = Column(Float)
    discount = Column(Boolean)
    status = Column(String)
    currency = Column(String)

class Mercadona(Base):
    __tablename__ = "mercadona"
    __table_args__ = {"schema": "Mercadona"}
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    date = Column(Date, nullable=False, primary_key=True)
    id = Column(String, nullable=False, primary_key=True)
    product_name = Column(Text, nullable=False)
    category_1 = Column(Text, nullable=False, primary_key=True)
    category_2 = Column(Text, primary_key=True)
    category_3 = Column(Text, primary_key=True)
    previous_unit_price = Column(Float)
    unit_price = Column(Float)
    unit_size = Column(Float)
    size_format = Column(String)
    iva = Column(Integer)
    reference_price = Column(Float)
    reference_unit = Column(String)
    total_units = Column(Integer)
    is_new = Column(Boolean)
    is_pack = Column(Boolean)
    packaging = Column(String)
    link = Column(String)
    image_link = Column(String)


def create_dynamic_model(class_name, model_name, schema_name, column_data):
    # Define the attributes for the class
    class_attributes = {
        "__tablename__": model_name,
        "__table_args__": {"schema": schema_name},
    }

    # Add columns to the class attributes
    for column_name, column_type in column_data.items():
        class_attributes[column_name] = column_type

    # Create the class using the type function
    dynamic_class = type(class_name, (Base,), class_attributes)
    return dynamic_class
