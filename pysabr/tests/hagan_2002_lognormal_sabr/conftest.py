import pytest
import itertools
import pandas as pd
from pysabr.helpers import year_frac_from_maturity_label


# Path to vols, premiums and discount factors data
PATH = 'pysabr/examples/'

# Load vols data
df_vols = pd.read_csv(PATH + 'vols.csv')
df_vols.set_index(['Type', 'Option_expiry'], inplace=True)
df_vols.sort_index(inplace=True)
idx = pd.IndexSlice

# Load premium data
df_premiums = pd.read_csv(PATH + 'premiums.csv')
df_premiums.set_index(['Type', 'Option_expiry', 'Strike'], inplace=True)
df_premiums.sort_index(inplace=True)

# Load discount factors
df_discount = pd.read_csv(PATH + 'discount_factors.csv')

# Cartesian product of all expiries and tenors
expiries = df_vols.index.levels[1]
tenors = df_vols.columns
all_points = list(itertools.product(*[expiries, tenors]))
# all_points = [('1Y', '10Y')] # for debugging
all_points_ids = ["{} into {}".format(e, t) for e, t in all_points]


# Fixture serves for each point of the vol surface a tuple of:
# * Vol input: Forward + Shift + SABR params
# * Target vols for a range of strike
@pytest.fixture(scope="module", params=all_points, ids=all_points_ids)
def vol_cube(request):
    """Return vol cube parameters, vols, premiums."""
    option_expiry, swap_tenor = request.param
    # Vol input
    p = dict(
        df_vols.loc[idx[:, option_expiry], swap_tenor].
        reset_index(level=1, drop=True)
    )
    expiry_year_frac = year_frac_from_maturity_label(option_expiry)
    vol_input = (p['Forward'], p['Shift'], expiry_year_frac,
                 p['Normal_ATM_vol'], p['Beta'], p['Rho'], p['Volvol'])
    # Target vols
    target_vols = df_premiums.loc[
        idx['SLN_vol', option_expiry, :], swap_tenor
        ].reset_index(level=[0, 1], drop=True)
    # Yields the tuple
    yield (vol_input, target_vols)
