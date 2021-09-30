import unittest
from desafio import *


class BudaBotTest(unittest.TestCase):
    def test_get_mercados_id(self):
        budabot = BudaBot()
        self.assertEqual(
            budabot.mercadosId,
            [
                "BTC-CLP",
                "BTC-COP",
                "ETH-CLP",
                "ETH-BTC",
                "BTC-PEN",
                "ETH-PEN",
                "ETH-COP",
                "BCH-BTC",
                "BCH-CLP",
                "BCH-COP",
                "BCH-PEN",
                "BTC-ARS",
                "ETH-ARS",
                "BCH-ARS",
                "LTC-BTC",
                "LTC-CLP",
                "LTC-COP",
                "LTC-PEN",
                "LTC-ARS"
            ]
        )

    def test_get_mercados(self):
        budabot = BudaBot()
        mercados = budabot.getMercados()
        error_msg = "object is not an instance of Mercado"
        self.assertIsInstance(mercados[0], Mercado, error_msg)


if __name__ == "__main__":
    unittest.main()
