from graphene import ObjectType, String, Int, List

class CountryType(ObjectType):
    country_id = Int()
    country_name = String()
    cities = List(lambda: CityType)

    @staticmethod
    def resolve_cities(root, info):
        return City.query.filter(City.country_id == root.country_id).all()