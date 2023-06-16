from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # retrieve items from database

    if request.method == "GET":
        return render_todo()

    # add new item

    # edit existing item

    # delete existing item

    return render_todo(form_values=request.form.to_dict())

def render_todo(form_values={}, items={}):
    return render_template(
        "index.html.j2",
        css_path=url_for("static", filename="style.css"),
        form_values=form_values,
        items={"1": "Item 1", "2": "Item 2", "3": "Item 3"}
    )




# app.add_route("/lists", Lists())
# app.add_route("/lists/{list_id}", List())
# app.add_route("/lists/{list_id}/items", ListItems())
# app.add_route("/lists/{list_id}/items/{item_id}", ListItem())
# app.add_route("/lists/{list_id}/items/{item_id}/tasks", ListItemTasks())
# app.add_route("/lists/{list_id}/items/{item_id}/tasks/{task_id}", ListItemTask())
