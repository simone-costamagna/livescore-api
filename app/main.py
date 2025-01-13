import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from starlette.responses import RedirectResponse
from app.routers import country, league, archive, match
from logger.logger_config import configure_logging
import os

load_dotenv()

RATE_LIMITING_FREQUENCY = os.getenv("RATE_LIMITING_FREQUENCY")
RATE_LIMITING_ENABLE = bool(os.getenv("RATE_LIMITING_ENABLE"))

configure_logging()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[RATE_LIMITING_FREQUENCY],
    enabled=RATE_LIMITING_ENABLE,
)

app = FastAPI(title="Football LiveScore Scraper API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Routers
app.include_router(country.router, prefix=f"/{country.ROUTER_NAME}", tags=["countries"])
app.include_router(league.router, prefix=f"/{league.ROUTER_NAME}", tags=["leagues"])
app.include_router(archive.router, prefix=f"/{archive.ROUTER_NAME}", tags=["archives"])
app.include_router(match.router, prefix=f"/{match.ROUTER_NAME}", tags=["matches"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
