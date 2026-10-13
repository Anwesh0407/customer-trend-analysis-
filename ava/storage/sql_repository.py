"""SQLAlchemy implementation of Repository supporting SQLite and PostgreSQL."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
    create_engine,
    desc,
    asc,
    func,
)
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

from ava.config import get_settings
from ava.models import Niche, Product, Review
from ava.storage.base import Repository

Base = declarative_base()


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), unique=True, nullable=False, index=True)
    display_name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ProductModel(Base):
    __tablename__ = "products"

    asin = Column(String(10), primary_key=True)
    product_name = Column(String(512), nullable=False)
    category = Column(String(128), nullable=False, index=True)
    brand = Column(String(128), nullable=True, index=True)
    price = Column(Float, nullable=True)
    mrp = Column(Float, nullable=True)
    discount_pct = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)
    colour = Column(String(64), nullable=True)
    material = Column(String(64), nullable=True)
    pattern = Column(String(64), nullable=True)
    sizes = Column(Text, nullable=True)  # JSON list stored as string
    seller = Column(String(128), nullable=True)
    availability = Column(String(32), default="in_stock")
    product_url = Column(String(1024), nullable=True)
    source = Column(String(64), default="unknown")
    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_category_brand", "category", "brand"),
        Index("idx_price", "price"),
        Index("idx_rating", "rating"),
    )

    def to_dict(self) -> Dict[str, Any]:
        parsed_sizes = []
        if self.sizes:
            try:
                parsed_sizes = json.loads(self.sizes)
            except Exception:
                parsed_sizes = [s.strip() for s in self.sizes.split(",") if s.strip()]

        return {
            "asin": self.asin,
            "product_name": self.product_name,
            "category": self.category,
            "brand": self.brand,
            "price": self.price,
            "mrp": self.mrp,
            "discount_pct": self.discount_pct,
            "rating": self.rating,
            "review_count": self.review_count,
            "colour": self.colour,
            "material": self.material,
            "pattern": self.pattern,
            "sizes": parsed_sizes,
            "seller": self.seller,
            "availability": self.availability,
            "product_url": self.product_url,
            "source": self.source,
            "collected_at": self.collected_at.isoformat() if self.collected_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ReviewModel(Base):
    __tablename__ = "reviews"

    review_id = Column(String(64), primary_key=True)
    product_id = Column(String(10), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    review_title = Column(String(512), nullable=True)
    review_text = Column(Text, nullable=True)
    review_date = Column(DateTime, nullable=True)
    source = Column(String(64), default="unknown")
    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "review_title": self.review_title,
            "review_text": self.review_text,
            "review_date": self.review_date.isoformat() if self.review_date else None,
            "source": self.source,
            "collected_at": self.collected_at.isoformat() if self.collected_at else None,
        }


class NicheModel(Base):
    __tablename__ = "niches"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    category = Column(String(128), nullable=False, index=True)
    filters_json = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        filters = {}
        try:
            filters = json.loads(self.filters_json) if self.filters_json else {}
        except Exception:
            pass
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "filters": filters,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class IngestRunModel(Base):
    __tablename__ = "ingest_runs"

    id = Column(String(64), primary_key=True)
    source = Column(String(64), nullable=False)
    file = Column(String(512), nullable=True)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    rows_in = Column(Integer, default=0)
    rows_out = Column(Integer, default=0)
    rows_rejected = Column(Integer, default=0)
    status = Column(String(32), default="pending")
    data_mode = Column(String(32), default="demo")
    details_json = Column(Text, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        details = {}
        try:
            details = json.loads(self.details_json) if self.details_json else {}
        except Exception:
            pass
        return {
            "id": self.id,
            "source": self.source,
            "file": self.file,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "rows_in": self.rows_in,
            "rows_out": self.rows_out,
            "rows_rejected": self.rows_rejected,
            "status": self.status,
            "data_mode": self.data_mode,
            "details": details,
        }


class ChatLogModel(Base):
    __tablename__ = "chat_logs"

    id = Column(String(64), primary_key=True)
    session_id = Column(String(64), nullable=True, index=True)
    niche_id = Column(String(64), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    tools_used_json = Column(Text, nullable=True)
    mode = Column(String(32), default="demo")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        tools = []
        try:
            tools = json.loads(self.tools_used_json) if self.tools_used_json else []
        except Exception:
            pass
        return {
            "id": self.id,
            "session_id": self.session_id,
            "niche_id": self.niche_id,
            "question": self.question,
            "answer": self.answer,
            "tools_used": tools,
            "mode": self.mode,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def _to_dt(val: Any) -> Optional[datetime]:
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    try:
        return datetime.fromisoformat(str(val).replace("Z", "+00:00"))
    except Exception:
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(str(val).strip(), fmt).replace(tzinfo=timezone.utc)
            except Exception:
                pass
        return None


class SQLAlchemyRepository(Repository):
    """Unified repository for SQLite and PostgreSQL."""

    def __init__(self, database_url: Optional[str] = None):
        self.db_url = database_url or get_settings().database_url
        connect_args = {}
        if self.db_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
        self.engine = create_engine(self.db_url, connect_args=connect_args)
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    def init_db(self) -> None:
        """Create all tables if they do not exist, and seed default categories."""
        Base.metadata.create_all(bind=self.engine)
        self._seed_default_categories()

    def _seed_default_categories(self) -> None:
        defaults = [
            {
                "id": "cat_kurtas",
                "name": "Women's Kurtas & Kurtis",
                "display_name": "Kurtas & Kurtis",
                "description": "Women's ethnic wear kurtas, kurtis, and tunics.",
                "is_active": True,
            },
            {
                "id": "cat_sarees",
                "name": "Sarees",
                "display_name": "Sarees",
                "description": "Traditional Indian sarees (Coming Soon).",
                "is_active": False,
            },
            {
                "id": "cat_jewellery",
                "name": "Fashion Jewellery",
                "display_name": "Fashion Jewellery",
                "description": "Earrings, necklaces, and bangles (Coming Soon).",
                "is_active": False,
            },
        ]
        session = self.SessionLocal()
        try:
            for cat in defaults:
                existing = session.query(CategoryModel).filter(CategoryModel.name == cat["name"]).first()
                if not existing:
                    session.add(CategoryModel(**cat))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def save_category(self, category_data: Dict[str, Any]) -> None:
        session = self.SessionLocal()
        try:
            existing = session.query(CategoryModel).filter(CategoryModel.id == category_data.get("id")).first()
            if existing:
                for k, v in category_data.items():
                    setattr(existing, k, v)
                existing.updated_at = datetime.now(timezone.utc)
            else:
                session.add(CategoryModel(**category_data))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_categories(self) -> List[Dict[str, Any]]:
        session = self.SessionLocal()
        try:
            cats = session.query(CategoryModel).all()
            return [c.to_dict() for c in cats]
        finally:
            session.close()

    def save_products(self, products: List[Product]) -> int:
        if not products:
            return 0
        session = self.SessionLocal()
        saved_count = 0
        try:
            for p in products:
                sizes_str = json.dumps(p.sizes) if isinstance(p.sizes, list) else (p.sizes or "")
                existing = session.query(ProductModel).filter(ProductModel.asin == p.asin).first()
                p_dt = _to_dt(p.collected_at) or datetime.now(timezone.utc)
                if p_dt.tzinfo is None:
                    p_dt = p_dt.replace(tzinfo=timezone.utc)

                if existing:
                    # Dedupe rule 10: newest collected_at wins; tie broken by completeness
                    ex_dt = existing.collected_at or datetime.min.replace(tzinfo=timezone.utc)
                    if ex_dt.tzinfo is None:
                        ex_dt = ex_dt.replace(tzinfo=timezone.utc)

                    should_update = False
                    if p_dt > ex_dt:
                        should_update = True
                    elif p_dt == ex_dt:
                        # completeness tiebreak
                        p_comp = sum(1 for v in [p.price, p.mrp, p.rating, p.colour, p.material, p.pattern] if v is not None)
                        ex_comp = sum(1 for v in [existing.price, existing.mrp, existing.rating, existing.colour, existing.material, existing.pattern] if v is not None)
                        if p_comp >= ex_comp:
                            should_update = True

                    if should_update:
                        existing.product_name = p.product_name
                        existing.category = p.category
                        existing.brand = p.brand
                        existing.price = p.price
                        existing.mrp = p.mrp
                        existing.discount_pct = p.discount_pct
                        existing.rating = p.rating
                        existing.review_count = p.review_count
                        existing.colour = p.colour
                        existing.material = p.material
                        existing.pattern = p.pattern
                        existing.sizes = sizes_str
                        existing.seller = p.seller
                        existing.availability = p.availability
                        existing.product_url = p.product_url
                        existing.source = p.source
                        existing.collected_at = p_dt
                        existing.updated_at = datetime.now(timezone.utc)
                        saved_count += 1
                else:
                    new_item = ProductModel(
                        asin=p.asin,
                        product_name=p.product_name,
                        category=p.category,
                        brand=p.brand,
                        price=p.price,
                        mrp=p.mrp,
                        discount_pct=p.discount_pct,
                        rating=p.rating,
                        review_count=p.review_count,
                        colour=p.colour,
                        material=p.material,
                        pattern=p.pattern,
                        sizes=sizes_str,
                        seller=p.seller,
                        availability=p.availability,
                        product_url=p.product_url,
                        source=p.source,
                        collected_at=p_dt,
                        updated_at=datetime.now(timezone.utc),
                    )
                    session.add(new_item)
                    saved_count += 1
            session.commit()
            return saved_count
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_products(
        self,
        category: Optional[str] = None,
        niche_filter: Optional[Dict[str, Any]] = None,
        sort_by: str = "review_count",
        sort_order: str = "desc",
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Dict[str, Any]], int]:
        all_items = self.get_all_products_for_niche(category=category, niche_filter=niche_filter)
        
        # Sort
        reverse = sort_order.lower() == "desc"
        def sort_key(x):
            val = x.get(sort_by)
            if val is None:
                return -1e9 if reverse else 1e9
            return val

        sorted_items = sorted(all_items, key=sort_key, reverse=reverse)
        total = len(sorted_items)
        page_items = sorted_items[offset : offset + limit]
        return page_items, total

    def get_product_by_asin(self, asin: str) -> Optional[Dict[str, Any]]:
        session = self.SessionLocal()
        try:
            prod = session.query(ProductModel).filter(ProductModel.asin == asin.strip().upper()).first()
            return prod.to_dict() if prod else None
        finally:
            session.close()

    def get_all_products_for_niche(
        self,
        category: Optional[str] = None,
        niche_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch products and apply niche filtering via python/pandas for dialect consistency."""
        session = self.SessionLocal()
        try:
            query = session.query(ProductModel)
            if category:
                query = query.filter(ProductModel.category == category)
            prods = [p.to_dict() for p in query.all()]
        finally:
            session.close()

        if niche_filter:
            from ava.analytics.niche_filter import apply_niche_filter
            prods = apply_niche_filter(prods, niche_filter)
        return prods

    def save_reviews(self, reviews: List[Review]) -> int:
        if not reviews:
            return 0
        session = self.SessionLocal()
        saved = 0
        try:
            for r in reviews:
                existing = session.query(ReviewModel).filter(ReviewModel.review_id == r.review_id).first()
                r_date = _to_dt(r.review_date)
                r_col = _to_dt(r.collected_at) or datetime.now(timezone.utc)
                if not existing:
                    session.add(
                        ReviewModel(
                            review_id=r.review_id,
                            product_id=r.product_id,
                            rating=r.rating,
                            review_title=r.review_title,
                            review_text=r.review_text,
                            review_date=r_date,
                            source=r.source,
                            collected_at=r_col,
                        )
                    )
                    saved += 1
            session.commit()
            return saved
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_reviews(
        self,
        asin: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Dict[str, Any]], int]:
        session = self.SessionLocal()
        try:
            query = session.query(ReviewModel)
            if asin:
                query = query.filter(ReviewModel.product_id == asin.strip().upper())
            elif category:
                # join with products
                query = query.join(ProductModel, ReviewModel.product_id == ProductModel.asin).filter(ProductModel.category == category)
            
            total = query.count()
            rows = query.order_by(desc(ReviewModel.review_date)).offset(offset).limit(limit).all()
            return [r.to_dict() for r in rows], total
        finally:
            session.close()

    def save_niche(self, niche: Niche) -> Dict[str, Any]:
        session = self.SessionLocal()
        try:
            existing = session.query(NicheModel).filter(NicheModel.id == niche.id).first()
            filters_str = json.dumps(niche.filters)
            if existing:
                existing.name = niche.name
                existing.category = niche.category
                existing.filters_json = filters_str
                existing.description = niche.description
                existing.updated_at = datetime.now(timezone.utc)
                session.commit()
                return existing.to_dict()
            else:
                new_niche = NicheModel(
                    id=niche.id,
                    name=niche.name,
                    category=niche.category,
                    filters_json=filters_str,
                    description=niche.description,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                session.add(new_niche)
                session.commit()
                return new_niche.to_dict()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_niches(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        session = self.SessionLocal()
        try:
            query = session.query(NicheModel)
            if category:
                query = query.filter(NicheModel.category == category)
            rows = query.order_by(desc(NicheModel.updated_at)).all()
            return [r.to_dict() for r in rows]
        finally:
            session.close()

    def get_niche_by_id(self, niche_id: str) -> Optional[Dict[str, Any]]:
        session = self.SessionLocal()
        try:
            n = session.query(NicheModel).filter(NicheModel.id == niche_id).first()
            return n.to_dict() if n else None
        finally:
            session.close()

    def delete_niche(self, niche_id: str) -> bool:
        session = self.SessionLocal()
        try:
            n = session.query(NicheModel).filter(NicheModel.id == niche_id).first()
            if n:
                session.delete(n)
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def save_ingest_run(self, run_data: Dict[str, Any]) -> None:
        session = self.SessionLocal()
        try:
            details_str = json.dumps(run_data.get("details", {}))
            started_at = run_data.get("started_at")
            if isinstance(started_at, str):
                started_at = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
            completed_at = run_data.get("completed_at")
            if isinstance(completed_at, str):
                completed_at = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))

            model = IngestRunModel(
                id=run_data["id"],
                source=run_data.get("source", "file"),
                file=run_data.get("file"),
                started_at=started_at or datetime.now(timezone.utc),
                completed_at=completed_at,
                rows_in=run_data.get("rows_in", 0),
                rows_out=run_data.get("rows_out", 0),
                rows_rejected=run_data.get("rows_rejected", 0),
                status=run_data.get("status", "completed"),
                data_mode=run_data.get("data_mode", "demo"),
                details_json=details_str,
            )
            session.merge(model)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_ingest_runs(self, limit: int = 10) -> List[Dict[str, Any]]:
        session = self.SessionLocal()
        try:
            runs = session.query(IngestRunModel).order_by(desc(IngestRunModel.started_at)).limit(limit).all()
            return [r.to_dict() for r in runs]
        finally:
            session.close()

    def save_chat_log(self, log_data: Dict[str, Any]) -> None:
        session = self.SessionLocal()
        try:
            tools_str = json.dumps(log_data.get("tools_used", []))
            created_at = log_data.get("created_at")
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

            log = ChatLogModel(
                id=log_data["id"],
                session_id=log_data.get("session_id"),
                niche_id=log_data.get("niche_id"),
                question=log_data["question"],
                answer=log_data["answer"],
                tools_used_json=tools_str,
                mode=log_data.get("mode", "demo"),
                created_at=created_at or datetime.now(timezone.utc),
            )
            session.add(log)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_chat_logs(
        self, session_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        session = self.SessionLocal()
        try:
            query = session.query(ChatLogModel)
            if session_id:
                query = query.filter(ChatLogModel.session_id == session_id)
            rows = query.order_by(desc(ChatLogModel.created_at)).limit(limit).all()
            return [r.to_dict() for r in rows]
        finally:
            session.close()
