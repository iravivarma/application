import pickle
import random
import string
import os
import sys
import json
from datetime import datetime, timedelta
from typing import Optional
from urllib import parse

# third party imports
# -------------------
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi import APIRouter, status, Security
from fastapi import BackgroundTasks, Request, Form, Depends
#from fastapi_mail.fastmail import FastMail
from fastapi import Header, File, Body, Query, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import (
    OAuth2,
    OAuthFlowsModel,
    get_authorization_scheme_param,
)

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from starlette.requests import Request

from jwt import PyJWTError
from jose import JWTError, jwt


from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse

from pydantic import BaseModel, EmailStr, ValidationError

from passlib.context import CryptContext
import requests as rq
import msal


from models import Users
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models, schemas
import qr_logger as qrl
from qr_logger import create_or_get_logger, log_warning, log_info


filename = 'security.log'
logging = qrl.create_or_get_logger(filename)


security_router = APIRouter()

template_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
)
#template_dir = os.path.join(template_dir, "E")
# template_dir = os.path.join(template_dir, "website")
# template_dir = os.path.join(template_dir, "templates")
# print(template_dir)

templates = Jinja2Templates(directory='templates')

SECRET_KEY = "bfdhvsdvfakuydgvfkajhsvlawegfUIFBVLjhvfulYFVsyuVFjavsfljv"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 3
COOKIE_AUTHORIZATION_NAME = "Authorization"
COOKIE_DOMAIN = 'https://fast-wave-91117.herokuapp.com/'
# give the time for each token.
# Note: it is in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# COOKIE_DOMAIN = "127.0.0.1"

PROTOCOL = "http://"
# FULL_HOST_NAME = "localhost"
FULL_HOST_NAME = "fast-wave-91117.herokuapp.com"
PORT_NUMBER = 8000



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="token",
#     scopes={"me": "Read information about the current user.", "items": "Read items."},
# )


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        auto_error: bool = False,
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )
        print(" -----------------------------------")
        print(header_scheme)
        print(cookie_scheme)
        print(" -----------------------------------")

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param
            print("the authorization in the url is {}".format("header"))

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param
            print("the authorization in the url is {}".format("cookie"))

        else:
            authorization = False
            print("the authorization in the url is {}".format(False))

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param



oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")



@security_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Takes in the OAuth2PasswordRequestForm and returns the access token.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # if isinstance(user.position, list) else [user.position]
    print(user_scope)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#30 min
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}






async def get_current_google_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    #db = get_db()
    print(token)
    qrl.log_info(logging, db)
    qrl.log_info(logging, token)

    authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    if token is not None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print("the payload is.................")
            print(payload)
            print("-----------------------------------")
            #qrl.log_info(logging, payload.__dict__)
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            #token_scopes = payload.get("scopes", [])
            #print(token_scopes)
            #print(payload.get('scopes'))
            token_data = schemas.TokenData(username=email)
        except (JWTError, ValidationError):
            return credentials_exception
        print("I am the current_user")
        print(email)
        if email is not None:
            authenticated_user = crud.authenticate_user_email(db, email)
            print(authenticated_user.id)
            #if authenticated_user.position == 'owner':
            course_names = crud.get_courses_by_username(db, authenticated_user.id)
                #print(course_names)
            return schemas.CoursesScope(email = authenticated_user.email, courses = course_names)
            #else:
                #return schemas.CoursesScope(email = authenticated_user.email, position = authenticated_user.position, courses=[])
            # user = authenticated_user
            # print(user.__dict__)
            # print("printing the scopes...............")

            # scope_status = False
            
            # if len(token_data.scopes) >= 1 :
            #     scope_status = all(i in security_scopes.scopes for i in token_data.scopes)


            #if scope_status == False:
                


            # for scope in security_scopes.scopes:
            #     print(scope)
            #     print(security_scopes.scopes)
            #     print(token_data.scopes)
            #     if scope not in token_data.scopes:
            #         raise HTTPException(
            #             status_code=status.HTTP_401_UNAUTHORIZED,
            #             detail="Not enough permissions",
            #             headers={"WWW-Authenticate": authenticate_value},
            #         )
                    
            #return user#crud.get_user(db, user.name).first()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """This verifies that the hashed_password in DB is same as what user enters."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Generates hash for the password."""
    return pwd_context.hash(password)





def authenticate_user(db, username: str, password: str):
    """
    First gets the user with get_user function, then
    verifies its password with the password entered at the front end.

    Parameters
    ----------
    username : str
        The username that the user entered.
        
    password : str
        The password entered by the user.

    Returns
    -------
    user : UserInDB
        The user info.
    """
    user = crud.get_user(db, username)
    print(user)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user



def get_current_active_user(current_user: schemas.CoursesScope = Depends(get_current_google_user)):
    # , current_google_user: User = Depends(get_current_google_user)
    """
    """
    print("the current active user is.......")
    print(current_user)
    qrl.log_info(logging,current_user)
    return current_user



@security_router.get("/login")
def login_user_page(request: Request, redirect_url: Optional[str]=None, db: Session = Depends(get_db)):
    """Redirects to the user login or sign in page"""
    if redirect_url is None:
        redirect_url = "/userbase"
    #auth_url = _build_auth_url(scopes=SCOPE,state="/"+redirect_url)
    print("Redirect url",redirect_url)
    return templates.TemplateResponse("login.html", {"request": request, "redirect":redirect_url})
    



@security_router.get("/profile")
async def get_profile(request : Request, current_user: schemas.CoursesScope = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if not current_user:
        return JSONResponse({'status_code' : status.HTTP_401_UNAUTHORIZED,
            'detail': 'User not loggedin'})
    data = crud.get_user_email(db, current_user.email)#.__dict__
    print("printing the profile.......")
    print(data.__dict__)
    return JSONResponse({'status_code' : status.HTTP_200_OK,
            'data': json.dumps(data.__dict__),
            'detail': 'user login'})


@security_router.post("/authenticate", response_model=schemas.Token)
async def check_user_and_make_token(request: schemas.authenticate_schema, db: Session = Depends(get_db)):
    # formdata = await request.form()
    # print(request)
    # print(formdata)
    #print("the scopes are .......")
    #print(formdata.scopes)
    # print(formdata["username"],formdata["password"])
    authenticated_user = authenticate_user(db, request.email,request.password)
    print(request.email)
    print(authenticated_user)
    if authenticated_user is None:
        return JSONResponse({'status_code':status.HTTP_401_UNAUTHORIZED,
            'detail':"Invalid username or password"})

    if authenticated_user.active_yn==False:
        return JSONResponse({
            'status_code':status.HTTP_401_UNAUTHORIZED,
             'detail':"User Not Activated. Please verify email"
             })


    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    log_info(logging, authenticated_user.email)

    # user_scope = authenticated_user.position# if isinstance(authenticated_user.position, list) else [authenticated_user.position]
    # print("the user scope is........")
    # print(user_scope)
    access_token = create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )

    #################### SUCCESSFULLY LOGED IN USING CUSTOM DETAILS ######################
    #crud.logged_in(authenticated_user.id,"custom",request)

    token = jsonable_encoder(access_token)
    print("token is----------------------")
    print(token)
    response = JSONResponse({"access_token": token, "token_type": "bearer"})
    
    response.set_cookie(
        key=COOKIE_AUTHORIZATION_NAME,
        value=f"Bearer {token}",
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=10800,          # 3 hours
        expires=10800,          # 3 hours
    )
    print(response.__dict__)
    return response

@security_router.get("/logout")
async def logout_and_remove_cookie(request: Request, current_user: schemas.NewUser = Depends(get_current_active_user), db: Session = Depends(get_db)) -> "RedirectResponse":
    response = JSONResponse({
        'status_code':status.HTTP_401_UNAUTHORIZED,
        'url':'/login',
        'detail':'not logged in to logout.'})

    # if not current_user:
    if current_user is None:
        return response
    # usertype = crud.get_user_third_party(current_user.email)
    # if usertype=="google":
    #     return templates.TemplateResponse("google_signout.html", {"request": request})
    # else:
    response.delete_cookie(key=COOKIE_AUTHORIZATION_NAME, domain=COOKIE_DOMAIN)
    #crud.logged_out(current_user.email)
    # return templates.TemplateResponse("logout.html",{"request":request, "instanceid":"13917092-3f6f-49e5-b39b-e21c89f24565"})
    return response


@security_router.get("/me")
async def get_mine(request: Request, current_user: schemas.CoursesScope = Depends(get_current_active_user), db: Session = Depends(get_db) ):
    log_info(logging, "hello please loge me in..........")
    log_info(logging, current_user)
    return current_user


@security_router.get("/new_user_signup")
async def enter_new_user(request: Request):
    """Redirects to the New user sign up page"""

    return templates.TemplateResponse("signup.html", {"request": request})


@security_router.post("/new_user/")
async def newUser(user: schemas.user_item = Depends(), redirect_url:Optional[str]=None, db: Session = Depends(get_db)):
    #try:
    user.password = get_password_hash(user.password)
    print("printing the hashed_password")
    print(get_password_hash(user.password))
    print("print the nortmal details")
    print(user.__dict__)
    try:
        inserted_user = crud.create_user(db, user)
        
        # print("user details..........")
        # print(inserted_user.__dict__)
        return JSONResponse({'status_code': status.HTTP_201_CREATED,
                            'detail':'Account Created SUCCESSFULLY'})

    except:
        print("user already existed..........")
        return JSONResponse({
            'status_code':status.HTTP_409_CONFLICT,
            'detail':'User Already Exists'
            })

    #return inserted_user
    # except:
    #     raise HTTPException(status_code=409, detail="Invalid username/password or user already exists")
    # #event_processor("SignUp",inserted_user)
    # if redirect_url:
    #     return RedirectResponse(url=f"/login?redirect_url={redirect_url}", status_code=status.HTTP_303_SEE_OTHER)
    # return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)



def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        '''
DateTime.UtcNow tells you the date and time as it would be in Coordinated Universal Time, 
which is also called the Greenwich Mean Time time zone. and used for to store the dates and time.
'''
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



##############################################################
############reset or update password apis#####################

def send_email(background_tasks: BackgroundTasks, email, code, request: Request):
    """Sends an email with a defined template containing the passcode.

    Email is intialized at '/enter_recovery_email' endpoint as global.
    You have to fill in here your email and password from which you want
    to send the mail (GMAIL).

    Parameters
    ----------
    background_tasks : BackgroudTasks
        For sending the mail in the background.
    request : Request
        For using JinJaTemplates as a response.

    Returns
    -------
    template : Jinaja Template
        Returns the template "after_email_sent_response.html".
    """

    template = """
        <html>
        <body>
        <p>Hi !!!
        <br>Thanks for using Workeeper</p>
        <p> Your passcode is : %s </p>
        </body>
        </html>
        """ % (
        code
    )

    conf = ConnectionConfig(
    MAIL_USERNAME='krishnardt365@gmail.com',
    MAIL_PASSWORD="google@1A0",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False)


    message = MessageSchema(

        subject="password recovery",

        recipients=[email],  # List of recipients, as many as you can pass  

        body=template,

        subtype="html"

    )


    
    fm = FastMail(conf)

    #await fm.send_message(message)

    background_tasks.add_task(
        fm.send_message,
        message
    )

    return templates.TemplateResponse(
        "after_email_sent_response.html", {"request": request}
    )


@security_router.get("/enter_recovery_email")
async def get_email(request: Request):
    """Returns the homepage template where you enter your email - 'enter_email_for_recovery.html'"""

    return templates.TemplateResponse(
        "enter_email_for_recovery.html", {"request": request}
    )



def get_random_alphanumeric_string(length):
    """Generates a random alphanumeric string of given length.

    Parameters
    ----------
    length : int
        The length of random string to be generated.

    Returns
    -------
    result_str : string
        A random string of the length given.
    """

    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    return result_str




@security_router.post("/send_mail")
async def send_mail(
    background_tasks: BackgroundTasks,
    request: Request,
    email_schema: schemas.EmailSchema = Depends(), db: Session = Depends(get_db)
):
    """End-point to send the mail.

    Generates the security-code and then calls the send_email function.

    Parameters
    ----------
    background_tasks : BackgroudTasks
        For sending the mail in the background.
    request : Request
        For using JinJaTemplates as a response.
    email_schema : EmailSchema
        Schema to get the email of user.

    Returns
    -------
    template : Jinaja Template
        Calls the send_email funtion which returns the template.
    """

    #global code, Email#
    #print(email_schema.__dict__)
    email = email_schema.__dict__['email']
    code = get_random_alphanumeric_string(10)
    crud.update_code(db, email, code)

    return send_email(background_tasks, email, code, request)


@security_router.get("/send_mail_again")
def send_mail_again(background_tasks: BackgroundTasks, request: Request):
    """Resends the mail when user clicks in the resend email button."""

    code = get_random_alphanumeric_string(10)
    crud.update_code(db, email, code)

    return send_email(background_tasks, email, code, request)

"""
Have to linkup with database...
users database has to be updated with new columns
columns: is_active, recent_login, recovery_passcode, recovered_yn
once the user asks for recovery_passcode, the recovered_yn has to be set as False
and the new generated passcode will be updated at recovery_passcode field

when user changes the password successfully, recovered_yn has to be True


"""
@security_router.post("/account_recovery/")
async def verify_passcode(request: Request, passcode_schema: schemas.SentPasscode = Depends(), current_user: schemas.NewUser = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Checks if the passcode entered by the user is correct or not.

    Parameters
    ----------
    request : Request
        For using JinJaTemplates as a response.
    passcode_schema : SentPasscode
        schema to get the passcode entered by the user.

    Returns
    -------
    template : Jinaja Template
        Returns the "failed_verification.html" or
        "successful_verification_result.html" templates.
    """

    result = ""
    email = current_user.email
    code = crud.get_code(db, email)
    if passcode_schema.passcode == code:
        result = "successful"

        # give the result of passcode validation
        return templates.TemplateResponse(
            "successful_verification_result.html",
            {"request": request, "result": result},
        )
    else:
        result = "failed"

        return templates.TemplateResponse(
            "failed_verification.html", {"request": request, "result": result}
        )


@security_router.get("/re_enter_passcode")
async def re_enter_passcode(request: Request):
    """Redirects to "after_email_sent_response.html for re-entering of the passcode."""

    return templates.TemplateResponse(
        "after_email_sent_response.html", {"request": request}
    )


@security_router.get("/check_links")
async def check_links():
    return {"this is merge checking purpose"}


@security_router.get("/change_password")
async def after_successful_verification(request: Request):
    """Redirects to 'enter_new_password.html' for taking the new password
        of the user after forgot password email verification successful"""

    return templates.TemplateResponse("enter_new_password.html", {"request": request})


@security_router.post("/change_user_password")
async def update_password(new_password_schema: schemas.NewPassword = Depends(), db: Session = Depends(get_db)):
    """Calls the update function for the password from the crud module.

    Parameters
    ----------
    new_password_schema : NewPassword
        schema to get the password entered by the user.

    Returns
    -------
    For now just a json response to say updation successful.
    Later will be used to redirect it to the HOME PAGE of
    user's account at workeeper.
    """
    details = new_password_schema.__dict__
    print(details)
    recovery_status = crud.get_recovery_status(db, "krishnardt365@gmail.com")
    print(recovery_status)
    if details['password1'] == details['password2'] and recovery_status==False:
        password = get_password_hash(details['password1'])
        update_result = crud.change_user_password(db, "krishnardt365@gmail.com", password)
        return update_result
    else:
        return HTTPException(
                    status_code=HTTP_403_FORBIDDEN,  detail="not updated successfully"
                )
    #event_dict = {}
    #event_dict['Email']=Email
    #event_processor("PasswordUpdation",event_dict)

    return {"password updation": "successful"}




###########################################################################
'''
update password is working fine..
Except only thing has to be changed is get_current user...
Once the custom login works fine...we can get the current active user..
'''

@security_router.get("/update_password")
async def after_successful_verification(request: Request):
    """Redirects to 'enter_new_password.html' for taking the new password
        of the user after forgot password email verification successful"""

    return templates.TemplateResponse("enter_new_password.html", {"request": request})


@security_router.post("/update_user_password")
async def update_password(new_password_schema: schemas.NewPassword = Depends(), current_user: schemas.NewUser = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Calls the update function for the password from the crud module.

    Parameters
    ----------
    new_password_schema : NewPassword
        schema to get the password entered by the user.

    Returns
    -------
    For now just a json response to say updation successful.
    Later will be used to redirect it to the HOME PAGE of
    user's account at workeeper.
    """
    details = new_password_schema.__dict__
    print(details)
    if details['password1'] == details['password2']:
        password = get_password_hash(details['password1'])
        update_result = crud.update_user_password(db, current_user.email, password)
        return update_result
    else:
        return JSONResponse({
                    'status_code':status.HTTP_403_FORBIDDEN,  "detail": "not updated successfully"
                })
    #event_dict = {}
    #event_dict['Email']=Email
    #event_processor("PasswordUpdation",event_dict)

    return {"password updation": "successful"}
