from fastapi import FastAPI, Depends, Request

from .apis.users import userAPI

app = FastAPI()

#API End points
app.include_router(userAPI)

# def getting_requests(request: Request):
#     my_headers = {"access_token": request.headers.get("Authorization")}
#     return my_headers

# Home page
@app.get("/home")
def home_api():
    
    return {"message": "Welcome to TestZip - Users"}