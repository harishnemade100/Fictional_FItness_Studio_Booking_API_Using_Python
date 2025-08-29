import os
import yaml
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator, Optional, Dict, Any

load_dotenv()

# Directories
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
CONFIG_DIR: str = os.path.join(BASE_DIR, "config")


def load_config(section: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file based on APP_ENV.

    Args:
        section (Optional[str]): Specific section to retrieve from the config file.
            - If None, returns the entire config dictionary.
            - Example: "LOCAL_DATABASE", "JWT_TOKEN"

    Raises:
        FileNotFoundError: If the config file cannot be found.
        KeyError: If the specified section is missing in the config file.

    Returns:
        Dict[str, Any]: The configuration dictionary or section.
    """
    env = os.getenv("APP_ENV", "LOCAL").upper()  # e.g., LOCAL, DEV, PROD
    config_file = os.path.join(CONFIG_DIR, f"{env.lower()}.yml")

    # Fallback: root/local.yml
    if not os.path.exists(config_file):
        config_file = os.path.join(BASE_DIR, "local.yml")

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, "r") as f:
        config: Dict[str, Any] = yaml.safe_load(f)

    if section:
        if section not in config:
            raise KeyError(f"Expected section '{section}' in {config_file}, found {list(config.keys())}")
        return config[section]

    return config


def build_base_url(config: Dict[str, Any]) -> str:
    """
    Build the SQLAlchemy connection URL without a database name.

    Args:
        config (Dict[str, Any]): Database configuration dictionary.

    Returns:
        str: SQLAlchemy connection URL (without DB name).
    """
    user = config["USER_NAME"]
    password = urllib.parse.quote_plus(config["PASSWORD"])
    host = config["HOST"]
    port = config["PORT"]
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/"


def build_database_url(config: Dict[str, Any]) -> str:
    """
    Build the SQLAlchemy connection URL including the database name.

    Args:
        config (Dict[str, Any]): Database configuration dictionary.

    Returns:
        str: SQLAlchemy connection URL (with DB name).
    """
    return build_base_url(config) + config["DATABASE_NAME"]


def create_db_engine():
    """
    Ensure the database exists, then return a SQLAlchemy engine bound to it.

    Returns:
        Engine: SQLAlchemy engine instance connected to the target database.
    """
    db_conf = load_config("LOCAL_DATABASE")

    # Step 1: Connect without DB (to ensure database exists)
    base_engine = create_engine(build_base_url(db_conf), pool_pre_ping=True)

    # Step 2: Create DB if missing
    with base_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_conf['DATABASE_NAME']}"))
        conn.commit()

    # Step 3: Return engine connected to actual DB
    return create_engine(build_database_url(db_conf), pool_pre_ping=True)


# --- Initialize Engine, Session, Base ---
engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session dependency for FastAPI routes.

    Yields:
        Session: SQLAlchemy database session.

    Ensures:
        Session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
