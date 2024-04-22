from dotenv import load_dotenv
import os

load_dotenv()
redis_host = os.environ.get("RESIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
redis_username = os.environ.get("REDIS_USERNAME")
redis_password = os.environ.get("REDIS_PASSWORD")