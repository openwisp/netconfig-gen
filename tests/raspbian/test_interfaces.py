import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestInterfaces(unittest.TestCase, _TabsMixin):

    def test_no_ip(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet manual

"""

        self.assertEqual(o.render(), expected)

    def test_multi_no_ip(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet"
                },
                {
                    "name": "eth1",
                    "type": "ethernet"
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet manual

auto eth1
iface eth1 inet manual

"""

        self.assertEqual(o.render(), expected)

    def test_ipv4_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv4",
                            "proto": "static",
                            "address": "10.0.0.1",
                            "mask": 28
                        }
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet static
address 10.0.0.1
netmask 255.255.255.240

"""
        self.assertEqual(o.render(), expected)

    def test_multi_ipv4_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv4",
                            "proto": "static",
                            "address": "10.0.0.1",
                            "mask": 28
                        }
                    ]
                },
                {
                    "name": "eth1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv4",
                            "proto": "static",
                            "address": "10.0.0.2",
                            "mask": 28
                        }
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet static
address 10.0.0.1
netmask 255.255.255.240

auto eth1
iface eth1 inet static
address 10.0.0.2
netmask 255.255.255.240

"""
        self.assertEqual(o.render(), expected)

    def test_ipv6_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv6",
                            "proto": "static",
                            "address": "fe80::ba27:ebff:fe1c:5477",
                            "mask": 64
                        }
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet6 static
address fe80::ba27:ebff:fe1c:5477
netmask 64

"""
        self.assertEqual(o.render(), expected)

    def test_multi_ipv6_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv6",
                            "proto": "static",
                            "address": "fe80::ba27:ebff:fe1c:5477",
                            "mask": 64
                        }
                    ]
                },
                {
                    "name": "eth1",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv6",
                            "proto": "static",
                            "address": "2001:db8:0:0:0:ff00:42:8329",
                            "mask": 64
                        }
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet6 static
address fe80::ba27:ebff:fe1c:5477
netmask 64

auto eth1
iface eth1 inet6 static
address 2001:db8:0:0:0:ff00:42:8329
netmask 64

"""
        self.assertEqual(o.render(), expected)

    def test_multiple_static(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "family": "ipv4",
                            "proto": "static",
                            "address": "10.0.0.1",
                            "mask": 28
                        },
                        {
                            "family": "ipv6",
                            "proto": "static",
                            "address": "fe80::ba27:ebff:fe1c:5477",
                            "mask": 64
                        }
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet static
address 10.0.0.1
netmask 255.255.255.240
iface eth0 inet6 static
address fe80::ba27:ebff:fe1c:5477
netmask 64

"""
        self.assertEqual(o.render(), expected)

    def test_ipv4_dhcp(self):
        o = Raspbian({
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "proto": "dhcp",
                                "family": "ipv4"
                            }
                        ]
                    }
                ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet dhcp

"""
        self.assertEqual(o.render(), expected)

    def test_multi_ipv4_dhcp(self):
        o = Raspbian({
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "proto": "dhcp",
                                "family": "ipv4"
                            }
                        ]
                    },
                    {
                        "name": "eth1",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "proto": "dhcp",
                                "family": "ipv4"
                            }
                        ]
                    }
                ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet dhcp

auto eth1
iface eth1 inet dhcp

"""
        self.assertEqual(o.render(), expected)

    def test_ipv6_dhcp(self):
        o = Raspbian({
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "proto": "dhcp",
                                "family": "ipv6"
                            }
                        ]
                    }
                ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet6 dhcp

"""
        self.assertEqual(o.render(), expected)

    def test_multi_ipv6_dhcp(self):
        o = Raspbian({
                "interfaces": [
                    {
                        "name": "eth0",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "proto": "dhcp",
                                "family": "ipv6"
                            }
                        ]
                    },
                    {
                        "name": "eth1",
                        "type": "ethernet",
                        "addresses": [
                            {
                                "proto": "dhcp",
                                "family": "ipv6"
                            }
                        ]
                    }
                ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet6 dhcp

auto eth1
iface eth1 inet6 dhcp

"""
        self.assertEqual(o.render(), expected)

    def test_multiple_dhcp(self):
        o = Raspbian({
                    "interfaces": [
                        {
                            "name": "eth0",
                            "type": "ethernet",
                            "addresses": [

                                {
                                    "proto": "dhcp",
                                    "family": "ipv4"
                                },
                                {
                                    "proto": "dhcp",
                                    "family": "ipv6"
                                }
                            ]
                        }
                    ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet dhcp
iface eth0 inet6 dhcp

"""
        self.assertEqual(o.render(), expected)

    def test_multiple_ip(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "autostart": True,
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        {
                            "address": "192.168.2.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        {
                            "address": "fd87::1",
                            "mask": 128,
                            "proto": "static",
                            "family": "ipv6"
                        }
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet static
address 192.168.1.1
netmask 255.255.255.0
iface eth0 inet static
address 192.168.2.1
netmask 255.255.255.0
iface eth0 inet6 static
address fd87::1
netmask 128

"""
        self.assertEqual(o.render(), expected)

    def test_autostart_false(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "autostart": False
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

iface eth0 inet manual

"""

        self.assertEqual(o.render(), expected)

    def test_mtu(self):
        o = Raspbian({
            "interfaces": [
                {
                    "mtu": 1500,
                    "name": "eth1",
                    "addresses": [
                        {
                            "family": "ipv4",
                            "proto": "dhcp"
                        }
                    ],
                    "type": "ethernet",
                }
            ],
        })

        expected = """# config: /etc/network/interfaces

auto eth1
iface eth1 inet dhcp
pre-up /sbin/ifconfig $IFACE mtu 1500

"""
        self.assertEqual(o.render(), expected)

    def test_mac(self):
        o = Raspbian({
                "interfaces": [
                    {
                        "name": "eth1",
                        "addresses": [
                            {
                                "family": "ipv4",
                                "proto": "dhcp"
                            }
                        ],
                        "type": "ethernet",
                        "mac": "52:54:00:56:46:c0"
                    }
                ],
        })

        expected = """# config: /etc/network/interfaces

auto eth1
iface eth1 inet dhcp
hwaddress 52:54:00:56:46:c0

"""

        self.assertEqual(o.render(), expected)

    def test_multiple_ip_and_dhcp(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "proto": "dhcp",
                            "family": "ipv4"
                        },
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                        {
                            "address": "192.168.2.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        },
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet dhcp
iface eth0 inet static
address 192.168.1.1
netmask 255.255.255.0
iface eth0 inet static
address 192.168.2.1
netmask 255.255.255.0

"""
        self.assertEqual(o.render(), expected)

    def test_interface_with_resolv(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "eth0",
                    "type": "ethernet",
                    "addresses": [
                        {
                            "address": "192.168.1.1",
                            "mask": 24,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ],
            "dns_servers": ["10.11.12.13", "8.8.8.8"],
            "dns_search": ["netjson.org", "openwisp.org"],
        })

        expected = """# config: /etc/network/interfaces

auto eth0
iface eth0 inet static
address 192.168.1.1
netmask 255.255.255.0

# config: /etc/resolv.conf

nameserver 10.11.12.13
nameserver 8.8.8.8
search netjson.org
search openwisp.org
"""
        self.assertEqual(o.render(), expected)

    def test_loopback(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "lo",
                    "type": "loopback",
                    "addresses": [
                        {
                            "address": "127.0.0.1",
                            "mask": 8,
                            "proto": "static",
                            "family": "ipv4"
                        }
                    ]
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto lo
iface lo inet loopback

"""
        self.assertEqual(o.render(), expected)

    def test_adhoc_wireless(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "ssid": "freifunk",
                        "mode": "adhoc",
                        "bssid": "02:b8:c0:00:00:00"
                    }
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet static
address 172.128.1.1
netmask 255.255.255.0
wireless-channel 1
wireless-essid freifunk
wireless-mode ad-hoc

"""
        self.assertEqual(o.render(), expected)

    def test_simple_bridge(self):
        o = Raspbian({
                    "interfaces": [
                        {
                            "network": "lan",
                            "name": "br-lan",
                            "type": "bridge",
                            "bridge_members": [
                                "eth0",
                                "eth1"
                            ]
                        }
                    ]
        })

        expected = """# config: /etc/network/interfaces

auto br-lan
bridge_ports eth0 eth1

"""
        self.assertEqual(o.render(), expected)

    def test_complex_bridge(self):
        o = Raspbian({
            "interfaces": [
                {
                    "mtu": 1500,
                    "name": "brwifi",
                    "bridge_members": [
                        "wlan0",
                        "vpn.40"
                    ],
                    "addresses": [
                        {
                            "mask": 64,
                            "family": "ipv6",
                            "proto": "static",
                            "address": "fe80::8029:23ff:fe7d:c214"
                        }
                    ],
                    "type": "bridge",
                }
            ]
        })

        expected = """# config: /etc/network/interfaces

auto brwifi
iface brwifi inet6 static
address fe80::8029:23ff:fe7d:c214
netmask 64
mtu 1500
bridge_ports wlan0 vpn.40

"""
        self.assertEqual(o.render(), expected)
