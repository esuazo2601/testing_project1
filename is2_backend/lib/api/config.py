from dotenv import load_dotenv
import os

load_dotenv()

class ApplicationConfig:
    SQLALCHEMY_TACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO = True