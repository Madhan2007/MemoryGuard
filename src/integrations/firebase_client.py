import os
import json
import logging
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
import firebase_admin
from firebase_admin import credentials, firestore, auth

logger = logging.getLogger(__name__)


class FirebaseSettings(BaseSettings):
    FIREBASE_API_KEY: str = ""
    FIREBASE_AUTH_DOMAIN: str = ""
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""
    FIREBASE_MESSAGING_SENDER_ID: str = ""
    FIREBASE_APP_ID: str = ""

    FIREBASE_ADMIN_TYPE: str = ""
    FIREBASE_ADMIN_PROJECT_ID: str = ""
    FIREBASE_ADMIN_PRIVATE_KEY_ID: str = ""
    FIREBASE_ADMIN_PRIVATE_KEY: str = ""
    FIREBASE_ADMIN_CLIENT_EMAIL: str = ""
    FIREBASE_ADMIN_CLIENT_ID: str = ""
    FIREBASE_ADMIN_AUTH_URI: str = ""
    FIREBASE_ADMIN_TOKEN_URI: str = ""
    FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL: str = ""
    FIREBASE_ADMIN_CLIENT_X509_CERT_URL: str = ""

    # Service account file path
    FIREBASE_SERVICE_ACCOUNT_PATH: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


firebase_settings = FirebaseSettings()


def _build_admin_cred() -> Optional[credentials.Certificate]:
    """Build Firebase Admin credentials from service account file or env vars."""
    
    # Try service account file path first
    if firebase_settings.FIREBASE_SERVICE_ACCOUNT_PATH:
        path = firebase_settings.FIREBASE_SERVICE_ACCOUNT_PATH
        if os.path.exists(path):
            try:
                logger.info(f"Loading Firebase credentials from: {path}")
                return credentials.Certificate(path)
            except Exception as e:
                logger.error(f"Failed to load Firebase credentials from file: {e}")
        else:
            logger.warning(f"Firebase service account file not found: {path}")
    
    # Fallback to individual env vars
    try:
        required = [
            "FIREBASE_ADMIN_TYPE",
            "FIREBASE_ADMIN_PROJECT_ID",
            "FIREBASE_ADMIN_PRIVATE_KEY_ID",
            "FIREBASE_ADMIN_PRIVATE_KEY",
            "FIREBASE_ADMIN_CLIENT_EMAIL",
        ]
        
        for field in required:
            if not getattr(firebase_settings, field, ""):
                logger.warning(f"Firebase Admin field missing: {field}")
                return None

        private_key = firebase_settings.FIREBASE_ADMIN_PRIVATE_KEY.replace("\\n", "\n")
        
        cred_dict = {
            "type": firebase_settings.FIREBASE_ADMIN_TYPE,
            "project_id": firebase_settings.FIREBASE_ADMIN_PROJECT_ID,
            "private_key_id": firebase_settings.FIREBASE_ADMIN_PRIVATE_KEY_ID,
            "private_key": private_key,
            "client_email": firebase_settings.FIREBASE_ADMIN_CLIENT_EMAIL,
            "client_id": firebase_settings.FIREBASE_ADMIN_CLIENT_ID,
            "auth_uri": firebase_settings.FIREBASE_ADMIN_AUTH_URI,
            "token_uri": firebase_settings.FIREBASE_ADMIN_TOKEN_URI,
            "auth_provider_x509_cert_url": firebase_settings.FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": firebase_settings.FIREBASE_ADMIN_CLIENT_X509_CERT_URL,
        }
        
        return credentials.Certificate(cred_dict)
    except Exception as e:
        logger.error(f"Failed to build Firebase Admin credentials: {e}")
        return None


def init_firebase() -> bool:
    """Initialize Firebase Admin SDK. Returns True if successful."""
    try:
        if firebase_admin._apps:
            logger.info("Firebase already initialized")
            return True
        
        cred = _build_admin_cred()
        if not cred:
            logger.warning("Firebase Admin credentials not configured, running without Firebase")
            return False
        
        firebase_admin.initialize_app(cred, {
            'projectId': firebase_settings.FIREBASE_ADMIN_PROJECT_ID or firebase_settings.FIREBASE_PROJECT_ID,
        })
        logger.info("Firebase Admin SDK initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        return False


def get_firestore_client():
    """Get Firestore client instance."""
    try:
        return firestore.client()
    except Exception as e:
        logger.error(f"Failed to get Firestore client: {e}")
        return None


# Initialize on import
_firebase_initialized = init_firebase()

# Export for use in other modules
firestore_client = get_firestore_client() if _firebase_initialized else None