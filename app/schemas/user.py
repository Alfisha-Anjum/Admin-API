def myadmin(item) -> dict :
    return{
        "id":str(item["_id"]),
        "first_name":item["first_name"],
        "last_name": item["last_name"],
        "email": item["email"],
        "mobile":item["mobile"],
           
    }
def mineadmin(entity):
    return [myadmin(item) for item in entity] 