from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .city import City
from .country import Country
from .mission import Mission
from .target import Target
from .target_type import TargetType
