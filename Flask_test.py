from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = "Enter your name below:"
    if request.method == "POST":
        name = request.form["name"]
        message = f"Hello, {name}!"
    
    html = """ 
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Name Capture</title>
    </head>
    <body>
        <h2>{{ message }}</h2>
        <form action="/" method="POST">
            <input type="text" name="name" required>
            <button type="submit">Submit</button>
        </form>
        <a href="page2">Next page</a>
    </body>
    </html>
    """
    
    return render_template_string(html, message=message)


@app.route("/page2")
def page2():
    name = request.args.get("name", "Guest")  # Get name from query string or use "Guest"
    message = f"{name}, this is page 2"
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Page 2</title></head>
    <body>
        <h2>{{ message }}</h2>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(html, message=message)

if __name__ == "__main__":
    app.run(debug=True)

