from sqlalchemy import Column, String, Float, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"

    asin = Column(String(50), primary_key=True, index=True)
    product_name = Column(String(500), nullable=False)
    category = Column(String(100), index=True)
    subcategory = Column(String(100), index=True)
    brand = Column(String(100), index=True)
    price_inr = Column(Float, nullable=False)
    mrp_inr = Column(Float, nullable=False)
    discount_pct = Column(Integer)
    rating = Column(Float)
    review_count = Column(Integer)
    color = Column(String(50), index=True)
    material = Column(String(100), index=True)
    pattern = Column(String(100), index=True)
    available_sizes = Column(String(200))  # Comma separated
    seller = Column(String(200), index=True)
    availability = Column(String(50))
    product_url = Column(Text)
    source = Column(String(100))
    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ReviewModel(Base):
    __tablename__ = "reviews"

    review_id = Column(String(100), primary_key=True, index=True)
    product_id = Column(String(50), index=True)
    rating = Column(Float)
    title = Column(String(500))
    text = Column(Text)
    date = Column(String(50))
    source = Column(String(100))
    sentiment = Column(String(50))
    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class CollectionRunModel(Base):
    __tablename__ = "collection_runs"

    run_id = Column(String(100), primary_key=True)
    source_name = Column(String(100))
    status = Column(String(50))  # success, failed, partial
    items_collected = Column(Integer, default=0)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    error_log = Column(Text, nullable=True)
