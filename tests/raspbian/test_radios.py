import unittest

from netjsonconfig import Raspbian
from netjsonconfig.utils import _TabsMixin


class TestRadio(unittest.TestCase, _TabsMixin):

    def test_radio_multi(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 11,
                    "channel_width": 20,
                    "tx_power": 5,
                    "country": "IT"
                },
                {
                    "name": "radio1",
                    "phy": "phy1",
                    "driver": "mac80211",
                    "protocol": "802.11n",
                    "channel": 36,
                    "channel_width": 20,
                    "tx_power": 4,
                    "country": "IT"
                }
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "myWiFi"
                    }
                }
            ]
        })

        expected = '''# config: /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
hw_mode=g
channel=11
ieee80211n=1
ssid=myWiFi

'''
        self.assertEqual(o.render(), expected)

    def test_radio_n_24ghz(self):
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
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "myWiFi"
                    }
                }
            ]
        })

        expected = '''# config: /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
hw_mode=g
channel=3
ieee80211n=1
ssid=myWiFi

'''
        self.assertEqual(o.render(), expected)

    def test_radio_n_5ghz(self):
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
                        "mode": "access_point",
                        "ssid": "myWiFi"
                    }
                }
            ]
        })

        expected = '''# config: /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
hw_mode=a
channel=36
ieee80211n=1
ssid=myWiFi

'''
        self.assertEqual(o.render(), expected)

    def test_radio_ac(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11ac",
                    "channel": 132,
                    "channel_width": 80,
                }
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "myWiFi"
                    }
                }
            ]
        })

        expected = '''# config: /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
hw_mode=a
channel=132
ieee80211ac=1
ssid=myWiFi

'''
        self.assertEqual(o.render(), expected)

    def test_radio_a(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11a",
                    "channel": 0,
                    "channel_width": 20
                }
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "myWiFi"
                    }
                }
            ]
        })

        expected = '''# config: /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
hw_mode=a
channel=0
ssid=myWiFi

'''
        self.assertEqual(o.render(), expected)

    def test_radio_g(self):
        o = Raspbian({
            "radios": [
                {
                    "name": "radio0",
                    "phy": "phy0",
                    "driver": "mac80211",
                    "protocol": "802.11g",
                    "channel": 0,
                    "channel_width": 20
                }
            ],
            "interfaces": [
                {
                    "name": "wlan0",
                    "type": "wireless",
                    "wireless": {
                        "radio": "radio0",
                        "mode": "access_point",
                        "ssid": "myWiFi"
                    }
                }
            ]
        })

        expected = '''# config: /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
hw_mode=g
channel=0
ssid=myWiFi

'''
        self.assertEqual(o.render(), expected)
