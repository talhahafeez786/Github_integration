from fastapi import FastAPI
from routes import auth_routes, integration_routes, data_routes, search_routes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(integration_routes.router)
app.include_router(data_routes.router)
app.include_router(search_routes.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:8000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "GitHub Integration API is running"}
