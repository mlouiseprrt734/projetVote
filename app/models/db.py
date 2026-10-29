
import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

# Charge le .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"))

# Fonction connexion basique à la base de données PostgreSQL
def get_connection():
    
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "prefer"),
        connect_timeout=5,
        row_factory=dict_row,
    )

# Test de la connexion à la base de données
# python -m app.models.db 
if __name__ == "__main__":
    try:
        with get_connection() as conn:
            info = conn.execute(
                "SELECT version() AS version, current_database() AS db, current_user AS usr"
            ).fetchone()
            tables = [r["table_name"] for r in conn.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' ORDER BY table_name"
            ).fetchall()]
        print("Connexion OK")
        print("  Serveur     :", info["version"])
        print("  Base        :", info["db"])
        print("  Utilisateur :", info["usr"])
        print("  Tables      :", ", ".join(tables) or "aucune")
    except Exception as e:
        print("Échec de la connexion :", e)
