import psycopg2
import psycopg2.extras
import tomllib
from flask import Flask, g, render_template, request, url_for

app = Flask(__name__, instance_relative_config=True)


##
## Request Lifecycle Functions
##

@app.before_request
def load_config():
    app.config.from_file("config.toml", load=tomllib.load, text = False)

@app.before_request
def db_connect():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=app.config["DATABASE"]["hostname"],
            port=app.config["DATABASE"]["port"],
            dbname=app.config["DATABASE"]["database"],
            user=app.config["DATABASE"]["username"],
            password=app.config["DATABASE"]["password"],
        )

@app.teardown_request
def close_db(error):
    if error is None:
        db = g.pop('db', None)

        if db is not None:
            db.close()


##
## Route Functions
##

@app.get("/")
def index_get():
    return render_todo(items=get_items())

@app.post("/")
def index_post():
    complete = request.form.get("complete")
    create = request.form.get("create")
    description = request.form.get("description")
    error = None
    remove = request.form.get("remove")
    save = request.form.get("save")

    if create:
        if description.strip() != "":
            create_item(description)
        else:
            error = "Can't create an empty To Do item."

    elif complete:
        complete_item(complete)

    elif save:
        update_item(save, description)

    elif remove:
        delete_item(remove)

    return render_todo(
        form_values=request.form.to_dict(),
        items=get_items(),
        error=error
    )


##
## Action Functions
##

def complete_item(id):
    cur = g.db.cursor()
    cur.execute("UPDATE item SET is_completed = TRUE WHERE id = %s;", (id,))
    g.db.commit()
    cur.close()

def create_item(description):
    cur = g.db.cursor()
    cur.execute("INSERT INTO item (description) VALUES (%s);", (description,))
    g.db.commit()
    cur.close()

def delete_item(id):
    cur = g.db.cursor()
    cur.execute("DELETE FROM item WHERE id = %s;", (id,))
    g.db.commit()
    cur.close()

def get_items():
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT id, description, is_completed FROM item ORDER BY id;")
    results = cur.fetchall()
    cur.close()

    return results

def render_todo(form_values=None, items=None, error=None):
    return render_template(
        "index.html.j2",
        css_path=url_for("static", filename="style.css"),
        error=error,
        form_values=form_values,
        items=items,
    )

def update_item(id, description):
    cur = g.db.cursor()
    cur.execute("UPDATE item SET description = %s WHERE id = %s;", (description, id))
    g.db.commit()
    cur.close()
