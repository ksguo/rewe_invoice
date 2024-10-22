from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class SupermarketChain(Base):
    __tablename__ = "supermarket_chains"
    chain_id = Column(Integer, primary_key=True)
    chain_name = Column(String)
    chain_shortname = Column(String)
    chain_api_type = Column(Integer)
    chain_api_endpoint = Column(Text)
    chain_created = Column(DateTime)


class SupermarketBranch(Base):
    __tablename__ = "supermarket_branches"
    branch_id = Column(Integer, primary_key=True)
    chain_id = Column(Integer, ForeignKey("supermarket_chains.chain_id"))
    branch_chaininternal_id = Column(Integer)
    branch_name = Column(String)
    branch_street = Column(String)
    branch_plz = Column(String)
    branch_ort = Column(String)
    branch_more = Column(Text)
    branch_specific = Column(Text)
    branch_created = Column(DateTime)
    branch_tel = Column(String)
    branch_uid_number = Column(String)  # uid number
    chain = relationship("SupermarketChain")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    paymentmethod_id = Column(Integer, primary_key=True)
    paymentmethod_name = Column(String)
    paymentmetod_subtype = Column(
        Integer, ForeignKey("payment_methods.paymentmethod_id")
    )


class Brand(Base):
    __tablename__ = "brands"
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)
    brand_noname = Column(Boolean)
    chain_id = Column(Integer, ForeignKey("supermarket_chains.chain_id"))
    brand_created = Column(DateTime)
    brand_modified = Column(DateTime)
    chain = relationship("SupermarketChain")


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    user_email = Column(String, unique=True)
    user_password = Column(String(255))
    user_created = Column(DateTime, default=func.now())  # Set default

    analyses = relationship("UserAnalysis", back_populates="user")


class Purchase(Base):
    __tablename__ = "purchases"
    purchase_id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey("supermarket_branches.branch_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    purchase_sum = Column(Float)
    purchase_time = Column(DateTime)
    paymentmethod_id = Column(Integer, ForeignKey("payment_methods.paymentmethod_id"))
    purchase_used_discount_type = Column(String)
    receipt_nr = Column(String)
    document_nr = Column(String)
    trace_nr = Column(String)
    purchase_processed = Column(DateTime)
    purchase_created = Column(DateTime, default=func.now())
    file_name = Column(String)
    file_path = Column(String)
    cashier_number = Column(String)  # bediner
    register_number = Column(String)  # kasse


class PurchasedProduct(Base):
    __tablename__ = "purchased_products"
    purchased_product_id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey("purchases.purchase_id"))
    purchased_product_price = Column(Float)
    purchased_product_qty = Column(Integer)
    purchased_procuct_includeddiscount = Column(Float)
    purchased_procuct_processed = Column(DateTime)
    purchased_product_name = Column(String)
    purchase = relationship("Purchase")


class UserAnalysis(Base):
    __tablename__ = "user_analysis"
    analysis_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    analysis_type = Column(String(255))
    insights = Column(Text)
    analysis_date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="analyses")
