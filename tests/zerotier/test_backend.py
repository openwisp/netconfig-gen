import tarfile
import unittest
from copy import deepcopy

from netjsonconfig import ZeroTier
from netjsonconfig.exceptions import ValidationError


class TestBackend(unittest.TestCase):
    """
    Tests for ZeroTier backend
    """

    maxDiff = None

    # Single test config
    _TEST_CONFIG = {
        "zerotier": [
            {
                "id": "9536600adf654321",
                "nwid": "9536600adf654321",
                "objtype": "network",
                "revision": 1,
                "creationTime": 1632012345,
                "name": "zerotier-openwisp-network",
                "private": True,
                "enableBroadcast": True,
                "v4AssignMode": {"zt": True},
                "v6AssignMode": {"6plane": False, "rfc4193": True, "zt": True},
                "mtu": 2700,
                "multicastLimit": 16,
                "routes": [{"target": "10.0.0.0/24", "via": "10.0.0.1"}],
                "ipAssignmentPools": [
                    {"ipRangeStart": "10.0.0.10", "ipRangeEnd": "10.0.0.100"}
                ],
                "dns": {"domain": "zerotier.openwisp.io", "servers": ["10.147.20.3"]},
                "rules": [
                    {
                        "etherType": 2048,
                        "not": True,
                        "or": False,
                        "type": "MATCH_ETHERTYPE",
                    },
                    {"type": "ACTION_DROP"},
                ],
                "capabilities": [
                    {
                        "default": True,
                        "id": 1,
                        "rules": [
                            {
                                "etherType": 2048,
                                "not": True,
                                "or": False,
                                "type": "MATCH_ETHERTYPE",
                            }
                        ],
                    }
                ],
                "tags": [{"default": 1, "id": 1}],
                "remoteTraceTarget": "7f5d90eb87",
                "remoteTraceLevel": 1,
                "client_options": {
                    "allow_managed": True,
                    "allow_global": False,
                    "allow_default": False,
                    "allow_dns": False,
                },
            }
        ]
    }

    # Multiple test config
    _TEST_MULTIPLE_CONFIG = deepcopy(_TEST_CONFIG)
    _TEST_MULTIPLE_CONFIG['zerotier'].append(
        {
            "id": "9536600adf654322",
            "nwid": "9536600adf654322",
            "objtype": "network",
            "revision": 1,
            "creationTime": 1632012345,
            "name": "zerotier-openwisp-network-2",
            "private": True,
            "enableBroadcast": True,
            "v4AssignMode": {"zt": True},
            "v6AssignMode": {"6plane": False, "rfc4193": True, "zt": True},
            "mtu": 2700,
            "multicastLimit": 16,
            "routes": [{"target": "10.0.0.0/24", "via": "10.0.0.1"}],
            "ipAssignmentPools": [
                {"ipRangeStart": "10.0.0.10", "ipRangeEnd": "10.0.0.100"}
            ],
            "dns": {"domain": "zerotier.openwisp.io", "servers": ["10.147.20.3"]},
            "tags": [{"default": 1, "id": 1}],
            "remoteTraceTarget": "7f5d90eb87",
            "remoteTraceLevel": 1,
        }
    )

    def test_test_schema(self):
        with self.assertRaises(ValidationError) as context_manager:
            ZeroTier({}).validate()
        self.assertIn(
            "'zerotier' is a required property", str(context_manager.exception)
        )

    def test_confs(self):
        c = ZeroTier(self._TEST_CONFIG)
        expected = """// zerotier controller config: 9536600adf654321.json

{
    "capabilities": [
        {
            "default": true,
            "id": 1,
            "rules": [
                {
                    "etherType": 2048,
                    "not": true,
                    "or": false,
                    "type": "MATCH_ETHERTYPE"
                }
            ]
        }
    ],
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654321",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network",
    "nwid": "9536600adf654321",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "rules": [
        {
            "etherType": 2048,
            "not": true,
            "or": false,
            "type": "MATCH_ETHERTYPE"
        },
        {
            "type": "ACTION_DROP"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}
"""
        self.assertEqual(c.render(), expected)

    def test_mutiple_confs(self):
        c = ZeroTier(self._TEST_MULTIPLE_CONFIG)
        expected = """// zerotier controller config: 9536600adf654321.json

{
    "capabilities": [
        {
            "default": true,
            "id": 1,
            "rules": [
                {
                    "etherType": 2048,
                    "not": true,
                    "or": false,
                    "type": "MATCH_ETHERTYPE"
                }
            ]
        }
    ],
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654321",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network",
    "nwid": "9536600adf654321",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "rules": [
        {
            "etherType": 2048,
            "not": true,
            "or": false,
            "type": "MATCH_ETHERTYPE"
        },
        {
            "type": "ACTION_DROP"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}

// zerotier controller config: 9536600adf654322.json

{
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654322",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network-2",
    "nwid": "9536600adf654322",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}
"""
        self.assertEqual(c.render(), expected)

    def test_generate(self):
        c = ZeroTier(self._TEST_MULTIPLE_CONFIG)
        expected = """{
    "capabilities": [
        {
            "default": true,
            "id": 1,
            "rules": [
                {
                    "etherType": 2048,
                    "not": true,
                    "or": false,
                    "type": "MATCH_ETHERTYPE"
                }
            ]
        }
    ],
    "creationTime": 1632012345,
    "dns": {
        "domain": "zerotier.openwisp.io",
        "servers": [
            "10.147.20.3"
        ]
    },
    "enableBroadcast": true,
    "id": "9536600adf654321",
    "ipAssignmentPools": [
        {
            "ipRangeEnd": "10.0.0.100",
            "ipRangeStart": "10.0.0.10"
        }
    ],
    "mtu": 2700,
    "multicastLimit": 16,
    "name": "zerotier-openwisp-network",
    "nwid": "9536600adf654321",
    "objtype": "network",
    "private": true,
    "remoteTraceLevel": 1,
    "remoteTraceTarget": "7f5d90eb87",
    "revision": 1,
    "routes": [
        {
            "target": "10.0.0.0/24",
            "via": "10.0.0.1"
        }
    ],
    "rules": [
        {
            "etherType": 2048,
            "not": true,
            "or": false,
            "type": "MATCH_ETHERTYPE"
        },
        {
            "type": "ACTION_DROP"
        }
    ],
    "tags": [
        {
            "default": 1,
            "id": 1
        }
    ],
    "v4AssignMode": {
        "zt": true
    },
    "v6AssignMode": {
        "6plane": false,
        "rfc4193": true,
        "zt": true
    }
}
"""
        tar = tarfile.open(fileobj=c.generate(), mode="r")
        self.assertEqual(len(tar.getmembers()), 2)
        vpn = tar.getmember("9536600adf654321.json")
        contents = tar.extractfile(vpn).read().decode()
        self.assertEqual(contents, expected)

    def test_auto_client(self):
        test_config = self._TEST_CONFIG["zerotier"][0]
        nw_id = test_config['id']
        expected = {
            'name': 'global',
            'networks': [{'id': '9536600adf654321', 'ifname': 'owzt654321'}],
            'secret': 'test_secret',
            'config_path': '/etc/openwisp/zerotier',
            'disabled': False,
        }
        self.assertEqual(
            ZeroTier.auto_client(
                name="global",
                networks=[
                    {
                        'id': nw_id,
                        'ifname': f'owzt{nw_id[-6:]}',
                    }
                ],
                identity_secret="test_secret",
            ),
            expected,
        )
