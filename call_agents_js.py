from flask import Flask, request, render_template_string, url_for  # Added url_for import

app = Flask(__name__)
A1 = 0
A2 = 0

@app.route("/", methods = ["GET", "POST"])
def screen1():
    global A1
    template1 = """
    <p> this is screen 1 </p>
    <p> this is Message 1 {{message1}} </p>
    <p> this is meassge from screen 1 {{message1b}} </p>
    <a href =  {{ url_for('screen2')}}> go to screen 2 </a> 
    
    
    """
    A1 = A1 + 1
    message1 =" HELLO SCREEN 1"
    message1b ="update from screen 1 send " + str(A1)
    return render_template_string(template1, message1=message1, message1b= message1b)

@app.route("/screen2", methods = ["GET", "POST"])
def screen2():
    global A2
    template2 = """
    <p> this is screen 2 </p>
    <p> this is Message 2 {{message2}} </p>
    <p> this is meassge from screen 1 {{message2b}} </p>
    <a href =  {{ url_for('screen1')}}>  go to screen 1 </a> 
  
    """
    A2 = A2 + 1
    message2 =" HELLO SCREEN 2" 
    message2b ="update from screen 1 send " + str(A2)
    
    return render_template_string(template2, message2 =message2, message2b = message2b)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5031)