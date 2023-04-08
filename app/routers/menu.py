from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/menus',
    tags=['Menus']
)

@router.get("/",response_model=List[schemas.Menu])
def get_menus(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user)):
    menus = db.query(models.Menu).all()
    return menus

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Menu)
def create_menus(menu: schemas.MenuCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    #new_menu = models.Menu(**menu.dict())
    #new_menu.owner_id = current_user.id
    existing_menu = db.query(models.Menu).filter(models.Menu.nama == menu.nama).first()
    if existing_menu:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Menu {menu.nama} already exist in database")
    new_menu = models.Menu(owner_id = current_user.id, **menu.dict())
    db.add(new_menu)
    db.commit()           
    db.refresh(new_menu)
    return new_menu

@router.get("/{id}", response_model=schemas.Menu)
def get_menu(id: int, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    menu = db.query(models.Menu).filter(models.Menu.id==id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"menu with id: {id} was not found")

    return menu

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    menu_query = db.query(models.Menu).filter(models.Menu.id==id)
    menu = menu_query.first()
    if menu== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"menu with id {id} does not exist")
    
    if menu.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    menu_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Menu)
def update_menu(id: int, updated_menu: schemas.MenuCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    menu_query = db.query(models.Menu).filter(models.Menu.id==id)
    menu = menu_query.first()
    
    if menu == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"menu with id {id} does not exist")
    
    if menu.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    menu_query.update(updated_menu.dict(), synchronize_session=False)
    db.commit()
    return menu_query.first()