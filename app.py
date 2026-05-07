from flask import Flask, render_template
from calculator import calc_bp
from formulas import physics_library

app = Flask(__name__)
app.register_blueprint(calc_bp)

@app.route('/')
def index():
    return render_template('index.html', library=physics_library)

# NEW: Explain endpoint (proxies to calculator)
@app.route('/api/explain', methods=['POST'])
def explain_proxy():
    """Proxy to calculator blueprint's explain endpoint."""
    from flask import request
    # Forward the request to blueprint
    return calc_bp.make_response(calc_bp.view_functions['calculator.explain_calculation'](request))

if __name__ == '__main__':
    app.run(debug=True, port=5000)