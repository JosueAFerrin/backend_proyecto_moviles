import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

cred = credentials.Certificate("secrets/firebase-key.json")
firebase_admin.initialize_app(cred)
