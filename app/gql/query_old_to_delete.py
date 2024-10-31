from graphene import ObjectType, String, Int, Float, Date, List, Field


# Example Query Type
class Query(ObjectType):
    mission_by_id = Field(MissionType, mission_id=Int(required=True))
    missions_by_date_range = List(
        MissionType,
        start_date=Date(required=True),
        end_date=Date(required=True)
    )
    missions_by_country = List(
        MissionType,
        country_name=String(required=True)
    )
    missions_by_target_industry = List(
        MissionType,
        target_industry=String(required=True)
    )

    def resolve_mission_by_id(self, info, mission_id):
        return Mission.query.filter(Mission.mission_id == mission_id).first()

    def resolve_missions_by_date_range(self, info, start_date, end_date):
        return Mission.query.filter(
            Mission.mission_date >= start_date,
            Mission.mission_date <= end_date
        ).all()

    def resolve_missions_by_country(self, info, country_name):
        return Mission.query.join(Target).join(City).join(Country).filter(
            Country.country_name == country_name
        ).all()

    def resolve_missions_by_target_industry(self, info, target_industry):
        return Mission.query.join(Target).filter(
            Target.target_industry == target_industry
        ).all()
