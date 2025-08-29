import os
import yaml
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
CONFIG_DIR = os.path.join(BASE_DIR, "config")


def load_config():
    """
    Load database config from YAML based on APP_ENV.
    Falls back to 'local.yml' at project root if not found.
    """
    env = os.getenv("APP_ENV", "LOCAL").upper()  # e.g. LOCAL, DEV, PROD
    config_file = os.path.join(CONFIG_DIR, f"{env.lower()}.yml")

    # fallback: root/local.yml
    if not os.path.exists(config_file):
        config_file = os.path.join(BASE_DIR, "local.yml")

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # e.g. LOCAL_DATABASE
    key = f"{env}_DATABASE"
    if key not in config:
        raise KeyError(f"Expected '{key}' in {config_file}, found {list(config.keys())}")

    return config[key]


def build_base_url(config: dict) -> str:
    """Build connection URL without DB (for creating database if missing)."""
    user = config["USER_NAME"]
    password = urllib.parse.quote_plus(config["PASSWORD"])
    host = config["HOST"]
    port = config["PORT"]
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/"


def build_database_url(config: dict) -> str:
    """Build connection URL including DB name."""
    return build_base_url(config) + config["DATABASE_NAME"]


def create_db_engine():
    """Ensure DB exists, then return SQLAlchemy engine bound to it."""
    db_conf = load_config()

    # Step 1: connect without DB
    base_engine = create_engine(build_base_url(db_conf), pool_pre_ping=True)

    # Step 2: create DB if missing
    with base_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_conf['DATABASE_NAME']}"))
        conn.commit()

    # Step 3: connect to actual DB
    return create_engine(build_database_url(db_conf), pool_pre_ping=True)


# --- Initialize Engine, Session, Base ---
engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Dependency for FastAPI ---
def get_db():
    """Provide a DB session for routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
