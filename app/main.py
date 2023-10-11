from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import standard, protected

app = FastAPI(
    title="CSIT SPOOKY API",
    description=
    "Discover the spirit of Halloween at your fingertips! This spooky API offers spooky messages and helps you find the closest haunted houses or events based on your provided MRT station."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Only allows GET requests
    allow_headers=["*"],
)

# Include any other app configurations or route definitions here
app.include_router(standard.router, tags=["General APIs"])
app.include_router(protected.router, tags=["Protected APIs"])


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    # Redirect the root URL ("/") to the API documentation
    return RedirectResponse("/docs")
