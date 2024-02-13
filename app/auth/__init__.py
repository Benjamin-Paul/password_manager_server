import os
from dotenv import load_dotenv
from app import app

load_dotenv(".env")
app.jwt_signing_key = os.environ["JWT_KEY"]
app.zk_password = os.environ["ZERO_KNOWLEDGE_PASSWORD"]