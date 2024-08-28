from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from .templating import env
from fastapi.staticfiles import StaticFiles
from .models import Student, Course
from .serializer import studentserializer, courseserializer


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def root():
    """
        Homepage
    """
    template = env.get_template('home.html')
    return HTMLResponse(content=template.render())



@app.get("/crm")
def projecct():
    template = env.get_template('project.html')
    return HTMLResponse(content=template.render())




@app.get("/student")
def student_data():
    """
        Displays the data from student and courses:
        option: serialized and html response
    """
    student_data = studentserializer(
        model='student',
        fields=('id', 'first_name', 'last_name', 'address', 'email')
    )

    enrolled_std = len(student_data)

    course_data = courseserializer(
        model='course',
        fields=('course_name', 'course_code')
    )
    # return {'student_data': student_data, 'course_data': course_data} #serialized form
    
    template = env.get_template('students.html')
    return HTMLResponse(content=template.render(
        students=student_data,
        courses=course_data,
        total_students=enrolled_std)
    )



@app.get("/add_student")
def add_student():
    template = env.get_template('add_student.html')
    return HTMLResponse(content=template.render())



@app.post("/adding_student")
def adding_student(
        first_name: str = Form(...),
        last_name: str = Form(...),
        address: str = Form(...),
        email: str = Form(...)
    ):

    """
    processes the student data and add it to the database
    data should be dict as add_data method takes an dict
    """

    if first_name and last_name and address and email:
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'email': email
        }
        Student.add_data(data)
        return RedirectResponse("/success", status_code=303)


@app.get("/add_course")
def add_course():
    template = env.get_template('add_course.html')
    return HTMLResponse(content=template.render())



@app.post("/adding_course")
def adding_course(
    course_name: str = Form(...),
    course_code: str = Form(...)
    ):

    """
    processes the corse data and add it to the database
    data should be dict
    """
     
    if course_name and course_code:
        data = {
            'course_name': course_name,
            'course_code': course_code
        }
        Course.add_data(data)
        return RedirectResponse("/success", status_code=303)



@app.get("/success")
def success():
    return HTMLResponse(content="<h1>Student added successfully!</h1>")


