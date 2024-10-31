from graphene import Mutation, Int, Boolean, String
from app.db.database import session_maker
from app.db.models import Mission, Target
from app.gql.input_types import CreateMissionInput, CreateTargetInput, UpdateAttackResultsInput
from app.gql.types.mission_type import MissionType
from app.gql.types.target_type import TargetType


class CreateMission(Mutation):
    class Arguments:
        mission_data = CreateMissionInput(required=True)

    Output = MissionType

    @staticmethod
    def mutate(root, info, mission_data):
        mission = Mission(
            mission_date=mission_data.mission_date,
            airborne_aircraft=mission_data.airborne_aircraft,
            attacking_aircraft=mission_data.attacking_aircraft,
            bombing_aircraft=mission_data.bombing_aircraft,
            aircraft_returned=mission_data.aircraft_returned,
            aircraft_failed=mission_data.aircraft_failed,
            aircraft_damaged=mission_data.aircraft_damaged,
            aircraft_lost=mission_data.aircraft_lost
        )
        with session_maker() as session:
            session.add(mission)
            session.commit()
            session.refresh(mission)
        return mission


class CreateTarget(Mutation):
    class Arguments:
        target_data = CreateTargetInput(required=True)

    Output = TargetType

    @staticmethod
    def mutate(root, info, target_data):
        with session_maker() as session:
            mission = session.query(Mission).filter(Mission.mission_id == target_data.mission_id).first()
            if not mission:
                raise Exception(f"Mission with ID {target_data.mission_id} not found")

            target = Target(
                mission_id=target_data.mission_id,
                target_industry=target_data.target_industry,
                city_id=target_data.city_id,
                target_type_id=target_data.target_type_id,
                target_priority=target_data.target_priority
            )
            session.add(target)
            session.commit()
            session.refresh(target)
        return target


class UpdateAttackResults(Mutation):
    class Arguments:
        mission_id = Int(required=True)
        attack_data = UpdateAttackResultsInput(required=True)

    Output = MissionType

    @staticmethod
    def mutate(root, info, mission_id, attack_data):
        with session_maker() as session:
            mission = session.query(Mission).filter(Mission.mission_id == mission_id).first()
            if not mission:
                raise Exception(f"Mission with ID {mission_id} not found")

            updates = {field: value for field, value in attack_data.items() if value is not None}
            if not updates:
                raise Exception("No fields provided for update")

            for field, value in updates.items():
                setattr(mission, field, value)

            session.commit()
            session.refresh(mission)
        return mission


class DeleteMission(Mutation):
    class Arguments:
        mission_id = Int(required=True)

    success = Boolean()
    message = String()

    @staticmethod
    def mutate(root, info, mission_id):
        try:
            with session_maker() as session:
                mission = session.query(Mission).filter(Mission.mission_id == mission_id).first()
                if not mission:
                    return DeleteMission(success=False, message=f"Mission with ID {mission_id} not found")

                session.query(Target).filter(Target.mission_id == mission_id).delete()

                session.delete(mission)
                session.commit()

                return DeleteMission(success=True, message="Mission and related targets deleted successfully")

        except Exception as e:
            return DeleteMission(success=False, message=str(e))
