import uvicorn
from fastapi import FastAPI
from ag_ui_langgraph import LangGraphAgent, add_langgraph_fastapi_endpoint
from contextlib import asynccontextmanager
from agent.agent import graph
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def _lifespan(app: FastAPI):
    add_langgraph_fastapi_endpoint(
        app=app,
        agent=LangGraphAgent(
            name="agent",
            description="An example agent to use as a starting point for your own agent.",
            graph=graph,
        ),
        path="/",
    )
    yield
app = FastAPI(lifespan=_lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    uvicorn.run("agent.main:app", host="0.0.0.0", port=8000, reload=True)
