import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestWpaSupplicant(unittest.TestCase, _TabsMixin):

    def test_wep_open(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "mode": "station",
                        "radio": "radio0",
                        "ssid": "wep-test",
                        "bssid": "01:23:45:67:89:ab",
                        "encryption": {
                            "protocol": "wep_open",
                            "key": "12345"
                        }
                    },
                }
            ]
        })

        expected = """# config: /etc/wpa_supplicant/wpa_supplicant.conf

network={
ssid="wep-test"
key_mgmt=NONE
wep_key0="12345"
}

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""

        self.assertEqual(o.render(), expected)

    def test_wep_shared(self):
        o = Raspbian({
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "mode": "station",
                        "radio": "radio0",
                        "ssid": "wep-test",
                        "bssid": "01:23:45:67:89:ab",
                        "encryption": {
                            "protocol": "wep_shared",
                            "key": "12345"
                        }
                    },
                }
            ]
        })

        expected = """# config: /etc/wpa_supplicant/wpa_supplicant.conf

network={
ssid="wep-test"
key_mgmt=NONE
wep_key0="12345"
auth_algs=shared
}

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""

        self.assertEqual(o.render(), expected)

    def test_wpa2_personal_sta(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ],
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "station",
                        "ssid": "Test",
                        "bssid": "00:11:22:33:44:55",
                        "encryption": {
                            "protocol": "wpa2_personal",
                            "key": "changeme",
                        },
                    },
                }
            ]
        })

        expected = """# config: /etc/wpa_supplicant/wpa_supplicant.conf

network={
ssid="Test"
key="changeme"
key_mgmt=WPA-PSK
}

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)

    def test_wpa2_enterprise_client(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 36,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "station",
                        "ssid": "enterprise-client",
                        "bssid": "00:26:b9:20:5f:09",
                        "encryption": {
                            "protocol": "wpa2_enterprise",
                            "cipher": "auto",
                            "eap_type": "tls",
                            "identity": "test-identity",
                            "password": "test-password",
                        }
                    }
                }
            ]
        })

        expected = """# config: /etc/wpa_supplicant/wpa_supplicant.conf

network={
ssid="enterprise-client"
eap=TLS
identity="test-identity"
password="test-password"
}

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""

        self.assertEqual(o.render(), expected)

    def test_no_encryption(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 3,
                    "channel_width": 20,
                    "tx_power": 3
                }
            ],
            "interfaces": [
                {
                    "type": "wireless",
                    "name": "wlan0",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "station",
                        "ssid": "ap-ssid-example",
                        "bssid": "00:11:22:33:44:55",
                    },
                }
            ]
        })

        expected = """# config: /etc/wpa_supplicant/wpa_supplicant.conf

network={
ssid="ap-ssid-example"
key_mgmt=NONE
}

# config: /etc/network/interfaces

auto wlan0
iface wlan0 inet manual

# script: /scripts/ipv4_forwarding.sh

sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

"""
        self.assertEqual(o.render(), expected)
