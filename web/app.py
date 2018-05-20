import falcon
import pysabr.models.hagan_2002_lognormal_sabr as sabr
import logging


logging.basicConfig(level=logging.INFO)


# Helper to get required parameters
def get_param_as_float(req, param):
    p = req.get_param(param, required=True)
    return float(p)


# /sabr
# Test URL:
# http://127.0.0.1:5000/sabr?k=1.0&f=1.0&t=1.0&a=0.20&b=1.0&r=0.0&n=0.2
class SabrLognormalVolResource(object):
    def on_get(self, req, resp):
        # Default status: success
        resp.status = falcon.HTTP_200
        # GET parameters
        params = ['k', 'f', 't', 'a', 'b', 'r', 'n']
        values = list(map(lambda x: get_param_as_float(req, x), params))
        logging.info("SABR Lognormal vol: " + str(values))
        # Compute sabr.lognormal(k, f, t, alpha, beta, rho, volvol)
        result = sabr.lognormal_vol(*values)
        resp.body = ('{}'.format(result))


# /alpha
# Test URL:
# http://127.0.0.1:5000/alpha?v=0.6&f=1.0&t=1.0&b=1.0&r=0.0&n=0.2
class SabrAlphaResource(object):
    def on_get(self, req, resp):
        # Default status: success
        resp.status = falcon.HTTP_200
        # GET parameters
        params = ['v', 'f', 't', 'b', 'r', 'n']
        values = list(map(lambda x: get_param_as_float(req, x), params))
        logging.info("Alpha: " + str(values))
        # Compute sabr.lognormal(v, f, t, beta, rho, volvol)
        result = sabr.alpha(*values)
        resp.body = ('{}'.format(result))


# Callable WSGI app
app = falcon.API()

# Resource instance
sabr_ln_vol_resource = SabrLognormalVolResource()
sabr_alpha = SabrAlphaResource()

# Routes
app.add_route('/sabr', sabr_ln_vol_resource)
app.add_route('/alpha', sabr_alpha)
