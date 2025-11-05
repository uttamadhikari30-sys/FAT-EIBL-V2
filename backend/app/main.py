from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from .database import engine, Base
from .routes import auth, audit_requests, imports, reports, ai, seed, roles, audit_logs
from .scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FAT-EIBL")

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth.router)
app.include_router(audit_requests.router)
app.include_router(imports.router)
app.include_router(reports.router)
app.include_router(ai.router)
app.include_router(seed.router)
app.include_router(roles.router)
app.include_router(audit_logs.router)

start_scheduler()

@app.get('/')
def root():
    return {'message': 'FAT-EIBL - API'}

@app.get('/docs', include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + ' - Docs', swagger_favicon_url='/static/logo.svg')
