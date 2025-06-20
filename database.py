from tinydb import TinyDB, Query
from better_profanity import profanity
from cryptography.fernet import Fernet

key = b'UF8ofzIpXvMP6gv0bOL-qyVCrvHEwoVdm9fRcLW8l74='
fernet = Fernet(key)
class database():

    def add_user(nm: str, psw: str, filename: str):
        db = TinyDB("./static/db.json")
        nm = nm.replace(" ", "%")
        info = Query()
        id = fernet.encrypt(f"{nm}".encode())
        if db.search(info.name == nm) == []:
            db.insert({"name": nm, "password": psw, "filename": filename, "id": id.decode()})
            return True
        else:
            return False
    
    def check_user(nm: str, psw: str):
        db = TinyDB("./static/db.json")
        info = Query()
        nm = nm.replace(" ", "%")
        if db.search(info.name == nm) != [] and db.search(info.password == psw) != []:
            return True
        else:
            return False

    def give_user_info(nm: str):
        db = TinyDB("./static/db.json")
        info = Query()
        nm = nm.replace(" ", "%")
        data = db.search(info.name == nm)
        if data:
            for record in data:
                return [record["name"], record["filename"], record["id"]]
            
    def give_user_info_with_id(id: str):
        db = TinyDB("./static/db.json")
        info = Query()
        id = id.replace(" ", "%")
        data = db.search(info.id == id)
        if data:
            for record in data:
                return [record["name"], record["filename"], record["id"]]
    
class database_post():
    def add_post(name: str, post: str, img_profile: str):
        post_db = TinyDB("./static/post.json")
        img_profile = img_profile.replace("%", " ")
        name = name.replace("%", " ")
        post = profanity.censor(post)
        post_db.insert({"name": name, "post": post, "img_profile": f"Profile_pic/{img_profile}"})
        return True
    
    def take_post():
        post_db = TinyDB("./static/post.json")
        all_post = post_db.all()
        return all_post
