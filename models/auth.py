#!/usr/bin/python3
"""
Module for Google Auth
"""
from os import getenv


class Auth:
    """
    Class for storing information about authenticating
    """
    CLIENT_ID = getenv('CLIENT_ID')
    CLIENT_SECRET = getenv('CLIENT_SECRET')
    REDIRECT_URI = 'https://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']
    SECRET_KEY = getenv("SECRET_KEY")
