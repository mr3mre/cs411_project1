from flask import Flask

from src.routes import bp

# Create flask app
app = Flask(__name__)
app.secret_key = "CS_411_Project_1"
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run()