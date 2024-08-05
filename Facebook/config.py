import os

class Config:
    FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL', 'email@example.com')
    FACEBOOK_PASSWORD = os.getenv('FACEBOOK_PASSWORD', 'password')
