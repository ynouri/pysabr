from flask import Flask
from flask import Response
from  flask import request
app = Flask(__name__)
import sabr

# To start the Flask server in dev mode:
# $ FLASK_APP=web/app.py FLASK_DEBUG=1 python -m flask run

@app.route('/sabr')
def compute():
    k = float(request.args.get('k', 1.))
    f = float(request.args.get('f', 0.1))
    t = float(request.args.get('t', 1.))
    alpha = float(request.args.get('a', 0.1))
    beta = float(request.args.get('b', 1.))
    rho = float(request.args.get('r', -0.2))
    volvol = float(request.args.get('n', 0.5))

    vol = sabr.lognormal(k, f, t, alpha, beta, rho, volvol)
    text = "{}".format(vol)
    return Response(text, mimetype='text/html')
