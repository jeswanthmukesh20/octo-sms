from typing import Optional, Union, Dict
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status, FastAPI, Response
from keycloak import KeycloakOpenID
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from keycloak.exceptions import KeycloakAuthenticationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyCookie
from fastapi import FastAPI, Request
from db import Database
from models import *
import logging
import uvicorn
import os


MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST', "mongo")
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
CLIENT = os.getenv('CLIENT', "rest-client")
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
DOMAIN = os.getenv('DOMAIN')
REALM = os.getenv('REALM')
ADMIN_DOMAIN = os.getenv("ADMIN_DOMAIN")

app = FastAPI(
    # root_path="/api",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Octa-Monitor",
    description="Student Monitoring System",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": "octa-auth",
        "scopes": ""
    }
)

origins = [
    f"https://{DOMAIN}"
    # ["http://localhost:3000"]
    # "http://localhost:5000",
]

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=[DOMAIN, ADMIN_DOMAIN]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"https://{DOMAIN}/api/token",
    auto_error=False,
    )
cookie_sec = APIKeyCookie(name="session")

keycloak_openid = KeycloakOpenID(
    server_url=f"https://auth.octamonitor.com/auth/",
    client_id=CLIENT,
    realm_name=REALM,
    client_secret_key=CLIENT_SECRET,
    verify=False
)

options = {"verify_signature": True, "verify_aud": False, "exp": True}

# def verify_collection(collection):
#     try:
#         collection = Mongo_collection[collection]
#         return collection
#     except KeyError as msg:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=str(msg)
#         )


def decode_token(token):
    KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + \
                          f"{keycloak_openid.public_key()}" + \
                          "\n-----END PUBLIC KEY-----"
    try:
        print(token)
        user = keycloak_openid.decode_token(token=token, key=KEYCLOAK_PUBLIC_KEY, options=options)
        print(user)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please Login!"
        )
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please Login!"
        )
    return user


async def get_current_user(token: dict = Depends(oauth2_scheme)):
    print(token)
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/api/token", tags=["Authentication"], include_in_schema=False)
async def login(response: Response, request: OAuth2PasswordRequestForm = Depends()):
    username = request.username
    password = request.password
    logging.error(f"Username: {username} Password: {password}")
    print(f"Username: {username}")
    print(f"Password: {password}")

    try:
        print("Getting Token")
        token = keycloak_openid.token(username=username, password=password)
        print("The token is fine at api2/token")
        response.set_cookie("session", token)
        # response.headers['Authentication'] = token

    except KeycloakAuthenticationError as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    token = {
        "access_token": token['access_token'],
        "refresh_token": token['refresh_token'] , 
        "token_type": "bearer"
        }
    return token


@app.get("/api/get_tokens", tags=["Authentication"], dependencies=[Depends(get_current_user)])
async def read_users_me(token=Depends(oauth2_scheme)):
    return token


@app.get("/api/home", tags=['Sample response'], summary="List Documents", dependencies=[Depends(get_current_user)],
        status_code=status.HTTP_200_OK)
async def home():
    """
    RestAPI Design is yet to be completed
    """
    return {
        "message": "Welcome to the Octa-Monitor API"
    }


@app.post("/api/live", tags=["Live datas"], summary="Live data", dependencies=[Depends(get_current_user)])
async def student_status(data: Update) -> dict:
    # user = decode_token(token)
    return await Database.student_status(data)

@app.post("/api/create-class", tags=["create class"], summary="Create a new class for students", dependencies=[Depends(get_current_user)])
async def create_class(data: createClass):
    data = dict(data)
    return data

