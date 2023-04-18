from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

#use Pydantic
class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] 
    created_at: datetime
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    owner: UserOut
    created_at: datetime
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class PostVote(BaseModel):
    Post: Post
    votes: int
    

class UserLogin(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class KelMenuCreate(BaseModel):
    kelompok: str
    no_urut: int

class KelMenu(BaseModel):
    id: int
    kelompok: str
    no_urut: int
    owner_id: int
    owner: UserOut
    created_at: datetime
    class Config:
        orm_mode = True

class MenuCreate(BaseModel):
    nama: str
    harga: int
    stok: int 
    kelompok_id: int

class MenuTampil(BaseModel):
    id: int
    nama: str
    harga: int

class Menu(BaseModel):
    id: int
    nama: str
    harga: int
    stok: int
    kelompok_id: int
    owner_id: int
    owner: UserOut
    kelompok: KelMenu
    created_at: datetime
    class Config:
        orm_mode = True

class VoteCreate(BaseModel):
    post_id: int
    vote_dir: conint(le=1)

class Vote(BaseModel):
    user_id: int
    post_id: int
    post: Post
    voter: UserOut
    created_at: datetime
    class Config:
        orm_mode = True

class DetTransaksiCreate(BaseModel):
    menu_id: int
    jumlah: int
    harga: float
    catatan: Optional[str] = None

class DetTransaksi(BaseModel):
    transaksi_id: int
    menu_id: int
    menu: MenuTampil
    jumlah: int
    harga: float
    status_masak: bool
    catatan: Optional[str] = ''
    class Config:
        orm_mode = True

class TransaksiCreate(BaseModel):
    no_meja: int 
    nama_pemesan: str
    discount: float
    status_bayar:  bool
    status_kirim: bool

class Transaksi(BaseModel):
    id: int
    no_meja: int 
    nama_pemesan: str
    discount: float
    status_bayar: bool
    status_kirim: bool
    owner_id: int
    owner: UserOut
    created_at: datetime
    class Config:
        orm_mode = True

class TransaksiLengkap(BaseModel):
    id: int
    no_meja: int
    nama_pemesan: str
    discount: float
    status_bayar: bool
    status_kirim: bool
    list_det_transaksi: list[DetTransaksi]
    owner_id: int
    owner: UserOut
    created_at: datetime
    class Config:
        orm_mode = True