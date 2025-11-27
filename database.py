from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 1. On récupère les variables EXACTEMENT comme dans ta capture d'écran Azure
# Azure App Service "Environment Variables"
SERVER = os.getenv("DB_HOST")      # ex: aztravel-db...
DATABASE = os.getenv("DB_NAME")    # ex: postgres
USERNAME = os.getenv("DB_USER")    # ex: zaydadmin
PASSWORD = os.getenv("DB_PASS")    # Ton mot de passe

# 2. Vérification : Si les variables existent, on est sur Azure (Prod)
if SERVER and DATABASE and USERNAME and PASSWORD:
    # URL pour PostgreSQL (protocole: postgresql)
    # Format: postgresql://user:password@host/dbname
    SQLALCHEMY_DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"
    
    # Azure Postgres demande souvent le SSL ("require")
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"sslmode": "require"}
    )
    print(f"--> Connexion Azure PostgreSQL configurée sur : {SERVER}")

else:
    # 3. Mode développement local (SQLite)
    # Cela s'activera si tu lances le code sur ton PC sans définir les variables DB_...
    print("--> Variables Azure 'DB_HOST' non trouvées. Mode Local SQLite activé.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./travel.db"
    
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
