import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import clients, lessons, students
from .core.config import settings
from .core.database import create_db_and_tables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info('Starting up TutorCruncher API...')
    create_db_and_tables()
    logger.info('Database tables created')

    # Initialize monitoring
    if settings.sentry_dsn:
        import sentry_sdk

        sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=1.0)
        logger.info('Sentry initialized')

    if settings.logfire_token:
        try:
            import logfire

            logfire.configure(token=settings.logfire_token)
            logger.info('Logfire initialized')
        except ImportError:
            logger.warning('Logfire token provided but logfire not properly configured')

    yield

    # Shutdown
    logger.info('Shutting down TutorCruncher API...')


app = FastAPI(
    title='TutorCruncher AI API',
    description='Backend API for TutorCruncher AI tutoring management system',
    version='0.1.0',
    lifespan=lifespan,
)

# Configure CORS
allowed_origins = settings.allowed_origins.split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include routers
app.include_router(clients.router, prefix='/api')
app.include_router(students.router, prefix='/api')
app.include_router(lessons.router, prefix='/api')


@app.get('/')
async def root():
    return {'message': 'TutorCruncher AI API', 'version': '0.1.0'}


@app.get('/health')
async def health_check():
    return {'status': 'healthy'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app.main:app', host=settings.api_host, port=settings.api_port, reload=True)
