import os
import yaml
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


def load_config():
    """
    Load database config from the correct YAML file based on APP_ENV.
    Falls back to 'local.yml' if APP_ENV is not set.
    """
    env = os.getenv("APP_ENV", "local").lower()
    config_file = f"config/{env}.yml"

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def build_database_url(config: dict) -> str:
    """
    Build SQLAlchemy database URL from config dictionary.
    Example: mysql+mysqlconnector://user:password@host:port/dbname
    """
    user = config["DB_USER"]
    password = config["DB_PASSWORD"]
    host = config["DB_HOST"]
    port = config["DB_PORT"]
    db_name = config["DB_NAME"]

    return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"


def create_db_engine():
    """Create a SQLAlchemy engine using the loaded config."""
    db_conf = load_config()
    database_url = build_database_url(db_conf)
    return create_engine(database_url, pool_pre_ping=True)


# --- Initialize Engine, Session, and Base ---
engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Dependency for FastAPI Routes ---
def get_db():
    """
    Dependency that provides a database session.
    Closes session after request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
