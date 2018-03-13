import falcon
import sabr

# To reload server on file changes on Windows/Waitress
# $ nodemon --exec 'python -mwaitress --port=5000 web.falcon_app:app' -e py

# Test URL: http://127.0.0.1:5000/sabr?k=1.0&f=1.0&t=1.0&a=0.20&b=1.0&r=0.0&n=0.2

# Helper to get required parameters
def get_param_as_float(req, param):
     p = req.get_param(param, required=True)
     return float(p)

class SabrLognormalVolResource(object):
    def on_get(self, req, resp):
        # Default status: success
        resp.status = falcon.HTTP_200
        # GET parameters
        params = ['k', 'f', 't', 'a', 'b', 'r', 'n']
        values = list(map(lambda x: get_param_as_float(req,x), params))
        print(values)
        # Compute sabr.lognormal(k, f, t, alpha, beta, rho, volvol)
        result = sabr.lognormal(*values)
        resp.body = ('{}'.format(result))

# Callable WSGI app
app = falcon.API()

# Resource instance
sabrLognormalVol = SabrLognormalVolResource()

# Routes
app.add_route('/sabr', sabrLognormalVol)
