from flask import Flask, render_template, request, url_for
from database import database, database_post
from markupsafe import escape

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Profile_pic'


@app.route("/")
def login():
    return render_template("login.html.jinja")


@app.route("/register")
def register():
 
   return render_template("register.html.jinja")

@app.route("/login", methods=["GET", "POST"])
def logged():
    if request.method == "POST":
        user = request.form["name"]
        user = user.replace(" ", "%")
        psw = request.form["password"]
        if database.check_user(nm=user,psw=psw):
            return render_template("logged.html.jinja", log="Login Succesfully", URL=f"/home<{escape(database.give_user_info(user)[2])}")
        else:
            return render_template("logged.html.jinja", log="Login Unsuccesfully", URL="/")
    return "Errore"


@app.route("/registered", methods=["GET", "POST"])
def registered():
    if request.method == "POST":
        user = request.form["name"]
        user = user.replace(" ", "%")
        psw = request.form["password"]
        profile_pic = request.files["profile"]
        file_path = f"./static/Profile_pic/{profile_pic.filename}"
        profile_pic.save(file_path)
        if database.add_user(nm=user, psw=psw, filename=profile_pic.filename):
            return render_template("logged.html.jinja", log="Register Succesfully", URL=f"/home<{escape(database.give_user_info(user)[2])}")
        else:
            return render_template("logged.html.jinja", log="Register Unsuccesfully", URL="/register")
    return "Errore"


@app.route("/home<id>")
def home(id):
    id = id.replace("<" , "")
    id = id.replace(">" , "")
    profile = database.give_user_info_with_id(id)
    path = url_for('static', filename=f"Profile_pic/{profile[1]}")
    posts = database_post.take_post()
    posts = posts[::-1]
    return render_template("home.html.jinja", user=escape(profile[0]), prof=path, posts=posts, id=id)

@app.route("/menu")
def menu():
    return render_template("menu.html.jinja")

@app.route("/new_post<id>")
def new_post(id):
    id = id.replace("<" , "")
    id = id.replace(">" , "")
    profile = database.give_user_info_with_id(id)[1]
    profile = profile.replace(" ", "%")

    return render_template("new_post.html.jinja", user=database.give_user_info_with_id(id)[0], profile=profile, id=id)

@app.route("/posted", methods=["GET", "POST"])
def posted():
    if request.method == "POST":
        user = request.form["user"]
        profile = request.form["profile_pic"]
        post = request.form["post"]
        database_post.add_post(user, post, profile)
        return render_template("logged.html.jinja", log="Posted Succesfully", URL=f"/home<{database.give_user_info(user)[2]}")
    return "Errore"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
