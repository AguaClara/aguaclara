"""
research tests.
"""

import unittest
from aguaclara.research.utils import Constants, orbital_speed, circumference, orbital_period


class TestUtils(unittest.TestCase):
    """
    Test research's utils.
    """

    def setUp(self):
        pass

    def test_orbital_speed(self):
        """
        Calculate the orbital speed of an object.
        """
        answer = orbital_speed(
            Constants.Earth,
            600000,
            70
        )
        answer = round(answer, 3)
        self.assertEqual(
            answer,
            2425.552
        )

    def test_circumference(self):
        """
        2*pi*r
        """
        answer = circumference(600000)
        answer = round(answer, 3)
        self.assertEqual(
            answer,
            3769911.184
        )

    def test_orbital_period(self):
        """
        Calculate the orbital period of an object.
        """
        answer = orbital_period(
            Constants.Earth,
            600000,
            70
        )
        answer = round(answer, 3)
        self.assertEqual(
            answer,
            1554.43
        )
