from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import ingredients, auth, shopping_lists, recipes, users
from app.routers import news as news_router
from app.routers import pages as pages_router
from app.routers import mailbox as mailbox_router
from app.routers import admin_mailbox as admin_mailbox_router
import os


def create_app() -> FastAPI:
    app = FastAPI(title="Reste-Rampe Backend")

    origins = [
        os.environ.get("VITE_APP_ORIGIN", "http://localhost:5173"),
        "http://localhost:3000",
        "http://localhost",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include routers
    app.include_router(ingredients.router)
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(mailbox_router.router)
    app.include_router(admin_mailbox_router.router)
    app.include_router(shopping_lists.router, prefix="/api/shopping-lists")
    app.include_router(recipes.router, prefix="/api/recipes")
    app.include_router(news_router.router, prefix="/api/news")
    app.include_router(pages_router.router, prefix="/api")

    @app.on_event("startup")
    def on_startup():
        # Create tables if they don't exist (using updated SQLAlchemy models with user_id)
        Base.metadata.create_all(bind=engine)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
