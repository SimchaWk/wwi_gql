from graphene import InputObjectType, Int, Float, String, Date

class CreateMissionInput(InputObjectType):
    mission_date = Date(required=True)
    airborne_aircraft = Float(required=True)
    attacking_aircraft = Float(required=True)
    bombing_aircraft = Float(required=True)
    aircraft_returned = Float()
    aircraft_failed = Float()
    aircraft_damaged = Float()
    aircraft_lost = Float()

class CreateTargetInput(InputObjectType):
    mission_id = Int(required=True)
    target_industry = String(required=True)
    city_id = Int(required=True)
    target_type_id = Int()
    target_priority = Int()

class UpdateAttackResultsInput(InputObjectType):
    aircraft_returned = Float()
    aircraft_failed = Float()
    aircraft_damaged = Float()
    aircraft_lost = Float()