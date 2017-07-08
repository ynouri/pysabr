import unittest
import sabr

class TestSabr(unittest.TestCase):

    def test_lognormal_beta_05(self):
        s = 3 / 100
        k = 3.02715567337258000 / 100
        f = 2.52715567337258000 /100
        t = 10.00000000000000000
        alpha = 0.0252982247897366000
        beta = 0.5000000000000000000
        rho = -0.2463339754454810000
        volvol = 0.2908465632529730000
        v_test = sabr.lognormal(k + s, f + s, t, alpha, beta, rho, volvol)
        v_target = 11.35945567852760000 / 100
        self.assertAlmostEqual(v_test, v_target, 7)

    def test_lognormal_beta_0(self):
        k = 0.01
        f = 0.03
        t = 10
        alpha = 0.02
        beta = 1.00
        rho = 0.00
        volvol = 0.00
        v_test = sabr.lognormal(k, f, t, alpha, beta, rho, volvol)
        v_target = 0.02
        self.assertAlmostEqual(v_test, v_target, 7)
