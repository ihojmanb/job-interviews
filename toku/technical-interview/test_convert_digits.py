import unittest
from convert_digits import *


class ConvertDigitsTest(unittest.TestCase):
    def test_digit_convertion_1(self):
        input_string = "Call my office, 888-123-4445"
        self.assertEqual(
            convert_digits(input_string, int(16), int(19)),
            "Call my office, EIGHTEIGHTEIGHT-123-4445")

    def test_digit_convertion_2(self):
        input_string = "Y0U, CONV3RT m3 PL3A2E"
        self.assertEqual(
            convert_digits(input_string, int(15), int(19)),
            "Y0U, CONV3RT mTHREE PLTHREEA2E")
    def test_digit_convertion_3(self):
        input_string = "666, the number of the devil"
        self.assertEqual(
            convert_digits(input_string, int(1), int(3)),
            "SIXSIXSIX, the number of the devil")

#   end_position > length of input string
    def test_invalid_digit_conversion_1(self):
        input_string = "666, the number of the devil"
        self.assertEqual(
            convert_digits(input_string, int(1), int(90)),
            "INVALID")
#   start_position > end_position
    def test_invalid_digit_conversion_2(self):
        input_string = "666, the number of the devil"
        self.assertEqual(
            convert_digits(input_string, int(3), int(1)),
            "INVALID")
    # start_position < 12
    def test_invalid_digit_conversion_3(self):
        input_string = "666, the number of the devil"
        self.assertEqual(
            convert_digits(input_string, int(0), int(3)),
            "INVALID")


if __name__ == "__main__":
    unittest.main()
