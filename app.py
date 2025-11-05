from flask import Flask, render_template, request, send_from_directory, redirect
import os
import uuid
from datetime import datetime
from database_manager import add_entry, get_data, delete_entry

app = Flask(__name__)

def show_data(paste_obj):
    """Display paste data and handle expiry or burn-after-read logic."""
    current_time = datetime.now().timestamp()

    # Expiry check
    if current_time > float(paste_obj.expiry):
        delete_entry(paste_obj.paste_id)
        return render_template("404.html")

    # Burn after read
    if paste_obj.burn_after_read:
        delete_entry(paste_obj.paste_id)
        return render_template(
            "view_paste.html",
            paste_id=paste_obj.paste_id,
            title=paste_obj.title,
            content=paste_obj.content,
        )

    # Normal view
    return render_template(
        "view_paste.html",
        paste_id=paste_obj.paste_id,
        title=paste_obj.title,
        content=paste_obj.content,
    )


def generate_uid():
    """Generate a short unique ID for paste."""
    new_uuid = uuid.uuid4()
    return str(new_uuid)[:4]


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        syntax = request.form.get("syntax")
        expiration = request.form.get("expiration")
        is_password_protected = request.form.get("is_password_protected") == "on"
        password = request.form.get("password")
        burn_after_read = request.form.get("burn_after_read") == "on"

        uid = generate_uid()
        current_epoch = datetime.now().timestamp()

        expiration_mapping = {
            "never": 333400450405,
            "3h": current_epoch + 10800,
            "24h": current_epoch + 86400,
            "1w": current_epoch + 604800,
            "1m": current_epoch + 2678400,
            "30s": current_epoch + 30,
        }

        expiry_time = expiration_mapping.get(expiration, 333400450405)

        add_entry(
            uid,
            title,
            content,
            expiry_time,
            is_password_protected,
            password,
            syntax,
            burn_after_read,
        )

        return redirect(f"/{uid}")

    return render_template("create.html")


@app.route("/<uid>", methods=["GET", "POST"])
def view_paste(uid):
    paste_obj = get_data(uid)

    if not paste_obj:
        return render_template("404.html")

    # Password protected logic
    if paste_obj.is_password_protected == 'true':
        if request.method == "GET":
            return render_template("password.html")

        elif request.method == "POST":
            user_password = request.form.get("password")
            if user_password == str(paste_obj.password):
                return show_data(paste_obj)
            else:
                return render_template("password.html")

    # Normal (not password protected)
    return show_data(paste_obj)


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


