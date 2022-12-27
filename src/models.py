from database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey,DECIMAL
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Utilisateur(Base):
    __tablename__ = "Utilisateurs"
    id = Column(Integer, primary_key=True)
    email = Column(String(30), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    nom = Column(String(30), nullable=False)
    prenom = Column(String(30), nullable=False)
    tel = Column(String(30), nullable=False)
    adresse = Column(Text, nullable=False)
    token = Column(Text, nullable=False)

class Annonce(Base):
    __tablename__ = "Annonces"
    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey("Utilisateurs.id"))
    titre = Column(Text)
    description = Column(Text)
    categorie = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    surface = Column(DECIMAL, nullable=False)
    prix = Column(DECIMAL, nullable=False)
    wilaya = Column(Integer, nullable=False)
    commune = Column(String(30), nullable=False)
    adresse = Column(String(30), nullable=False)
    photos = Column(Text, nullable=False)
    datePub = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Favoris(Base):
    __tablename__ = "AnnoncesFav_Utilisateurs"
    id = Column(Integer, primary_key=True)
    annonce_id = Column(Integer, ForeignKey("Annonces.id"))
    utilisateur_id = Column(Integer, ForeignKey("Utilisateurs.id"))

class Messages(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True)
    annonce_id = Column(Integer, ForeignKey("Annonces.id"))
    utilisateur_id = Column(Integer, ForeignKey("Utilisateurs.id"))
    body = Column(Text, nullable=False)
    dateEnvoi = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
