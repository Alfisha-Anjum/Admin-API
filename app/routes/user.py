from fastapi import APIRouter, HTTPException, Depends
from app.model.user import *
from app.config.db import *
from app.schemas.user import *
from app.main import *
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/admin-register", tags=["Admin-Page"])
async def register(newUser: Admin):
    try:
        existing_user = admin.find_one({"email": newUser.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if len(str(newUser.mobile)) != 10:
            raise HTTPException(status_code=400, detail="Contact number must be of 10 digits")
             
        admin_data = newUser.model_dump()  
        res = admin.insert_one(admin_data)

        return {"status_code": 201, "message": "User registered successfully", "user_id": str(res.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    


@router.get("/admin-gel-all", tags=["Admin-page"])
async def get_all_admin():
    all_admin = admin.find()
    return mineadmin(all_admin)

@router.get("/find-one", tags=["Admin-page"])
async def find_one_admin(id:str):
    all_admin = admin.find_one({"_id": ObjectId(id)})
    return myadmin(all_admin)


# @router.get("/admin/{id}", tags=["Admin-page"])
# def get_id(id: str): 
#     user = admin.find_one({"_id": ObjectId(id)})
#     if user is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     all_admin = {**user, "_id": str(user["_id"])}

#     return {
#         "status": "ok",
#         "data": all_admin
#     }

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
