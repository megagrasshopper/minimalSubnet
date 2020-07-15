import re

ip_pattern = re.compile('''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.(
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$''')


class WrongIpException(Exception):
    pass


class TooFewIpsException(Exception):
    pass


def string_ip_to_int(ip):
    if not ip_pattern.match(ip):
        raise WrongIpException('Invalid IP Address format.')
    ip_bin = ['{0:08b}'.format(int(octet)) for octet in ip.split('.')]
    return int(''.join(ip_bin), 2)


def extract_octet(n, octet_number):
    return ((1 << 8) - 1) & n >> (n.bit_length() - 8 * octet_number)


def get_min_subnet(ips):
    ips = list(set(ips))
    if len(ips) < 2:
        raise TooFewIpsException

    diff = 0
    for ip, next_ip in zip(ips, ips[1:]):
        ip1 = string_ip_to_int(ip)
        ip2 = string_ip_to_int(next_ip)
        diff = diff | (ip1 ^ ip2)

    diff = diff.bit_length()

    mask = ((1 << (4 * 8 - diff)) - 1) << diff
    subnet_ip = string_ip_to_int(ips[0]) & mask

    return '{0}/{1}'.format('.'.join(str(it) for it in map(lambda i: extract_octet(subnet_ip, i), [1, 2, 3, 4])),
                            str(32 - diff))


if __name__ == '__main__':
    print(get_min_subnet(['192.168.1.1', '192.168.10.5']))
