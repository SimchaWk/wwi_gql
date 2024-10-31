from graphene import ObjectType, String, Int, Field


class TargetType(ObjectType):
    target_id = Int()
    mission_id = Int()
    target_industry = String()
    city_id = Int()
    target_type_id = Int()
    target_priority = Int()
    mission = Field('app.gql.types.mission_type.MissionType')
    city = Field('app.gql.types.CityType')
    target_type = Field('app.gql.types.target_type_type.TargetTypeType')

    @staticmethod
    def resolve_mission(root, info):
        pass

    @staticmethod
    def resolve_city(root, info):
        pass

    @staticmethod
    def resolve_target_type(root, info):
        pass
