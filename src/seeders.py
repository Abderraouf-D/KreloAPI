import schemas
import models
from database import get_db , Base ,engine , SessionLocal

Base.metadata.create_all(bind=engine)
db = SessionLocal()



def seedAll(nbUsers , anPerUser , msgPerListing):
    for  u in range(nbUsers) : 
        #create user 
            try :
                user = schemas.UtilisateurBase(
                    is_admin=False , 
                    email = f"user{u}@gmail.com",
                    nom = f"nom {u}",
                    prenom = f"prenom {u}",
                    tel='0'+str(u)*9,
                    adresse='This is an adress'
                )
                userDB = models.Utilisateur(**user.dict())
                db.add(userDB)
                db.commit()
                db.refresh(userDB)

                addeduser = userDB.id

                for a in range(anPerUser) :
                    #create annonce
                    annonce  = schemas.AnnonceBase(
                    utilisateur_id= 1  ,
                    titre= "This is a titles"    ,
                    description= "Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum ." ,
                    categorie= 1  , 
                    type= 1 , 
                    surface= 80 , 
                    commune= "This is a city" ,
                    adresse =  "This is an adresse",
                    prix = 700000 , 
                    wilaya= 17 , 
                    photos= "test1.jpeg;test2.jpeg;test3.jpeg", 
                    isScraped=False 
                    )
                    annonceDB = models.Annonce(**annonce.dict())
                    db.add(annonceDB)
                    db.commit()
                    db.refresh(annonceDB)

                    addedlisting = annonceDB.id
                    if ( u>0) :
                        for m in range(msgPerListing) :
                            #create message 
                            message = schemas.MessageBase(
                                body="Hello I want this item !\n"+"test"*15
                            )
                            messageDB = models.Messages(**message.dict())
            
                            messageDB.annonce_id = addedlisting
                            messageDB.utilisateur_id = addeduser -1 
                            db.add(messageDB)
                            db.commit()
            except Exception as e :
                 print(e)
                 




u = int(input("Enter number of Users : "))
a = int(input("Enter number of listings per user  : "))
m = int(input("Enter number of messages per listing : "))

seedAll(u,a,m)
db.close()