from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .templating import env
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def root():
    template = env.get_template('home.html')
    return HTMLResponse(content=template.render())


@app.get("/crm")
def projecct():
    template = env.get_template('project.html')
    return HTMLResponse(content=template.render())


@app.get("/student")
def student_data():
    template = env.get_template('students.html')
    return HTMLResponse(content=template.render())