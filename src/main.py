import os
from typing import Optional,List
from fastapi import FastAPI,Response,status,Depends ,Path , HTTPException , UploadFile , File
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session 
from sqlalchemy import or_ 
import models,schemas
from database import engine,get_db,Base
import string
from datetime import datetime
import re 
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()


#enabling CORS 

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


#Crée Utilisateur

@app.post('/create_user')
def create_user(user:schemas.UtilisateurBase,db: Session=Depends(get_db)):
    #Check if the user exists or not
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
    #Check if the user exists or no
    new_user=db.query(models.Utilisateur).filter(models.Utilisateur.email==email).first()
    if(new_user is None):#not found
        raise HTTPException(status_code=404, detail="User not found")
    return new_user



#Créer annonce 
@app.post('/create_annonce')
async def create_annonce(annonce : schemas.AnnonceBase,db: Session=Depends(get_db)):
    #check if it exists or no
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==annonce.utilisateur_id).first()
    if(user==None):#User doesn't exist
        raise HTTPException(status_code=404, detail="User not found")
    new_annonce=models.Annonce(**annonce.dict())
    db.add(new_annonce)
    db.commit()
    db.refresh(new_annonce)
    return new_annonce



#Uploader  les images d'une annonce by id
@app.post('/upload_byid')
async def upload_byid(id : int  , files : Optional[list[UploadFile]]=File (...),db: Session=Depends(get_db)):
    #TODO  : Validate file type 
    folder_path= ("uploads")
    annonce = db.query(models.Annonce).filter(models.Annonce.id == id).first()
    if ( annonce == None) :
        raise HTTPException(status_code=405, detail="items not found")

    if not os.path.exists(folder_path):
         os.makedirs(folder_path)

    for i , file in enumerate(files) :  
        tmp = file.filename.split(".")
        file.filename = f"{id}_{i}.{tmp[1]}"
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
    annonce.photos = ';'.join([f.filename for f in files])
    db.commit()

    return {"succes" : True}

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

    
    
 #retourner toutes les annonces  
@app.get('/get_Annonces_all' )
def get_Annonces_all( db : Session = Depends(get_db)): 
    annonces = db.query(models.Annonce).all() 
    if ( annonces == None) :
        raise HTTPException(status_code=405, detail="items not found")
    return annonces

#Rechercher annonce par id  
@app.get('/get_Annonce_byid' )
def get_get_Annonce_byid( id : int , db : Session = Depends(get_db)): 

    annonce = db.query(models.Annonce).filter(models.Annonce.id == id).first()
    if ( annonce == None) :
        raise HTTPException(status_code=405, detail="items not found")
    user=db.query(models.Utilisateur).filter(models.Utilisateur.id==annonce.utilisateur_id).first()
    if(user==None):
        raise HTTPException(status_code=404, detail="User not found")
    annonce.utilisateur_id = user 
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
     annonce=db.query(models.Annonce).filter(models.Annonce.id==annonce_id).first()
     if(annonce!=None):
         db.delete(annonce)
         db.commit()
     else:
         raise HTTPException(status_code=405, detail="items not found")




#Filterer les annonces   
@app.get('/filter_annonces') 
def filter_annonces(*,  type: Optional[int] =None,
                        wilaya: Optional[int]= None,
                        commune: Optional[str]= None,
                        dateMins : Optional[str]=None, 
                        dateMaxs : Optional[str]=None,db :  Session = Depends(get_db)) :
    dateMin = dateMax = None 
 
    if ( dateMins is not None ) : 
        if (not re.match("^\d{4}-\d{2}-\d{2}$", dateMins) ) :
            raise HTTPException(500 , "Please enter the date in the following form : yyyy-mm-dd")
        dateMin = datetime.strptime(dateMins,"%Y-%m-%d").date()
    if ( dateMaxs is not None ) : 
        if ( not re.match("^\d{4}-\d{2}-\d{2}$", dateMaxs) ) : 
            raise HTTPException(500 , "Please enter the date in the following form : yyyy-mm-dd")
        dateMax = datetime.strptime(dateMaxs,"%Y-%m-%d").date()
   
    queryRes= None
    params = locals().copy() 
    result=[]
    minLength=0
   
    for attr in [x for x in params][0:3]: # avoir l union des annonces qui contiennent ces  valeurs
        if ( params[attr] is not None): 
            if ( dateMin == None and dateMax ==  None) : 
                queryRes = db.query(models.Annonce).filter(getattr(models.Annonce, attr)==params[attr]).all() 
            elif ( dateMin == None )  : 
                queryRes = db.query(models.Annonce).filter(getattr(models.Annonce, attr)==params[attr], models.Annonce.datePub >= dateMin).all() 
            elif ( dateMax == None )  : 
                queryRes = db.query(models.Annonce).filter(getattr(models.Annonce, attr)==params[attr], models.Annonce.datePub <= dateMax).all() 
            else :  
                queryRes = db.query(models.Annonce).filter(getattr(models.Annonce, attr)==params[attr], dateMax >= models.Annonce.datePub ,models.Annonce.datePub  >= dateMin).all()
            
            if (queryRes == None or len(queryRes)==0) :  
                raise HTTPException(status_code=406, detail="items not found")
               
            
            result.append(set(queryRes))     
            if (len(result[minLength]) > len(queryRes)) : minLength = len(result)-1
                   
     #result contient plusieurs sets chaque set  contient les annonces qui ont un certain attribut 
     #on doit faire l'intersection de tous ces sets pour avoir notre resultat 
    if( len(result)>0) : 
        filtered = result[minLength]
        for an in result : 
            filtered = filtered & an 
            if(len(filtered) == 0 ) :
                raise HTTPException(status_code=405, detail="items not found")
    else : 
        if ( dateMin == None and dateMax ==  None) : 
            queryRes = None
        elif ( dateMin == None )  : 
                queryRes = db.query(models.Annonce).filter(models.Annonce.datePub >= dateMin).all() 
        elif ( dateMax == None )  : 
                queryRes = db.query(models.Annonce).filter(models.Annonce.datePub <= dateMax).all() 
        else :  
                queryRes = db.query(models.Annonce).filter(dateMax >= models.Annonce.datePub ,models.Annonce.datePub  >= dateMin).all()
        if (queryRes == None or len(queryRes)==0) : 
            raise HTTPException(status_code=406, detail="items not found")
        filtered = set(queryRes)    
            
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



    
