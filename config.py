from cryptography.fernet import Fernet

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ids.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret123'
    # مفتاح Fernet ثابت (Base64، 32 بايت)
    ENCRYPTION_KEY = b'3v_7bZx1qK6u4H6fDfMthwTz4lA6Wx5s2vR4vZ-0X0A='