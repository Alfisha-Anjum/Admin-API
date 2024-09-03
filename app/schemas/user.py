def myadmin(item) -> dict :
    return{
        "id":str(item["_id"]),
        "full_name":item["full_name"],
        "email": item["email"],
        "mobile":item["mobile"],
           
    }
def mineadmin(items):
    return [myadmin(item) for item in items] 