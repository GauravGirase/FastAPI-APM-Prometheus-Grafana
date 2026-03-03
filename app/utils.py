import hashlib
import base64
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_passwd(password: str) -> str:
    hashed = pwd_context.hash(password)
    return hashed

def verify_password(password: str, hashed: str) -> bool:
    sha256_bytes = hashlib.sha256(password.encode("utf-8")).digest()
    safe_str = base64.b64encode(sha256_bytes).decode("utf-8")
    return pwd_context.verify(safe_str, hashed)