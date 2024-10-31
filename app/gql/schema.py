import graphene

from app.gql.mutation import Mutation
from app.gql.query import Query

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
