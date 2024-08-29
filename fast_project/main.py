from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from .templating import env
from .models import Product
from .serializer import productserializer, oneserializer

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
    product = productserializer(
        model= 'product',
        fields=('id', 'title', 'made_by')
    )
    template = env.get_template('project.html')
    return HTMLResponse(content=template.render(products = product))


@app.get("/add-product-form")
def add_product_form():
    template = env.get_template('add_product.html')
    return HTMLResponse(content=template.render())



@app.post("/add_product")
def add_product(title: str = Form(...), made_by: str = Form(...)):
    if title and made_by:
        data = {
            'title': title,
            'made_by': made_by
        }
        Product.add_data(data)
        return RedirectResponse("/success", status_code=303)
    else:
        raise HTTPException(status_code=400, detail="Title and Made By fields are required")


@app.get("/crm/{id}")
def detail_prod(id: int):
    data = oneserializer(
        model='product',
        fields=('title', 'made_by'),
        pk=id
    )
    template = env.get_template('product_detail.html')
    return HTMLResponse(content=template.render(product = data))


@app.get("/success")
def success():
    return HTMLResponse(content="<h1>Student added successfully!</h1>")


