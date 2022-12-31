from typing import Optional,List
from fastapi import FastAPI,Response,status,Depends ,Path , HTTPException
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





#Crée Utilisateur

@app.post('/create_user')
def create_user(user:schemas.UtilisateurBase,db: Session=Depends(get_db)):
    #Check if the user exist or no
    new_user=db.query(models.Utilisateur).filter(models.Utilisateur.email==user.email).first()
    if(new_user):#User already exists
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user=models.Utilisateur(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Récuperer utilisateur 
@app.get('/get_user')
def get_user(email:str,db: Session=Depends(get_db)):
    #Check if the user exist or no
    new_user=db.query(models.Utilisateur).filter(models.Utilisateur.email==email).first()
    if(new_user):#not found
        raise HTTPException(status_code=404, detail="User not found")
    return new_user


#Créer Annonce

@app.post('/create_annonce')
def create_annonce(annonce:schemas.AnnonceBase,db: Session=Depends(get_db)):
    #check if the  exist or no
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==annonce.utilisateur_id).first()
    if(user==None):#User doesn't exist
        raise HTTPException(status_code=404, detail="User not found")
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
        raise HTTPException(status_code=404, detail="User not found")
    annonce=db.query(models.Annonce).filter(models.Annonce.utilisateur_id==id_utilisateur).all()
    
    if ( annonce == None) :
        raise HTTPException(status_code=405, detail="items not found")
    return annonce

    
    
 

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
        raise HTTPException(status_code=405, detail="items not found")


    

#Supprimer annonce 
@app.delete('/delete_annonce/{annonce_id}')
def delete_annonce(annonce_id : int   , db : Session =Depends(get_db)) :
    if ( db.delete(annonce_id)> 0 ) :
        db.commit()
    else : 
        raise HTTPException(status_code=405, detail="Error when deleting item")




#Filterer les annonces   !!!!  NOT COMPLETED !!!
@app.get('filter_annonces') 
def filter_annonces(*,  categorie: Optional[int] =None,
                        type: Optional[int] =None,
                        surface: Optional[float]= None,
                        prix: Optional[float]= None,
                        wilaya: Optional[int]= None,
                        commune: Optional[str]= None,
                        adresse: Optional[str]= None,
                        photos: Optional[bool] = None) :

    params = locals().copy()
    result=[]
    minLength=0
    for attr in [x for x in params if params[x] is not None]: # avoir l union des annonce qui contiennent ces  valeurs
        queryRes = db.query(models.Annonce).filter(getattr(db_model.Item, attr)==params[attr]).all() ; 
        if (queryRes == None ) : 
            raise HTTPException(status_code=405, detail="items not found")
       
        if (len(result[minLength]) > len(queryRes)) : minLength = len(result)-1
       
        result.append(set(queryRes))     
                       
     #result contient plusieurs sets chaque set  contient les annonces qui ont un certain attribut 
     #on doit faire l'intersection de tous ces sets pour avoir notre resultat 
    filtered = result[minLength]
    
    for an in result : 
        filtered = filtered & an 
        if(len(filtered) == 0 ) :
            raise HTTPException(status_code=405, detail="items not found")
        
    return filtered

         

    
#Récuperer messages recus 
@app.get('/get_message')
def get_message(id_utilisateur:int,db:Session=Depends(get_db)):
    annonce_table=get_mesAnnonces(id_utilisateur=id_utilisateur,db=db)#Pour recuperer tous les annonces 
    message=[]
    if(annonce_table==None or len(annonce_table)==0):
         raise HTTPException(status_code=405, detail="items not found")
    for annonce in annonce_table:
        message.append(db.query(models.Messages).filter(models.Messages.annonce_id==annonce.id).all())
    if (len(message>0)) :    
        return message
    else : raise HTTPException(status_code=406, detail="messages not found")


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

#Web scraping 
    
    
