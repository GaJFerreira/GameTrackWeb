import firebase_admin
from firebase_admin import credentials, firestore
from .config import settings  # <-- MUDANÇA AQUI

cred = credentials.Certificate(settings.firebase_credentials_path)

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

print("Firebase Admin SDK inicializado com sucesso.")
db = firestore.client()