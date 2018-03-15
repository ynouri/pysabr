# pySABR
Python implementation of SABR model.

# Introduction
SABR (Stochastic Alpha Beta Rho) is a financial volatility smile model widely used for interest rates options such as swaptions or cap/floors. This Python library implements its Hagan 2002 specification. For more information about the model itself, please consult the [original paper](/doc/Hagan - Managing Smile Risk.pdf) or [Wikipedia](https://en.wikipedia.org/wiki/SABR_volatility_model).

# Requirements
Core pySABR functions require `numpy` & `scipy` to run. The web microservice is based on `falcon`, which can itself be run with `waitress` (Windows) or `gunicorn` (Linux). Finally, the Excel function wrapper for the web microservice requires Windows and Excel 2013+.

# Examples

Interpolate a shifted-lognormal volatility:
```Python
import sabr
[s, k, f, t, alpha, beta, rho, volvol] = [0.03, 0.02, 0.025, 1.0, 0.025, 0.50, -0.24, 0.29]
vol = sabr.lognormal(k + s, f + s, t, alpha, beta, rho, volvol)
```

Calibrate alpha from the ATM lognormal vol:
```Python
import sabr
```

Calibrate alpha, rho and volvol from a discrete smile:
```Python
import sabr
```

Compute an option premium using Black formula:
```Python
import sabr
```

# Web microservice

pySABR includes a web microservice exposing the two main functions of the library: volatility interpolation and alpha calibration. Those two
functions are available through a simple REST API:

```bash
# Returns a lognormal vol
curl http://127.0.0.1:5000/sabr?k=1.0&f=1.0&t=1.0&a=0.20&b=1.0&r=0.0&n=0.2

# Returns a calibrated alpha parameter
curl
http://127.0.0.1:5000/alpha?v=0.6&f=1.0&t=1.0&b=1.0&r=0.0&n=0.2
```

To run the microservice on Linux:
```bash
$ gunicorn -b '0.0.0.0:5000' web.app:app &>> pysabr_web.log &
```

To reload server on file changes on Windows:
```bash
$ nodemon --exec 'python -mwaitress --port=5000 web.app:app' -e py
```

# Excel web microservice wrapper

The web microservice can conveniently be called from Excel 2013+ using the ```WEBSERVICE``` spreadsheet function. For even more convenience, pySABR provides a small VBA wrapper mapping directly to the /sabr and /alpha resources. VBA code is available under [pySABR_web.bas](/pySABR_web.bas)
