import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/beautyshop')
    SQLALCHEMY_TRACK_MODIFICATIONS = False