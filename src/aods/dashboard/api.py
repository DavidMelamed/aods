
"""FastAPI + optional GraphQL API for opportunities."""

from typing import List

try:
    from fastapi import FastAPI, WebSocket
except Exception:  # pragma: no cover - optional dependency
    FastAPI = None
    WebSocket = None

from ..pipeline import Pipeline

app = FastAPI(title="AODS") if FastAPI else None
pipe = Pipeline()


def fetch_opportunities() -> List[dict]:
    """Run the pipeline and return ranked opportunities."""
    return pipe.run()



def get_top_opportunities():
    return fetch_opportunities()


if app:
    @app.get("/opportunities")
    def opportunities():
        return fetch_opportunities()

    @app.websocket("/mcp")
    async def mcp_endpoint(ws: WebSocket):
        await ws.accept()
        ops = fetch_opportunities()
        await ws.send_json(ops)
        await ws.close()



if app:
    try:
        import graphene
        from starlette_graphene3 import GraphQLApp

        class Opportunity(graphene.ObjectType):
            keyword = graphene.String()
            score = graphene.Float()

        class Query(graphene.ObjectType):
            opportunities = graphene.List(Opportunity)

            def resolve_opportunities(root, info):
                return fetch_opportunities()

        graphql_app = GraphQLApp(schema=graphene.Schema(query=Query))
        app.add_route("/graphql", graphql_app)
    except Exception:  # pragma: no cover - optional dependency
        pass

