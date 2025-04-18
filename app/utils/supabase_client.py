import psycopg2
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # service key for full access

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))
