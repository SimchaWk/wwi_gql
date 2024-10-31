from typing import List
from returns.maybe import Maybe
from returns.result import Result, Success, Failure

from app.db.database import session_maker
from app.db.models import Target


def get_target_by_id(target_id: int) -> Maybe[Target]:
    with session_maker() as session:
        try:
            target = session.get(Target, target_id)
            return Maybe.from_optional(target)
        except Exception as e:
            session.rollback()
            return Maybe.empty


def get_targets_by_mission(mission_id: int) -> Result[List[Target], str]:
    with session_maker() as session:
        try:
            targets = (
                session.query(Target)
                .filter(Target.mission_id == mission_id)
                .all()
            )
            return Success(targets)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch targets: {str(e)}")


def create_target(target: Target) -> Result[Target, str]:
    with session_maker() as session:
        try:
            session.add(target)
            session.commit()
            session.refresh(target)
            return Success(target)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to create target: {str(e)}")


def get_targets_by_industry(industry: str) -> Result[List[Target], str]:
    with session_maker() as session:
        try:
            targets = (
                session.query(Target)
                .filter(Target.target_industry == industry)
                .all()
            )
            return Success(targets)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch targets by industry: {str(e)}")
