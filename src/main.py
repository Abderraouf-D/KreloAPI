from typing import Optional,List
#€
from fastapi import FastAPI,Response,status,HTTPException,Depends

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
import models,schemas
from database import engine,get_db,Base

app=FastAPI()

Base.metadata.create_all(bind=engine)


""""
@app.get('/results/{name}',status_code=status.HTTP_202_ACCEPTED)
def result(name:str):
    for obj in set:
        if(obj['name']==name):
            return obj
    #response.status_code=status.HTTP_404_NOT_FOUND
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'{name} not found.')
    return {'Data':'Not Found'}

@app.post('/posts-all',response_model=List[schemas.PostResponse])
def get_all(db:Session=Depends(get_db)):
    post=db.query(models.Post).all()
    return post
@app.post('/posts',response_model=schemas.PostResponse)
def create_posts(post:schemas.Post,db: Session=Depends(get_db)):
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
@app.get('/posts/{id}')
def get_posts(id:int,db: Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    return post
@app.delete('/posts/{id}')
def del_posts(id:int,db: Session=Depends(get_db)):
    db.query(models.Post).filter(models.Post.id==id).delete(synchronize_session=False)
    db.commit()
@app.put('/posts/{id}')
def upd_posts(post:schemas.Post,id:int,db: Session=Depends(get_db)):
    db.query(models.Post).filter(models.Post.id==id).update(post.dict(),synchronize_session=False)
    db.commit()"""



@app.post('/create_user')
def create_user(user:schemas.UtilisateurBase,db: Session=Depends(get_db)):
    #Check if the user exist or no
    new_user=db.query(models.Utilisateur).filter(models.Utilisateur.email==user.email).first()
    print(new_user)
    new_user=models.Utilisateur(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@app.get('get_user')
def get_user(user:schemas.UtilisateurBase,db: Session=Depends(get_db)):
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==id).first()
