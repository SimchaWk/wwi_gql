from typing import List, Dict, Any
from datetime import date
from returns.maybe import Maybe
from returns.result import Result, Success, Failure

from app.db.database import session_maker
from app.db.models import Mission, Target, City, Country, TargetType


def get_mission_by_id(mission_id: int) -> Maybe[Mission]:
    with session_maker() as session:
        try:
            mission = session.get(Mission, mission_id)
            return Maybe.from_optional(mission)
        except Exception as e:
            session.rollback()
            return Maybe.empty


def get_missions_by_date_range(start_date: date, end_date: date) -> Result[List[Mission], str]:
    with session_maker() as session:
        try:
            missions = session.query(Mission).filter(
                Mission.mission_date >= start_date,
                Mission.mission_date <= end_date
            ).all()
            return Success(missions)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch missions by date range: {str(e)}")


def get_missions_by_country(country_name: str) -> Result[List[Mission], str]:
    with session_maker() as session:
        try:
            missions = (
                session.query(Mission)
                .join(Target)
                .join(City)
                .join(Country)
                .filter(Country.country_name == country_name)
                .all()
            )
            return Success(missions)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch missions by country: {str(e)}")


def get_missions_by_target_industry(target_industry: str) -> Result[List[Mission], str]:
    with session_maker() as session:
        try:
            missions = (
                session.query(Mission)
                .join(Target)
                .filter(Target.target_industry == target_industry)
                .all()
            )
            return Success(missions)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch missions by target industry: {str(e)}")


def create_mission(mission: Mission) -> Result[Mission, str]:
    with session_maker() as session:
        try:
            session.add(mission)
            session.commit()
            session.refresh(mission)
            return Success(mission)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to create mission: {str(e)}")


def delete_mission_with_targets(mission_id: int) -> Result[bool, str]:
    with session_maker() as session:
        try:
            session.query(Target).filter(Target.mission_id == mission_id).delete()

            result = session.query(Mission).filter(Mission.mission_id == mission_id).delete()
            if result == 0:
                return Failure("Mission not found")

            session.commit()
            return Success(True)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to delete mission: {str(e)}")


def update_mission_results(
        mission_id: int,
        aircraft_returned: float = None,
        aircraft_failed: float = None,
        aircraft_damaged: float = None,
        aircraft_lost: float = None
) -> Result[Mission, str]:
    with session_maker() as session:
        try:
            mission = session.get(Mission, mission_id)
            if not mission:
                return Failure("Mission not found")

            updates = {
                'aircraft_returned': aircraft_returned,
                'aircraft_failed': aircraft_failed,
                'aircraft_damaged': aircraft_damaged,
                'aircraft_lost': aircraft_lost
            }

            for field, value in updates.items():
                if value is not None:
                    setattr(mission, field, value)

            session.commit()
            session.refresh(mission)
            return Success(mission)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to update mission results: {str(e)}")


def get_mission_aircraft(mission_id: int) -> Result[Dict[str, Any], str]:
    with session_maker() as session:
        try:
            mission = session.get(Mission, mission_id)
            if not mission:
                return Failure("Mission not found")

            stats = {
                "airborne_aircraft": mission.airborne_aircraft,
                "attacking_aircraft": mission.attacking_aircraft,
                "bombing_aircraft": mission.bombing_aircraft
            }
            return Success(stats)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch aircraft stats: {str(e)}")


def get_attack_results(mission_id: int) -> Result[Dict[str, Any], str]:
    with session_maker() as session:
        try:
            mission = session.get(Mission, mission_id)
            if not mission:
                return Failure("Mission not found")

            results = {
                "returned_aircraft": mission.aircraft_returned,
                "failed_aircraft": mission.aircraft_failed,
                "damaged_aircraft": mission.aircraft_damaged,
                "lost_aircraft": mission.aircraft_lost
            }
            return Success(results)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch attack results: {str(e)}")


def get_attack_results_by_type(attack_type: str) -> Result[List[Dict], str]:
    with session_maker() as session:
        try:
            target_type = (
                session.query(TargetType)
                .filter(TargetType.target_type_name == attack_type)
                .first()
            )

            if not target_type:
                return Failure(f"Invalid attack type: {attack_type}")

            missions = (
                session.query(Mission)
                .join(Target)
                .join(TargetType)
                .filter(TargetType.target_type_name == attack_type)
                .all()
            )

            results = [
                {
                    'mission_id': mission.mission_id,
                    'mission_date': mission.mission_date,
                    'returned_aircraft': mission.aircraft_returned,
                    'failed_aircraft': mission.aircraft_failed,
                    'damaged_aircraft': mission.aircraft_damaged,
                    'lost_aircraft': mission.aircraft_lost,
                    'target_type': attack_type
                }
                for mission in missions
            ]

            return Success(results)
        except Exception as e:
            session.rollback()
            return Failure(f"Failed to fetch attack results by type: {str(e)}")
