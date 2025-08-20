from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import works, materials, projects, estimates, exports
from .settings import settings


app = FastAPI(title="Construction Estimate API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(works.router, prefix="/works", tags=["works"])
app.include_router(materials.router, prefix="/materials", tags=["materials"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(estimates.router, prefix="/estimates", tags=["estimates"])
app.include_router(exports.router, prefix="/exports", tags=["exports"])

