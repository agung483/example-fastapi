from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
#from sqlalchemy import func

from sqlalchemy.sql.functions import func



router = APIRouter(
    prefix='/pesans',
    tags=['Pesan']
)

@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0):
    
    posttransaksi = db.query(models.Transaksi).join(
        models.DetTransaksi, models.Transaksi.id == models.DetTransaksi.id, isouter=True).join(
        models.User, models.Transaksi.owner_id== models.User.id, isouter=True).group_by(models.Transaksi.id).limit(limit).offset(skip).all()
    
    return posttransaksi

#@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.TransaksiLengkap)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaksis(pesan: schemas.TransaksiCreate,det_pesans: list[schemas.DetTransaksiCreate], db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    existing_pesan = db.query(models.Transaksi).filter(models.Transaksi.no_meja == pesan.no_meja,models.Transaksi.nama_pemesan == pesan.nama_pemesan).first()
    if existing_pesan:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Pesan {existing_pesan.id} already exist in database")
    new_pesan = models.Transaksi(owner_id = current_user.id, **pesan.dict())
    db.add(new_pesan)
    db.commit()
    db.refresh(new_pesan)
    list_det_pesan=[]
    for det_pesan in det_pesans:
        det_pesan = models.DetTransaksi(transaksi_id= new_pesan.id, **det_pesan.dict())
        list_det_pesan.append(det_pesan)
        db.add(det_pesan)
    db.commit()
    db.close()
    
    #return  schemas.TransaksiLengkap(new_pesan)
    return "success"