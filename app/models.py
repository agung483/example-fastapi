from sqlalchemy import Column, Integer, Float ,String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False) 
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False) 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    post = relationship("Post")
    voter = relationship("User")

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, nullable=False) 
    nama = Column(String, nullable=False, unique=True)
    harga = Column(Float, nullable=False)
    stok = Column(Integer, nullable=False)
    kelompok_id = Column(Integer, ForeignKey(
        "kelmenus.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    kelompok = relationship("KelMenu")
    owner = relationship("User")

class KelMenu(Base):
    __tablename__ = "kelmenus"
    id = Column(Integer, primary_key=True, nullable=False) 
    kelompok = Column(String, nullable=False, unique=True)
    no_urut = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner = relationship("User")


class Transaksi(Base):
    __tablename__ = "transaksis"
    id = Column(Integer, primary_key=True, nullable=False) 
    no_meja = Column(Integer, nullable=True)
    nama_pemesan = Column(String, nullable=True)
    discount = Column(Float,server_default="0", nullable=False)
    status_bayar = Column(Boolean,server_default="FALSE", nullable=False)
    status_kirim = Column(Boolean,server_default="FALSE", nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner = relationship("User")

class DetTransaksi(Base):
    __tablename__ = "dettransaksis"
    id = Column(Integer, primary_key=True, nullable=False) 
    transaksi_id = Column(Integer, ForeignKey("transaksis.id", ondelete="CASCADE"), nullable=False) 
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False)
    jumlah = Column(Integer, nullable=False)
    harga = Column(Float, nullable=False)
    status_masak = Column(Boolean,server_default="FALSE", nullable=False)
    catatan = Column(String, nullable=True)
    menu = relationship("Menu")