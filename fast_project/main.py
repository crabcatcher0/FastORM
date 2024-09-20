from fastapi import FastAPI, Form, HTTPException, status, Query, Depends, Request
from datetime import timedelta
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from .templating import env
from .models import Product, User, Review
from .serializer import productserializer, oneserializer
from .fast_utils import search_products
from .auth.utils import get_password_hash, verify_password
from .auth.jwt_handlers import (
    create_access_token,
    get_current_user,
    get_email_from_token,
)
from .auth.decorators import login_required
import logging
from starlette.status import HTTP_401_UNAUTHORIZED
from .schema import ProductSchema


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """
    Homepage
    """
    template = env.get_template("home.html")
    return HTMLResponse(content=template.render())


@app.get("/crm")
async def projecct():
    product = productserializer(model="product", fields=("id", "title", "made_by"))
    template = env.get_template("project.html")
    return HTMLResponse(content=template.render(products=product))


@app.get("/add-product-form")
async def add_product_form():
    template = env.get_template("add_product.html")
    return HTMLResponse(content=template.render())


@app.post("/add_product")
async def add_product(title: str = Form(...), made_by: str = Form(...)):
    if title and made_by:
        data = {"title": title, "made_by": made_by}
        Product.add_data(data)
        return RedirectResponse("/success", status_code=303)
    else:
        raise HTTPException(
            status_code=400, detail="Title and Made By fields are required"
        )


@app.get("/crm/{id}")
async def detail_prod(id: int):
    data = oneserializer(model="product", fields=("id", "title", "made_by"), pk=id)
    review_data = Review.filter_data("review", "in_product", value=id)
    template = env.get_template("product_detail.html")
    return HTMLResponse(content=template.render(product=data, reviews=review_data))


@app.post("/register")
async def register(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    hashed_password = get_password_hash(password)
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password,
    }
    User.add_data(user)
    return RedirectResponse("/login", status_code=303)


@app.get("/register-form")
async def register_form():
    template = env.get_template("register.html")
    return HTMLResponse(content=template.render())


@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    user = User.get_data(email=email)
    if not user:
        logging.error(f"User with email {email} not found")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.password):
        logging.error("Password verification failed")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse("/profile", status_code=303)
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True, secure=True
    )

    return response


@app.get("/login-form")
async def login_form():
    template = env.get_template("login.html")
    return HTMLResponse(content=template.render())


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login-form")
    response.delete_cookie("access_token")
    return response


@app.get("/profile")
@login_required
async def profile(request: Request, current_user: User = Depends(get_current_user)):
    full_name = f"{current_user.first_name} {current_user.last_name}"
    review_data = Review.filter_data(
        model="review", field="review_by", value=current_user.email
    )

    template = env.get_template("profile.html")
    return HTMLResponse(
        content=template.render(
            full_name=full_name,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            rev=review_data,
        )
    )


@app.get("/search/")
async def search_query(
    request: Request, query: str = Query(..., min_length=1, max_length=100)
):
    results = search_products(query)
    if query.isdigit():
        raise HTTPException(
            status_code=400, detail="Search query should not be a numeric ID"
        )

    result_list = [
        {"id": result["id"], "title": result["title"], "made_by": result["made_by"]}
        for result in results
    ]
    return HTMLResponse(
        content=env.get_template("search_result.html").render(
            query=query, results=result_list
        )
    )


@app.get("/review-form")
async def review_form(
    request: Request, product_id: int = Query(None, description="ID of the product")
):
    template = env.get_template("add_review.html")
    return HTMLResponse(
        content=template.render({"request": request, "product_id": product_id})
    )


@app.post("/review")
async def review(
    request: Request, product_id: int = Form(...), comments: str = Form(...)
):

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token is missing")

    email = get_email_from_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Not found email...")

    data = {"review_by": email, "in_product": product_id, "comments": comments}
    Review.add_data(data)
    return RedirectResponse("/crm", status_code=303)


@app.get("/sorted")
def sort_post(sort: str = Query("newest")):
    reviews = productserializer(
        model="product", fields=("id", "title", "made_by", "created_at")
    )
    if sort == "newest":
        sorted_data = sorted(reviews, key=lambda post: post["created_at"], reverse=True)
    elif sort == "oldest":
        sorted_data = sorted(reviews, key=lambda post: post["created_at"])
    else:
        sorted_data = reviews

    return sorted_data


@app.get("/success")
def success():
    return HTMLResponse(content="<h1>Student added successfully!</h1>")
