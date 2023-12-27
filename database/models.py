from database.connection import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy import String, Column, Text, Date, Float, Boolean, Integer

# this Item model (table) stems from the Base class and has its properties 
# named in an object-oriented style

SCHEMA = "elCorteIngles"
    
class Supermarket(Base):
    __tablename__ = "supermarket"
    __table_args__ = {'schema': SCHEMA}
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    date = Column(Date, nullable=False, primary_key=True)
    id = Column(String, nullable=False, primary_key=True)
    product_name = Column(Text, nullable=False)
    category_1 = Column(Text, nullable=False)
    category_2 = Column(Text)
    category_3 = Column(Text)
    category_4 = Column(Text)
    category_5 = Column(Text)
    brand = Column(String)
    original_price = Column(Float)
    final_price = Column(Float)
    discount = Column(Boolean)
    status = Column(String)
    currency = Column(String)


def create_dynamic_model(class_name, model_name, schema_name, column_data):
    # Define the attributes for the class
    class_attributes = {
        "__tablename__": model_name,
        "__table_args__": {'schema': schema_name}
    }

    # Add columns to the class attributes
    for column_name, column_type in column_data.items():
        class_attributes[column_name] = column_type

    # Create the class using the type function
    dynamic_class = type(class_name, (Base,), class_attributes)
    return dynamic_class
