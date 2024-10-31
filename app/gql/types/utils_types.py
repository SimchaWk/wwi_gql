from graphene import ObjectType, Float, Int, String, Date, List, Field


class AircraftStatsType(ObjectType):
    airborne_aircraft = Float()
    attacking_aircraft = Float()
    bombing_aircraft = Float()


class AttackResultsType(ObjectType):
    returned_aircraft = Float()
    failed_aircraft = Float()
    damaged_aircraft = Float()
    lost_aircraft = Float()


class AttackResultsByTypeType(ObjectType):
    mission_id = Int()
    mission_date = Date()
    count = Float()
