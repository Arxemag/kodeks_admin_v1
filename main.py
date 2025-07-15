from fastapi import FastAPI
from api import auth, admin, users

app = FastAPI(title="Kodeks Admin API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Administration"])
app.include_router(users.router, prefix="/user", tags=["Users"])