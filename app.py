from flask import Flask

app = Flask(__name__)

@app.route("/")
def test():
    print("This is a test of the engine...")
