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
    target_type_id = Int(required=True)
    target_priority = Int()


class CreateAttackResultsInput(InputObjectType):
    mission_id = Int(required=True)
    aircraft_returned = Float(required=True)
    aircraft_failed = Float(required=True)
    aircraft_damaged = Float(required=True)
    aircraft_lost = Float(required=True)


class UpdateAttackResultsInput(InputObjectType):
    aircraft_returned = Float()
    aircraft_failed = Float()
    aircraft_damaged = Float()
    aircraft_lost = Float()
