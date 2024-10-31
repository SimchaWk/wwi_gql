from sqlalchemy import Column, Integer, Date, Numeric
from sqlalchemy.orm import relationship

from app.db.models import Base


class Mission(Base):
    __tablename__ = 'missions'

    mission_id = Column(Integer, primary_key=True, autoincrement=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Numeric(10, 2))
    attacking_aircraft = Column(Numeric(10, 2))
    bombing_aircraft = Column(Numeric(10, 2))
    aircraft_returned = Column(Numeric(10, 2))
    aircraft_failed = Column(Numeric(10, 2))
    aircraft_damaged = Column(Numeric(10, 2))
    aircraft_lost = Column(Numeric(10, 2))

    targets = relationship("Target", back_populates="mission")
