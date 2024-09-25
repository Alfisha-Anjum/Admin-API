from fastapi import APIRouter, HTTPException,Query
from app.model.user import *
from app.config.db import *
from app.schemas.user import *
from app.main import *
from bson.objectid import ObjectId
import smtplib
import hashlib
#importing emailMessage
from email.message import EmailMessage 
from fastapi import WebSocket

router = APIRouter()

# EMAIL_ADDRESS = 'anjumalfisha@gmail.com'
# EMAIL_PASSWORD = 'vzgz szjn cykj ngka'

# def send_email(subject, body, to):
#     msg = EmailMessage()
#     msg.set_content(body)
#     msg['Subject'] = subject
#     msg['From'] = EMAIL_ADDRESS
#     msg['To'] = to

#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.starttls() 
#         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  
#         smtp.send_message(msg) 


@router.post("/admin-register", tags=["Admin-Page"])
async def register(newUser: Admin):
    try:
        existing_user = admin.find_one({"email": newUser.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if len(str(newUser.mobile)) != 10:
            raise HTTPException(status_code=400, detail="Contact number must be 10 digits")


        hashed_password = hashlib.sha256(newUser.password.encode()).hexdigest()
        newUser.password = hashed_password 

        admin_data = newUser.model_dump()
        res = admin.insert_one(admin_data)

        # subject = "Registration Successful"
        # body = f"Dear {newUser.full_name},\n\nYou have successfully registered as an admin.\n\nRegards,\nTeam"
        # to = newUser.email

        # send_email(subject, body, to)

        return {"status_code": 201, "message": "User registered successfully", "user_id": str(res.inserted_id)}

    except Exception as e:
       
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    




EMAIL_ADDRESS = 'abuzaryaseen@gmail.com'
EMAIL_PASSWORD = 'gyii sfoc myzl ushv'

def send_email(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = f"Portfolio <{EMAIL_ADDRESS}>"  # Modify this line
    msg['To'] = to

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls() 
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  
        smtp.send_message(msg) 

@router.post("/yaseen-register", tags=["Yaseen"])
async def register(newUser: Yaseen):
    try:
        admin_data = newUser.model_dump()
        res = admin.insert_one(admin_data)

        subject = "Registration Successful"
        body = (
            f"Dear {newUser.full_name},\n\n"
            f"Hello! Yaseen There is a message for you.\n\n"
            f"Your details:\n"
            f"Full Name: {newUser.full_name}\n"
            f"Email: {newUser.email}\n"
            f"Message: {newUser.message}\n\n"
            "Regards,\nTeam"
        )
        to = newUser.email

        send_email(subject, body, to)

        return {"status_code": 201, "message": "User registered successfully", "user_id": str(res.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")




# Login API
@router.post("/admin-login", tags=["Admin-Page"])
async def login(login_data: Login):
    try:
       
        existing_user = admin.find_one({"email": login_data.email})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

       
        hashed_password = hashlib.sha256(login_data.password.encode()).hexdigest()

        if existing_user['password'] != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        subject = "Login Successful"
        body = f"Dear {existing_user['full_name']},\n\nYou have successfully logged in.\n\nRegards,\nTeam"
        to = login_data.email
        send_email(subject, body, to)

        return {"status_code": 200, "message": "Login successful"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    
    
websocket_list = []
@router.websocket("/WS")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if websocket not in websocket_list:
        websocket_list.append(websocket)
    while True:
        data = await websocket.receive_text()
        for websocket in websocket_list:
            if websocket != websocket:
                await websocket.send_text(f"{data}")

@router.get("/gel-all-admin", tags=["Admin-page"])    
async def get_all_admin(limit: int = Query(5, ge=1), offset: int = Query(0, ge=0)):
 all_admin = admin.find().skip(offset).limit(limit)
 return mineadmin(all_admin)





@router.get("/find-one", tags=["Admin-page"])
async def find_one_admin(id:str):
    all_admin = admin.find_one({"_id": ObjectId(id)})
    return myadmin(all_admin)


@router.patch("/updateAdmin/{id}", tags=["Admin-page"])
def updateAdmin(id: str, newUser:Admin):
    if len(str(newUser.mobile)) != 10:
        raise HTTPException(status_code=400,detail="Contact number must be of 10 digits")
    admin.find_one_and_update(
        {"_id" : ObjectId(id)},
        {"$set": dict(newUser)}
    )
    return {
        "status" : "ok" ,
        "messege" : "Data have been updated"
    }

@router.delete("/deleteAdmin/{id}", tags=["Admin-page"])
def deleteAdmin(id: str):   
    user = admin.find_one_and_delete({"_id": ObjectId(id)})
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "status": "ok",
        "message": "Data has been deleted"
    }
