from databases import Database
import sqlalchemy

DATABASE_URL = "sqlite:///pdf_storage.db"

database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

pdf_metadata = sqlalchemy.Table(
    "pdf_metadata",
    metadata,
    sqlalchemy.Column("unique_pdf_id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("filename", sqlalchemy.String),
    sqlalchemy.Column("extracted_text", sqlalchemy.Text),
    sqlalchemy.Column("page_count", sqlalchemy.Integer)
)

# Create the engine and create the tables
engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)
metadata.create_all(engine)
