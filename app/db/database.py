from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.models import Base, City, Country, Mission, Target, TargetType
from app.settings.config import DB_URL


engine = create_engine(DB_URL)
session_maker = sessionmaker(bind=engine)


if __name__ == '__main__':
   with session_maker() as session:
      targettypes = session.query(TargetType).all()
      print(targettypes)
