from graphene import Mutation
from app.db.database import session_maker
from app.db.models import Mission, Target
from app.gql.input_types import CreateTargetInput
from app.gql.types.target_type import TargetType


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
