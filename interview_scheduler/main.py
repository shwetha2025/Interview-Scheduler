import uvicorn
from fastapi import FastAPI
from interview_scheduler.core.config.constants import ServiceDetails
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from interview_scheduler.core.services.login import router
from interview_scheduler.core.services.schedule import sched_router


app = FastAPI(title="Interview Scheduler")

app.include_router(router)
app.include_router(sched_router)

app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=ServiceDetails.service_host,
        port=int(ServiceDetails.service_port),
    )
