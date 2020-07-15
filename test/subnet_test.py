import unittest

from src.subnet import string_ip_to_int, WrongIpException, get_min_subnet, TooFewIpsException, extract_octet


class StringIpToIntTest(unittest.TestCase):
    def test_stringIpToInt(self):
        val = string_ip_to_int('192.168.1.1')
        self.assertEqual('0b11000000101010000000000100000001', bin(val))

    def test_wrongIp(self):
        with self.assertRaises(WrongIpException):
            string_ip_to_int('192.168.1.1111')

    def test_wrongIp2(self):
        with self.assertRaises(WrongIpException):
            string_ip_to_int('asda')

    def test_wrongIp3(self):
        with self.assertRaises(WrongIpException):
            string_ip_to_int('257.168.1.1')


class ExtractOctetTest(unittest.TestCase):
    def test_extractOctet(self):
        val = extract_octet(192, 1)
        self.assertEqual(192, val)

        val = extract_octet(int('1000000011001100', 2), 2)
        self.assertEqual(204, val)
        self.assertEqual('11001100', bin(val)[2:])


class GetMinSubnetTest(unittest.TestCase):

    def test_minSubnetNoArg(self):
        with self.assertRaises(TypeError):
            get_min_subnet()

    def test_minSubnetEmptyIpList(self):
        with self.assertRaises(TooFewIpsException):
            get_min_subnet([])

    def test_minSubnetOneIp(self):
        with self.assertRaises(TooFewIpsException):
            get_min_subnet(['192.168.1.1'])

    def test_minSubnetOneDistinctIp(self):
        with self.assertRaises(TooFewIpsException):
            get_min_subnet(['192.168.1.1', '192.168.1.1'])

    # 192.168.1.1 = 11000000101010000000000100000001
    # 192.10.5.4  = 11000000000010100000010100000100
    # 192.168.5.5 = 11000000101010000000010100000101
    # 192.17.55.6 = 11000000000100010011011100000110
    # mask        = 11111111000000000000000000000000
    # subnet      = 11000000000000000000000000000000 = 192.0.0.0/8
    def test_minSubnet(self):
        val = get_min_subnet(['192.168.1.1', '192.10.5.4', '192.168.5.5', '192.17.55.6'])
        self.assertEqual('192.0.0.0/8', val)


if __name__ == '__main__':
    unittest.main()
