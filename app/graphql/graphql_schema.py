import strawberry

from app.graphql.users.queries import UserQuery
from app.graphql.users.mutations import UserMutation


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


graphql_schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)