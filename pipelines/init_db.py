from db.connection import get_engine
from models.schema import Base

def init_database(reset: bool = False):
    engine = get_engine()
    if reset:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Database tables initialized!")

if __name__ == "__main__":
    # Pass reset=True only when you explicitly want a full wipe
    init_database(reset=True)