from flask import Flask, render_template, request

app = Flask(__name__)


PIN = "1124"

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        
        pin = request.form.get("pin")

        if pin == PIN:
            
            return "SUKCES", 200
        else:
            message = "❌ Niepoprawny PIN!"

    return render_template("index.html", message=message)

if __name__ == "__main__":

    app.run(debug=True, threaded=True)