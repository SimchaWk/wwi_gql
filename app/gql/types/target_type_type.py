from graphene import ObjectType, String, Int, List, Float


class TargetTypeType(ObjectType):
    target_type_id = Int()
    target_type_name = String()
    targets = List('app.gql.types.target_type.TargetType')

    @staticmethod
    def resolve_targets(root, info):
        pass
