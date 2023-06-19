from dotenv import load_dotenv
import os
FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_APP = os.getenv("FLASK_APP")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")
FLASK_RELOAD = os.getenv("FLASK_RELOAD")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
load_dotenv()
