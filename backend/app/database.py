import firebase_admin
from firebase_admin import credentials, firestore
from app.config import settings

firebase_app = None
db = None

# Só inicializa Firebase se tiver caminho válido
if settings.firebase_credentials_path:
    try:
        cred = credentials.Certificate(settings.firebase_credentials_path)

        # evita inicialização duplicada
        try:
            firebase_app = firebase_admin.get_app()
        except ValueError:
            firebase_app = firebase_admin.initialize_app(cred)

        db = firestore.client()

        print("Firebase Admin SDK inicializado com sucesso.")

    except Exception as e:
        # Evita crash no pytest / CI
        print(f"Firebase não inicializado: {e}")
else:
    print("Firebase ignorado (settings.firebase_credentials_path vazio).")
