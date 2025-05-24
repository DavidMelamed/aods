
"""FastAPI + optional GraphQL API for opportunities."""

from fastapi import FastAPI
from typing import List
from ..pipeline import Pipeline

app = FastAPI(title="AODS")
pipe = Pipeline()


def fetch_opportunities() -> List[dict]:
    return pipe.run()



def get_top_opportunities():
    # Placeholder data
    return [
        {"keyword": "ai", "score": 1.0},
        {"keyword": "ml", "score": 0.8},
    ]


@app.get("/opportunities")
def opportunities():
    return get_top_opportunities()

from fastapi import WebSocket

@app.websocket("/mcp")
async def mcp_endpoint(ws: WebSocket):
    await ws.accept()
    ops = get_top_opportunities()
    await ws.send_json(ops)
    await ws.close()



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

    return get_top_opportunities()

