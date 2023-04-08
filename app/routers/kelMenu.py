from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/kelmenus',
    tags=['Kelompok menus']
)

@router.get("/",response_model=List[schemas.KelMenu])
def get_kelmenus(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user)):
    kelmenus = db.query(models.KelMenu).all()
    return kelmenus

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.KelMenu)
def create_kelmenus(kelmenu: schemas.KelMenuCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    #new_kelmenu = models.KelMenu(**kelmenu.dict())
    #new_kelmenu.owner_id = current_user.id
    new_kelmenu = models.KelMenu(owner_id = current_user.id, **kelmenu.dict())
    db.add(new_kelmenu)
    db.commit()
    db.refresh(new_kelmenu)
    return new_kelmenu

@router.get("/{id}", response_model=schemas.KelMenu)
def get_kelmenu(id: int, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    kelmenu = db.query(models.KelMenu).filter(models.KelMenu.id==id).first()
    if not kelmenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"kelompok menu with id: {id} was not found")

    return kelmenu

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kelmenu(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    kelmenu_query = db.query(models.KelMenu).filter(models.KelMenu.id==id)
    kelmenu = kelmenu_query.first()

    if kelmenu == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"kelompok menu with id {id} does not exist")
    
    if kelmenu.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    kelmenu_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.KelMenu)
def update_kelmenu(id: int, updated_kelmenu: schemas.KelMenuCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    kelmenu_query = db.query(models.KelMenu).filter(models.KelMenu.id==id)
    kelmenu = kelmenu_query.first()
    
    if kelmenu == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"kelompok menu with id {id} does not exist")
    
    if kelmenu.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    kelmenu_query.update(updated_kelmenu.dict(), synchronize_session=False)
    db.commit()
    return kelmenu_query.first()