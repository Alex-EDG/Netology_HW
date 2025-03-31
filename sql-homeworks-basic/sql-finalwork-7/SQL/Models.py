import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users(Base):
    """
    Tablename: **users** \n
    Column: **id** SERIAL PRIMARY KEY,\n
	**name** VARCHAR(64) NOT NULL UNIQUE CHECK(name !='')
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=64), db.CheckConstraint("name != ''"), nullable=False, unique=True)

class Words(Base):
    """
    Tablename: **words**\n
    Column: **id** SERIAL PRIMARY KEY,\n
	**ru_word** VARCHAR(64) NOT NULL UNIQUE CHECK(ru_word !=''),\n
	**en1_word** VARCHAR(64) NOT NULL CHECK(en1_word !=''),\n
	**en2_word** VARCHAR(64) CHECK(en2_word !='')
    """
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ru_word = db.Column(db.String(length=64), db.CheckConstraint("ru_word != ''"), nullable=False, unique=True)
    en1_word = db.Column(db.String(length=64), db.CheckConstraint("en1_word != ''"), nullable=False)
    en2_word = db.Column(db.String(length=64), db.CheckConstraint("en2_word != ''"))

class UsersWords(Base):
    """
    Tablename: **words** \n
    Column: **id** SERIAL PRIMARY KEY,\n
	**id_user** INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,\n
	**id_word** INTEGER NOT NULL REFERENCES words (id) ON DELETE CASCADE
    """
    __tablename__ = "users_words"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_word = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)

    users = relationship(Users, backref="users_words")
    words = relationship(Words, backref="users_words")

def create_tables(engine):

    Base.metadata.create_all(engine)