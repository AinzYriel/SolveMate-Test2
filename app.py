from flask import Flask, render_template, request
from calculator import calc_bp
from formulas import physics_library

app = Flask(__name__)
app.register_blueprint(calc_bp)

@app.route('/')
def index():
    return render_template('index.html', library=physics_library)

# FIXED: Remove the broken proxy - blueprint handles routing directly
# The blueprint's /api/explain endpoint is already accessible at /api/explain

if __name__ == '__main__':
    app.run(debug=True, port=5000)
