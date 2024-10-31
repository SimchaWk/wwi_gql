from graphene import Mutation, Int, Boolean, String
from app.db.database import session_maker
from app.db.models import Mission, Target
from app.gql.input_types import CreateMissionInput, UpdateAttackResultsInput, CreateAttackResultsInput
from app.gql.types.mission_type import MissionType


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


class CreateAttackResults(Mutation):
    class Arguments:
        attack_data = CreateAttackResultsInput(required=True)

    Output = MissionType

    @staticmethod
    def mutate(root, info, attack_data):
        with session_maker() as session:
            mission = session.query(Mission).filter(Mission.mission_id == attack_data.mission_id).first()
            if not mission:
                raise Exception(f"Mission with ID {attack_data.mission_id} not found")

            if any([
                mission.aircraft_returned is not None,
                mission.aircraft_failed is not None,
                mission.aircraft_damaged is not None,
                mission.aircraft_lost is not None
            ]):
                raise Exception(f"Attack results already exist for mission {attack_data.mission_id}")

            data = {field: value for field, value in attack_data.items() if value is not None}
            if not data:
                raise Exception("No fields provided for creation")

            for field, value in data.items():
                setattr(mission, field, value)

            session.commit()
            session.refresh(mission)

        return mission


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
