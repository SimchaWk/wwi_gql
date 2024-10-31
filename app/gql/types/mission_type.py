from graphene import ObjectType, String, Int, List, Float, Field


class CityType(ObjectType):
    city_id = Int()
    city_name = String()
    country_id = Int()
    latitude = Float()
    longitude = Float()
    country = Field(lambda: CountryType)
    targets = List(lambda: TargetType)

    @staticmethod
    def resolve_country(root, info):
        return Country.query.filter(Country.country_id == root.country_id).first()

    @staticmethod
    def resolve_targets(root, info):
        return Target.query.filter(Target.city_id == root.city_id).all()