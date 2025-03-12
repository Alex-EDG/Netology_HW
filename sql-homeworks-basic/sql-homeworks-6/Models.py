import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=96), db.CheckConstraint("name != ''"), unique=True)

class Shop(Base):
    __tablename__ = "shop"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=96), db.CheckConstraint("name != ''"), unique=True)

class Book(Base):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    id_publisher = db.Column(db.Integer, db.ForeignKey("publisher.id"), nullable=False)
    title = db.Column(db.String(length=128), nullable=False)

    publisher = relationship(Publisher, backref="book")

class Stock(Base):
    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    id_book = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    id_shop = db.Column(db.Integer, db.ForeignKey("shop.id"), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"

    id = db.Column(db.Integer, primary_key=True)
    id_stock = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    date_sale = db.Column(db.DateTime, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    stock = relationship(Stock, backref="sale")

def create_tables(engine):

    Base.metadata.create_all(engine)