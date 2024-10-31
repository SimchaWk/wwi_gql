from graphene import ObjectType

from app.gql.mutations.missions_mutations import CreateMission, CreateAttackResults, UpdateAttackResults, DeleteMission
from app.gql.mutations.targets_mutations import CreateTarget


class Mutation(ObjectType):
    create_mission = CreateMission.Field()
    create_target = CreateTarget.Field()
    create_attack_results = CreateAttackResults.Field()
    update_attack_results = UpdateAttackResults.Field()
    delete_mission = DeleteMission.Field()
