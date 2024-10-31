from graphene import ObjectType, String, Int, List, Float, Field


class CityType(ObjectType):
    city_id = Int()
    city_name = String()
    country_id = Int()
    latitude = Float()
    longitude = Float()
    country = Field('app.gql.types.country_type.CountryType')
    targets = List('app.gql.types.target_type.TargetType')

    @staticmethod
    def resolve_country(root, info, city_id):
        pass

    @staticmethod
    def resolve_targets(root, info):
        pass
