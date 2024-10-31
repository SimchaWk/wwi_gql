from graphene import ObjectType, String, Int, List, Float, Field


class TargetType(ObjectType):
    target_id = Int()
    mission_id = Int()
    target_industry = String()
    city_id = Int()
    target_type_id = Int()
    target_priority = Int()
    mission = Field(lambda: MissionType)
    city = Field(lambda: CityType)
    target_type = Field(lambda: TargetTypeType)

    @staticmethod
    def resolve_mission(root, info):
        return Mission.query.filter(Mission.mission_id == root.mission_id).first()

    @staticmethod
    def resolve_city(root, info):
        return City.query.filter(City.city_id == root.city_id).first()

    @staticmethod
    def resolve_target_type(root, info):
        return TargetType.query.filter(TargetType.target_type_id == root.target_type_id).first()