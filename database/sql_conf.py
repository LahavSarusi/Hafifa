import os


# class BaseSqlConfig:
#     db_server_name = os.environ.get("DB_SERVER_NAME", "MZ-SQL-DEV08")
#     db_name = os.environ.get("DB_NAME", "heromanager")
#     db_username = os.environ.get("DB_USERNAME", "herouser")
#     db_password = os.environ.get("DB_PASSWORD", "Password1")
#     SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{db_username}:{db_password}@{db_server_name}/{db_name}?driver=ODBC+Driver17+for+SQL+Server"
class BaseSqlConfig:
    SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'


class SqliteTestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
