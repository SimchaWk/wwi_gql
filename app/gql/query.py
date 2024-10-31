from graphene import ObjectType, Int, String, Date, Field, List

from app.gql.types import MissionType

from app.gql.types.utils_types import AircraftStatsType, AttackResultsType, AttackResultsByTypeType
from app.repository.mission_repository import (
    get_mission_aircraft, get_attack_results, get_attack_results_by_type,
    get_missions_by_target_industry, get_mission_by_id, get_missions_by_date_range, get_missions_by_country
)


class Query(ObjectType):
    mission_by_id = Field(
        MissionType,
        mission_id=Int(required=True),
        description="Returns a specific mission by its mission ID"
    )

    missions_by_date_range = List(
        MissionType,
        start_date=Date(required=True),
        end_date=Date(required=True),
        description="Returns a list of missions conducted within a specific date range"
    )

    missions_by_country = List(
        MissionType,
        country_name=String(required=True),
        description="Returns a list of missions conducted in a specific country"
    )

    missions_by_target_industry = List(
        MissionType,
        target_industry=String(required=True),
        description="Returns a list of missions conducted against a specific industry sector"
    )

    mission_aircraft = Field(
        AircraftStatsType,
        mission_id=Int(required=True),
        description="Returns statistical data about aircraft that participated in a specific mission"
    )

    attack_results = Field(
        AttackResultsType,
        mission_id=Int(required=True),
        description="Returns attack results for a specific mission"
    )

    attack_results_by_type = List(
        AttackResultsByTypeType,
        attack_type=String(required=True),
        description="Returns a list of attack results filtered by attack type"
    )

    @staticmethod
    def resolve_mission_by_id(root, info, mission_id):
        result = get_mission_by_id(mission_id)
        return result.value_or(None)

    @staticmethod
    def resolve_missions_by_date_range(root, info, start_date, end_date):
        result = get_missions_by_date_range(start_date, end_date)
        return result.value_or([])

    @staticmethod
    def resolve_missions_by_country(root, info, country_name):
        result = get_missions_by_country(country_name)
        return result.value_or([])

    @staticmethod
    def resolve_missions_by_target_industry(root, info, target_industry):
        result = get_missions_by_target_industry(target_industry)
        return result.value_or([])

    @staticmethod
    def resolve_mission_aircraft(root, info, mission_id):
        result = get_mission_aircraft(mission_id)
        return result.value_or(None)

    @staticmethod
    def resolve_attack_results(root, info, mission_id):
        result = get_attack_results(mission_id)
        return result.value_or(None)

    @staticmethod
    def resolve_attack_results_by_type(root, info, attack_type):
        result = get_attack_results_by_type(attack_type)
        return result.value_or([])
