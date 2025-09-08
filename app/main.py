from fastapi import FastAPI
from app.routes import questions

app = FastAPI(title="Docx2HTML Converter API")

app.include_router(questions.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Docx2HTML Converter API running"}
