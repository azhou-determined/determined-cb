
from flask import Flask

app = Flask(__name__)

app.config.from_pyfile("config.py")

# Import routes from separate file
import routes

if __name__ == "__main__":
	app.run()