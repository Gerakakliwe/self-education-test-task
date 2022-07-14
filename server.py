# Import modules
import config
from flask import render_template

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# Create a URL route to configure the endpoints
@connex_app.route("/")
def home():
    """
    This function responds to the browser URL
    localhost:5000/

    :return:    The rendered template "home.html"
    """
    return render_template("home.html")


if __name__ == "__main__":
    connex_app.run(debug=True)
