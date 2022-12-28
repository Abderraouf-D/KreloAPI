from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends ,Path
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session 
from sqlalchemy import or_
import models,schemas
from database import engine,get_db,Base
import string
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
    
#Créer/Récuperer Utilisateur

@app.post('/create_user')
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

#Créer Annonce

@app.post('/create_annonce')
def create_annonce(annonce:schemas.AnnonceBase,db: Session=Depends(get_db)):
    #check if the  exist or no
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==annonce.utilisateur_id).first()
    if(user==None):#User doesn't exist
        return None
    new_annonce=models.Annonce(**annonce.dict())
    db.add(new_annonce)
    db.commit()
    db.refresh(new_annonce)
    return new_annonce

#Récuperer les anonnces postés
@app.get('/get_mesAnnonces')
def get_mesAnnonces(id_utilisateur:int,db: Session=Depends(get_db)):
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==id_utilisateur).first()
    if(user==None):
        return None
    annonce=db.query(models.Annonce).filter(models.Annonce.utilisateur_id==id_utilisateur).all()
    return annonce


#Récuperer messages recus 
@app.get('/get_message')
def get_message(id_utilisateur:int,db:Session=Depends(get_db)):
    annonce_table=get_mesAnnonces(id_utilisateur=id_utilisateur,db=db)#Pour recuperer tous les annonces 
    message=[]
    if(annonce_table==None or len(annonce_table)==0):
        return annonce_table
    for annonce in annonce_table:
        message.append(db.query(models.Messages).filter(models.Messages.annonce_id==annonce.id).all())
    return message


#Créer message a envoyer
@app.post('/create_message')
def create_message(id_utilisateur : int , id_annonce : int ,message :schemas.MessageBase,db: Session=Depends(get_db)):
    
    new_message = models.Messages(**message.dict())
 
    new_message.annonce_id = id_annonce
    new_message.utilisateur_id = id_utilisateur
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

    
    
#ToDo 

#Rechercher annonce selon les mots clés 
@app.get('/get_Annonces_ByKeywords' )
def get_Annonces_ByKeywords( keyWords  :str  , db : Session = Depends(get_db)): 
    wordList = set (   keyWords.lower().split(' '))
    annonces = db.query(models.Annonce).all() 
    result =[]

    for an in annonces :  
        if len(wordList & set (  an.titre.lower().split(' ')+an.description.lower().split(' ') ))>0  : 
            result.append(an)
    if  (len(result)> 0) : 
        return result 
    else :
        return None  


    

#Supprimer annonce 
@app.delete('/delete_annonce/{annonce_id}')
def delete_annonce(annonce_id : int   , db : Session =Depends(get_db)) :
    if ( db.delete(annonce_id)> 0 ) :
        db.commit()
        return {"succes" : True}
    else : 
        return {"succes" : False}

    

#Web scraping 
    
    
