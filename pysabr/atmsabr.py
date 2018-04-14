from pysabr import sabr
from pysabr import black

def shifted_lognormal_vol(k, f, s, t, v_atm_n, beta, rho, volvol):
    # Check if distribution is shifted enough, otherwise return 0
    if (k+s<=0) or (f+s<=0): return 0.

    # Convert ATM normal vol to ATM SLN vol
    v_atm_sln = black.normal_to_shifted_lognormal(f, f, s, t, v_atm_n)

    # Calibrate alpha parameter to ATM SLN vol
    alpha = sabr.alpha(v_atm_sln, f+s, t, beta, rho, volvol)

    # Compute SLN SABR vol at strike K
    v_sln = sabr.lognormal_vol(k+s, f+s, t, alpha, beta, rho, volvol)

    return v_sln
