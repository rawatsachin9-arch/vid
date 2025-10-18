from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes import stripe_routes

load_dotenv()

app = FastAPI(title="VideoAI API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(stripe_routes.router, prefix="/api/stripe", tags=["stripe"])

@app.get("/api/")
async def root():
    return {"message": "VideoAI API is running", "status": "success"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "VideoAI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)