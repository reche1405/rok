from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
db = SQLAlchemy()

@event.listens_for(db.engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()