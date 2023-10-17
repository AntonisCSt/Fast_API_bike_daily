from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home_page():
    return "Hello World"

@app.get("/about")
def about_page():
    return "A test page"

#uvicorn fastapi_example:app --reload