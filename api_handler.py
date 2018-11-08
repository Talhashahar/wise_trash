from flask import Flask
import googleAPI_handler
import db_handler

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"



if __name__ == "__main__":
    app.run()