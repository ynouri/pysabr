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


"""
VBA wrapper:

Option Explicit
Option Base 1

Public Function LogNormal_SABR_Web(k As Double, f As Double)

    ' , f As Double, t As Double, Alpha As Double, Beta As Double, Rho As Double, Vovol As Double
    Dim SABR_service_url As String
    Dim result As Double

    SABR_service_url = "http://127.0.0.1:5000/sabr?k=" & k & "&f=" & f
    result = WorksheetFunction.WebService(SABR_service_url)
    LogNormal_SABR_Web = result * 100

End Function
"""
