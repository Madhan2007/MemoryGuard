import os
import logging
from typing import Optional, Dict, Any
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import firestore

logger = logging.getLogger(__name__)


class FirebaseAuthService:
    """Firebase Authentication service for user management."""
    
    def __init__(self):
        self._initialized = False
    
    def _ensure_initialized(self):
        """Check if Firebase is initialized."""
        self._initialized = bool(firebase_admin._apps)
        return self._initialized
    
    def is_configured(self) -> bool:
        return self._ensure_initialized()
    
    async def create_user(self, email: str, password: str, display_name: str = "") -> Dict[str, Any]:
        """Create a new user with email/password."""
        if not self._ensure_initialized():
            return {"success": False, "error": "Firebase not configured"}
        
        try:
            user = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=display_name,
                email_verified=False
            )
            
            # Create user profile in Firestore
            db = firestore.client()
            user_data = {
                "uid": user.uid,
                "email": email,
                "display_name": display_name,
                "role": "rep",
                "created_at": firestore.SERVER_TIMESTAMP,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }
            db.collection("users").document(user.uid).set(user_data)
            
            logger.info(f"Created user: {user.uid} ({email})")
            return {
                "success": True,
                "uid": user.uid,
                "email": email,
                "display_name": display_name
            }
        except firebase_auth.EmailAlreadyExistsError:
            return {"success": False, "error": "Email already registered"}
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return {"success": False, "error": str(e)}
    
    async def sign_in_user(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in user with email/password (returns custom token for client SDK)."""
        if not self._ensure_initialized():
            return {"success": False, "error": "Firebase not configured"}
        
        try:
            # Get user by email to verify they exist
            user = firebase_auth.get_user_by_email(email)
            
            # Create custom token for client-side sign-in
            custom_token = firebase_auth.create_custom_token(user.uid)
            
            # Get user profile from Firestore
            db = firestore.client()
            user_doc = db.collection("users").document(user.uid).get()
            profile = user_doc.to_dict() if user_doc.exists else {}
            
            return {
                "success": True,
                "custom_token": custom_token.decode() if isinstance(custom_token, bytes) else custom_token,
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name or "",
                "profile": profile
            }
        except firebase_auth.UserNotFoundError:
            return {"success": False, "error": "User not found"}
        except Exception as e:
            logger.error(f"Sign in failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def verify_token(self, id_token: str) -> Dict[str, Any]:
        """Verify Firebase ID token."""
        if not self._ensure_initialized():
            return {"success": False, "error": "Firebase not configured"}
        
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            return {"success": True, "decoded_token": decoded_token}
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return {"success": False, "error": "Invalid token"}
    
    async def get_user_profile(self, uid: str) -> Dict[str, Any]:
        """Get user profile from Firestore."""
        if not self._ensure_initialized():
            return {"success": False, "error": "Firebase not configured"}
        
        try:
            db = firestore.client()
            user_doc = db.collection("users").document(uid).get()
            if user_doc.exists:
                return {"success": True, "profile": user_doc.to_dict()}
            return {"success": False, "error": "Profile not found"}
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_user_profile(self, uid: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile in Firestore."""
        if not self._ensure_initialized():
            return {"success": False, "error": "Firebase not configured"}
        
        try:
            db = firestore.client()
            data["updated_at"] = firestore.SERVER_TIMESTAMP
            db.collection("users").document(uid).update(data)
            return {"success": True}
        except Exception as e:
            logger.error(f"Failed to update profile: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_user(self, uid: str) -> Dict[str, Any]:
        """Delete user from Auth and Firestore."""
        if not self._ensure_initialized():
            return {"success": False, "error": "Firebase not configured"}
        
        try:
            firebase_auth.delete_user(uid)
            db = firestore.client()
            db.collection("users").document(uid).delete()
            return {"success": True}
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            return {"success": False, "error": str(e)}


class FirestoreService:
    """Firestore service for teams, deals, and other data."""
    
    def __init__(self):
        self._initialized = False
    
    def _ensure_initialized(self):
        """Check if Firebase is initialized."""
        self._initialized = bool(firebase_admin._apps)
        return self._initialized
    
    def is_configured(self) -> bool:
        return self._ensure_initialized()
    
    def _get_db(self):
        """Get Firestore client lazily."""
        if not self._ensure_initialized():
            return None
        try:
            return firestore.client()
        except Exception as e:
            logger.error(f"Failed to get Firestore client: {e}")
            return None
    
    # Team operations
    async def create_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "Firestore not configured"}
        
        try:
            db = self._get_db()
            if not db:
                return {"success": False, "error": "Firestore client not available"}
            
            team_data["created_at"] = firestore.SERVER_TIMESTAMP
            team_data["updated_at"] = firestore.SERVER_TIMESTAMP
            team_data["member_uids"] = team_data.get("member_uids", [])
            
            doc_ref = db.collection("teams").document()
            doc_ref.set(team_data)
            
            return {"success": True, "team_id": doc_ref.id, "data": team_data}
        except Exception as e:
            logger.error(f"Failed to create team: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_team(self, team_id: str) -> Dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "Firestore not configured"}
        
        try:
            db = self._get_db()
            if not db:
                return {"success": False, "error": "Firestore client not available"}
            
            doc = db.collection("teams").document(team_id).get()
            if doc.exists:
                return {"success": True, "team_id": doc.id, "data": doc.to_dict()}
            return {"success": False, "error": "Team not found"}
        except Exception as e:
            logger.error(f"Failed to get team: {e}")
            return {"success": False, "error": str(e)}
    
    async def add_user_to_team(self, team_id: str, uid: str, role: str = "member") -> Dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "Firestore not configured"}
        
        try:
            db = self._get_db()
            if not db:
                return {"success": False, "error": "Firestore client not available"}
            
            team_ref = db.collection("teams").document(team_id)
            team_ref.update({
                "member_uids": firestore.ArrayUnion([uid]),
                "updated_at": firestore.SERVER_TIMESTAMP,
            })
            
            # Also update user's team list
            user_ref = db.collection("users").document(uid)
            user_ref.update({
                "team_ids": firestore.ArrayUnion([team_id]),
                "updated_at": firestore.SERVER_TIMESTAMP,
            })
            
            return {"success": True}
        except Exception as e:
            logger.error(f"Failed to add user to team: {e}")
            return {"success": False, "error": str(e)}
    
    # Deal operations
    async def create_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "Firestore not configured"}
        
        try:
            db = self._get_db()
            if not db:
                return {"success": False, "error": "Firestore client not available"}
            
            deal_data["created_at"] = firestore.SERVER_TIMESTAMP
            deal_data["updated_at"] = firestore.SERVER_TIMESTAMP
            deal_data["hindsight_bank"] = f"memoryguard-project-{deal_data.get('deal_id', '')}"
            
            doc_ref = db.collection("deals").document()
            doc_ref.set(deal_data)
            
            return {"success": True, "deal_id": doc_ref.id, "data": deal_data}
        except Exception as e:
            logger.error(f"Failed to create deal: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_deal(self, deal_id: str) -> Dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "Firestore not configured"}
        
        try:
            db = self._get_db()
            if not db:
                return {"success": False, "error": "Firestore client not available"}
            
            doc = db.collection("deals").document(deal_id).get()
            if doc.exists:
                return {"success": True, "deal_id": doc.id, "data": doc.to_dict()}
            return {"success": False, "error": "Deal not found"}
        except Exception as e:
            logger.error(f"Failed to get deal: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user_deals(self, uid: str) -> Dict[str, Any]:
        """Get all deals for a user (via team membership)."""
        if not self.is_configured():
            return {"success": False, "error": "Firestore not configured"}
        
        try:
            db = self._get_db()
            if not db:
                return {"success": False, "error": "Firestore client not available"}
            
            # Get user's teams
            user_doc = db.collection("users").document(uid).get()
            if not user_doc.exists:
                return {"success": True, "deals": []}
            
            user_data = user_doc.to_dict()
            team_ids = user_data.get("team_ids", [])
            
            if not team_ids:
                return {"success": True, "deals": []}
            
            # Get deals for user's teams
            deals = []
            for team_id in team_ids:
                deals_query = db.collection("deals").where("team_id", "==", team_id).stream()
                for deal_doc in deals_query:
                    deals.append({"deal_id": deal_doc.id, **deal_doc.to_dict()})
            
            return {"success": True, "deals": deals}
        except Exception as e:
            logger.error(f"Failed to get user deals: {e}")
            return {"success": False, "error": str(e)}
    
    async def update_deal(self, deal_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "Firestore not configured"}
        
        try:
            db = self._get_db()
            if not db:
                return {"success": False, "error": "Firestore client not available"}
            
            data["updated_at"] = firestore.SERVER_TIMESTAMP
            db.collection("deals").document(deal_id).update(data)
            return {"success": True}
        except Exception as e:
            logger.error(f"Failed to update deal: {e}")
            return {"success": False, "error": str(e)}


# Lazy-initialized singletons
_firebase_auth_service = None
_firestore_service = None


def get_firebase_auth_service() -> FirebaseAuthService:
    """Get or create FirebaseAuthService singleton."""
    global _firebase_auth_service
    if _firebase_auth_service is None:
        _firebase_auth_service = FirebaseAuthService()
    return _firebase_auth_service


def get_firestore_service() -> FirestoreService:
    """Get or create FirestoreService singleton."""
    global _firestore_service
    if _firestore_service is None:
        _firestore_service = FirestoreService()
    return _firestore_service


# Backward compatibility
firebase_auth_service = get_firebase_auth_service()
firestore_service = get_firestore_service()