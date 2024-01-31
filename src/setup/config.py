import os 


def get_postgres_uri():
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    user = os.environ.get("DB_USER")    
    password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")    
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
