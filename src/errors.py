from app import app

# Page not found
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# Bad request
@app.errorhandler(400)
def bad_request(e):
    return "<h1>400</h1><p>Your request is missing parameters.</p>", 400

# Resource already exist
@app.errorhandler(409)
def already_exist(e):
    return "<h1>409</h1><p>The resource already exists.</p>", 409