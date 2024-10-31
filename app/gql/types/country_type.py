from graphene import ObjectType, String, Int, List


class CountryType(ObjectType):
    country_id = Int()
    country_name = String()
    cities = List('app.gql.types.city_type.CityType')

    @staticmethod
    def resolve_cities(root, info):
        pass
