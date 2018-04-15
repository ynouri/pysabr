import re


p1 = re.compile(r'(\d+Y)?(\d+M)?(\d+W)?(\d+D)?')
p2 = re.compile(r'(\d+)(\w)')


def year_frac_from_maturity_label(maturity_label):
    """
    Computes the year fraction from a maturity label.
    For example, '1Y6M' returns 1.5, and '1D' returns 1/360
    """
    # Step 1: break into years/months/weeks/days
    m1 = p1.search(maturity_label)

    # Step 2: break into decimals and symbol
    maturity_codes = []
    for g in m1.group(1, 2, 3, 4):
        if g:
            m2 = p2.search(g)
            maturity_codes.append((int(m2.group(1)), m2.group(2)))

    # Step 3: sum codes by their weights
    weights = {'Y': 360, 'M': 30, 'W': 7, 'D': 1}
    yearfrac = sum([n * weights[code] for (n, code) in maturity_codes]) / 360

    return yearfrac
