import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.utils import _TabsMixin


class TestZeroTier(unittest.TestCase, _TabsMixin):
    maxDiff = None
    # This configuration is used when we want to join multiple networks
    # and the ZT service is running on a single default port 9993
    _multiple_networks_netjson = {
        "zerotier": [
            {
                "local_conf_path": "/etc/openwisp/zerotier/zerotier.conf",
                "name": "global",
                "networks": [
                    {
                        "id": "9536600adf654321",
                        "ifname": "owzt654321",
                        "allow_managed": True,
                        "allow_global": False,
                        "allow_default": False,
                        "allow_dns": False,
                    },
                    {
                        "id": "9536600adf654322",
                        "ifname": "owzt654322",
                        "allow_managed": True,
                        "allow_global": False,
                        "allow_default": False,
                        "allow_dns": False,
                    },
                ],
            },
        ]
    }
    _multiple_networks_uci = """package zerotier

config zerotier 'global'
    option config_path '/etc/openwisp/zerotier'
    option copy_config_path '1'
    option enabled '1'
    list join '9536600adf654321'
    list join '9536600adf654322'
    option local_conf '/etc/openwisp/zerotier/zerotier.conf'
    option local_conf_path '/etc/openwisp/zerotier/zerotier.conf'

config network 'owzt654321'
    option allow_default '0'
    option allow_dns '0'
    option allow_global '0'
    option allow_managed '1'
    option id '9536600adf654321'

config network 'owzt654322'
    option allow_default '0'
    option allow_dns '0'
    option allow_global '0'
    option allow_managed '1'
    option id '9536600adf654322'

# ---------- files ---------- #

# path: /etc/openwisp/zerotier/devicemap
# mode: 0644

# network_id=interface_name
9536600adf654321=owzt654321
9536600adf654322=owzt654322

"""

    # This ZT configuration is used when ZT services
    # are configured to run on multiple ports, e.g., 9993 and 9994.
    # For more information, refer to:
    # https://docs.zerotier.com/zerotier/zerotier.conf/#local-configuration-options
    _TEST_DIFF_NAME_MULTIPLE_CONFIG = {
        "zerotier": [
            {
                "name": "global1",
                "networks": [{"id": "9536600adf654321", "ifname": "owzt654321"}],
            },
            {
                "name": "global2",
                "networks": [{"id": "9536600adf654322", "ifname": "owzt654322"}],
            },
        ]
    }

    def test_zt_render(self):
        o = OpenWrt(self._multiple_networks_netjson)
        expected = self._tabs(self._multiple_networks_uci)
        self.assertEqual(o.render(), expected)

    def test_zt_parse_old(self):
        native = self._tabs(
            """package zerotier

config zerotier 'global'
    option enabled '0'
    option local_conf '/etc/openwisp/zerotier/zerotier.conf'
    list join '9536600adf654321'
    list join '9536600adf654322'
"""
        )
        expected = {
            "zerotier": [
                {
                    "local_conf_path": "/etc/openwisp/zerotier/zerotier.conf",
                    "networks": [
                        {"id": "9536600adf654321", "ifname": "owzt654321"},
                        {"id": "9536600adf654322", "ifname": "owzt654322"},
                    ],
                    "name": "global",
                    "disabled": True,
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)

    def test_zt_parse_new(self):
        native = self._tabs(
            """package zerotier

config zerotier 'global'
    option enabled '0'
    option local_conf_path '/etc/openwisp/zerotier/zerotier.conf'

config network
    option id '9536600adf654321'

config network
    option id '9536600adf654322'
    option allow_default '0'
    option allow_dns '0'
    option allow_global '0'
    option allow_managed '1'
"""
        )
        expected = {
            "zerotier": [
                {
                    "local_conf_path": "/etc/openwisp/zerotier/zerotier.conf",
                    "networks": [
                        {"id": "9536600adf654321", "ifname": "owzt654321"},
                        {
                            "id": "9536600adf654322",
                            "ifname": "owzt654322",
                            "allow_managed": True,
                            "allow_global": False,
                            "allow_default": False,
                            "allow_dns": False,
                        },
                    ],
                    "name": "global",
                    "disabled": True,
                },
            ]
        }
        o = OpenWrt(native=native)
        self.assertEqual(o.config, expected)
