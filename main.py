from typing import Optional,List
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
    

@app.post('/create_user',description='Créer utilisateur (s\'il n\'existe pas)')
def create_user(user:schemas.UtilisateurBase,db: Session=Depends(get_db)):
    #Check if the user exist or no
    new_user=db.query(models.Utilisateur).filter(models.Utilisateur.email==user.email).first()
    if(new_user!=None):#User already exists
        return new_user
    new_user=models.Utilisateur(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post('/create_annonce',description='Créer annonce')
def create_annonce(annonce:schemas.AnnonceBase,db: Session=Depends(get_db)):
    #check if the user exist or no
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==annonce.utilisateur_id).first()
    if(user==None):#User doesn't exist
        return None
    new_annonce=models.Annonce(**annonce.dict())
    db.add(new_annonce)
    db.commit()
    db.refresh(new_annonce)
    return new_annonce


@app.get('/get_personal_annonce',description='Consulter les annonces déposées')
def get_annonce(id_utilisateur:int,db: Session=Depends(get_db)):
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==id_utilisateur).first()
    if(user==None):
        return None
    annonce=db.query(models.Annonce).filter(models.Annonce.utilisateur_id==id_utilisateur).all()
    return annonce


@app.get('/get_message',description='Consulter les messages reçus')
def get_message(id_utilisateur:int,db:Session=Depends(get_db)):
    #Pour récupérer tous les annonces.
    annonce_table=get_annonce(id_utilisateur=id_utilisateur,db=db)
    message=[]
    if(annonce_table==None or len(annonce_table)==0):
        return annonce_table
    for annonce in annonce_table:
        msg=db.query(models.Messages).filter(models.Messages.annonce_id==annonce.id).all()
        if(msg!=None and len(msg)>0):
            message.append(msg)
    return message





    
    

    
    

