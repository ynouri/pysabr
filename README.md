# pysabr
Python implementation of SABR model.

# Introduction
SABR (Stochastic Alpha Beta Rho) is a financial volatility smile model widely used for interest rates options such as swaptions or cap/floors. This Python library implements its Hagan 2002 specification. For more information about the model itself, please consult the [original paper](./papers/Hagan%20-%20Managing%20Smile%20Risk%20-%202002.pdf) or [Wikipedia](https://en.wikipedia.org/wiki/SABR_volatility_model).

# Requirements
Core pySABR functions require `numpy` & `scipy` to run. The web microservice is based on `falcon`, which can itself be run with `waitress` (Windows) or `gunicorn` (Linux). Finally, the Excel function wrapper for the web microservice requires Windows and Excel 2013+.

# Installation
```bash
pip install pysabr

```

# Examples

`pysabr` provides two interface levels:
* A high-level, SABR model object interface, that lets the user work with the standard market inputs (ATM normal vol) and easily access model results (SLN or N vols, option premiums, density).
* A low-level interface to the Hagan expansions formulas and to the Black Scholes model.

## SABR model object

Interpolate a volatility using ATM normal vol input:
```Python
from pysabr import Hagan2002LognormalSABR
# Forward = 2.5%, Shift = 3%, ATM Normal Vol = 40bps
# Beta = 0.5, Rho = -20%, Volvol = 0.30
sabr = Hagan2002LognormalSABR(f=0.025, shift=0.03, t=1., v_atm_n=0.0040,
                              beta=0.5, rho=-0.2, volvol=0.30)
k = 0.025
sabr.lognormal_vol(k) * 100
# returns 7.27
sabr.normal_vol(k) *1e4
# returns 40
```

Calibrate alpha, rho and volvol from a discrete shift-lognormal smile:
```Python
from pysabr import Hagan2002LognormalSABR
import numpy as np
sabr = Hagan2002LognormalSABR(f=2.5271/100, shift=3/100, t=10, beta=0.5)
k = np.array([-0.4729, 0.5271, 1.0271, 1.5271, 1.7771, 2.0271, 2.2771, 2.4021,
              2.5271, 2.6521, 2.7771, 3.0271, 3.2771, 3.5271, 4.0271, 4.5271,
              5.5271]) / 100
v_sln = np.array([19.641923, 15.785344, 14.305103, 13.073869, 12.550007, 12.088721,
              11.691661, 11.517660, 11.360133, 11.219058, 11.094293, 10.892464,
              10.750834, 10.663653, 10.623862, 10.714479, 11.103755])
[alpha, rho, volvol] = sabr.fit(k, v_sln)
# returns [0.025299981543599154, -0.24629917636394097, 0.2908005625794777]
```

## Hagan 2002 lognormal expansion

Interpolate a shifted-lognormal volatility:
```Python
from pysabr import hagan_2002_lognormal_sabr as hagan2002
[s, k, f, t, alpha, beta, rho, volvol] = [0.03, 0.02, 0.025, 1.0, 0.025, 0.50, -0.24, 0.29]
hagan2002.lognormal_vol(k + s, f + s, t, alpha, beta, rho, volvol)
# returns 0.11408307
```

Calibrate alpha from an ATM lognormal vol:
```Python
from pysabr import hagan_2002_lognormal_sabr as hagan2002
[v_atm_sln, f, t, beta, rho, volvol] = [0.60, 0.02, 1.5, 1.0, 0.0, 0.0]
hagan2002.alpha(v_atm_sln, f, t, beta, rho, volvol)
# returns 0.60
```

## Black Scholes

Compute an option premium using Black formula:
```Python
from pysabr import black
[k, f, t, v, r, cp] = [0.012, 0.013, 10., 0.20, 0.02, 'call']
black.lognormal_call(k, f, t, v, r, cp) * 1e5
# returns 296.8806106707276
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
gunicorn -b '0.0.0.0:5000' web.app:app &>> pysabr_web.log &
```

To run the microservice on Windows:
```bash
python -mwaitress --port=5000 web.app:app
```

# Excel wrapper

The web microservice can conveniently be called from Excel 2013+ using the ```WEBSERVICE``` spreadsheet function. For even more convenience, pySABR provides a small VBA wrapper mapping directly to the /sabr and /alpha resources. VBA code is available under [pySABR_web.bas](./web/pySABR_web.bas)


# Run the tests
```bash
$ python -m pytest
```
