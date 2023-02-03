import schemas
import models
from database import get_db , Base ,engine , SessionLocal

Base.metadata.create_all(bind=engine)
db = SessionLocal()


#you have to put images test1 test2 test3 in .../uploads folder 
def seedAnnonces(numberOfSeeds):
    for i in range(numberOfSeeds):
        annonce  = schemas.AnnonceBase(
        utilisateur_id= 1  ,
        titre= "Lorem ipsum"    ,
        description= "Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum \nLorem ipsum Lorem ipsum ." ,
        categorie= 1  , 
        type= 1 , 
        surface= 80 , 
        commune= 56 ,
        adresse =  "test",
        prix = 700000 , 
        wilaya= 17 , 
        photos= "test1;test2;test3", 
        isScraped=False 
        )
        annonceDB = models.Annonce(**annonce.dict())
        db.add(annonceDB)
        db.commit()
        db.refresh(annonceDB)   
    db.close()


i = int(input("Enter number of Listings : "))
seedAnnonces(i)