from tinydb import TinyDB, Query
from better_profanity import profanity
class database():

    def add_user(nm: str, psw: str, filename: str):
        db = TinyDB("./static/db.json")
        nm = nm.replace(" ", "%")
        info = Query()
        if db.search(info.name == nm) == []:
            db.insert({"name": nm, "password": psw, "filename": filename})
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
                return [record["name"], record["filename"]]
    
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