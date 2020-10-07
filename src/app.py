import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = '3628e8ec01b81c2d9e01e55f'