"""
ZeroTier specific JSON-Schema definition
"""

from copy import deepcopy

from ...schema import schema as default_schema

# The schema is taken from OpenAPI specification:
# https://docs.zerotier.com/service/v1/ (self-hosted controllers)
# https://docs.zerotier.com/openapi/centralv1.json (central controllers)
base_zerotier_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": True,
    "definitions": {
        "zerotier_server": {
            "type": "object",
            "title": "ZeroTier Network",
            "required": ["name"],
            "properties": {
                # Read-only properties
                "name": {
                    "type": "string",
                    # Since it is intended to be set by
                    # the VPN backend's name field, it is read-only
                    "readOnly": True,
                    "propertyOrder": 1,
                    "description": "Name of the network",
                },
                "id": {
                    "type": "string",
                    "maxLength": 16,
                    "readOnly": True,
                    "propertyOrder": 2,
                    "description": "Network ID",
                },
                "nwid": {
                    "type": "string",
                    "maxLength": 16,
                    "readOnly": True,
                    "propertyOrder": 3,
                    "description": "Network ID legacy field (same as 'id')",
                },
                "objtype": {
                    "type": "string",
                    "readOnly": True,
                    "propertyOrder": 4,
                    "default": "network",
                },
                "revision": {
                    "type": "integer",
                    "readOnly": True,
                    "propertyOrder": 5,
                    "description": "The revision number of the network configuration",
                },
                "creationTime": {
                    "type": "number",
                    "readOnly": True,
                    "propertyOrder": 6,
                    "description": "Time when the network was created",
                },
                # Configurable properties
                "capabilities": {
                    "type": "array",
                    "items": {"type": "object"},
                    "propertyOrder": 17,
                    "description": "Array of network capabilities",
                },
                "dns": {
                    "type": "object",
                    "propertyOrder": 15,
                    "properties": {
                        "domain": {
                            "type": "string",
                            "propertyOrder": 1,
                            "description": "The domain for DNS resolution",
                        },
                        "servers": {
                            "type": "array",
                            "propertyOrder": 2,
                            "items": {
                                "type": "string",
                                "description": "The DNS server IP addresses",
                            },
                        },
                    },
                },
                "enableBroadcast": {
                    "type": "boolean",
                    "default": True,
                    "format": "checkbox",
                    "propertyOrder": 8,
                    "description": "Enable broadcast packets on the network",
                },
                "ipAssignmentPools": {
                    "type": "array",
                    "propertyOrder": 14,
                    "items": {
                        "type": "object",
                        "properties": {
                            "ipRangeStart": {
                                "type": "string",
                                "propertyOrder": 1,
                                "description": "The starting IP address of the pool range",
                            },
                            "ipRangeEnd": {
                                "type": "string",
                                "propertyOrder": 2,
                                "description": "The ending IP address of the pool range",
                            },
                        },
                    },
                    "description": "Range of IP addresses for the auto assign pool",
                },
                "mtu": {
                    "type": "integer",
                    "default": 2800,
                    "propertyOrder": 11,
                    "description": "MTU to set on the client virtual network adapter",
                },
                "multicastLimit": {
                    "type": "integer",
                    "default": 32,
                    "propertyOrder": 12,
                    "description": (
                        "Maximum number of recipients per multicast or broadcast. "
                        "Warning - Setting this to 0 will disable IPv4 communication on your network!"
                    ),
                },
                "private": {
                    "type": "boolean",
                    "default": True,
                    "format": "checkbox",
                    "propertyOrder": 7,
                    "description": (
                        "Whether or not the network is private "
                        "If false, members will NOT need to be authorized to join"
                    ),
                },
                "remoteTraceLevel": {
                    "type": "integer",
                    "propertyOrder": 19,
                    "description": "The level of network tracing",
                },
                "remoteTraceTarget": {
                    "type": ["string", "null"],
                    "propertyOrder": 20,
                    "default": "",
                    "description": "The remote target ID for network tracing",
                },
                "routes": {
                    "type": "array",
                    "propertyOrder": 13,
                    "items": {
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "string",
                                "propertyOrder": 1,
                                "description": "The target IP address range for the route",
                            },
                            "via": {
                                "type": "string",
                                "propertyOrder": 2,
                                "description": "The IP address of the next hop for the route",
                            },
                        },
                    },
                    "description": "Array of route objects",
                },
                "rules": {
                    "type": "array",
                    "items": {"type": "object"},
                    "propertyOrder": 16,
                    "description": "Array of network rule objects",
                    # This is the default rule set
                    # that allows IPv4 and IPv6 traffic
                    # It is based on the default
                    # network configuration from ZeroTier Central
                    # https://docs.zerotier.com/zerotier/rules
                    "default": [
                        {
                            "etherType": 2048,
                            "not": True,
                            "or": False,
                            "type": "MATCH_ETHERTYPE",
                        },
                        {
                            "etherType": 2054,
                            "not": True,
                            "or": False,
                            "type": "MATCH_ETHERTYPE",
                        },
                        {
                            "etherType": 34525,
                            "not": True,
                            "or": False,
                            "type": "MATCH_ETHERTYPE",
                        },
                        {"type": "ACTION_DROP"},
                        {"type": "ACTION_ACCEPT"},
                    ],
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "object"},
                    "propertyOrder": 18,
                    "description": "Array of network tag objects",
                },
                "v4AssignMode": {
                    "type": "object",
                    "propertyOrder": 9,
                    "properties": {
                        "zt": {
                            "type": "boolean",
                            "format": "checkbox",
                            "description": "Whether ZeroTier should assign IPv4 addresses to members",
                        },
                    },
                },
                "v6AssignMode": {
                    "type": "object",
                    "propertyOrder": 10,
                    "properties": {
                        "6plane": {
                            "type": "boolean",
                            "format": "checkbox",
                            "description": "Whether 6PLANE addressing should be used for IPv6 assignment",
                        },
                        "rfc4193": {
                            "type": "boolean",
                            "format": "checkbox",
                            "description": "Whether RFC4193 addressing should be used for IPv6 assignment",  # noqa
                        },
                        "zt": {
                            "type": "boolean",
                            "format": "checkbox",
                            "description": "Whether ZeroTier should assign IPv6 addresses to members",
                        },
                    },
                },
            },
        },
    },
    "properties": {
        "zerotier": {
            "type": "array",
            "title": "ZeroTier",
            "uniqueItems": True,
            "additionalItems": True,
            "propertyOrder": 12,
            "items": {
                "type": "object",
                "title": "VPN",
                "additionalProperties": True,
                "allOf": [
                    {"$ref": "#/definitions/zerotier_server"},
                ],
            },
        }
    },
}

schema = deepcopy(base_zerotier_schema)
schema['required'] = ['zerotier']
schema['properties']['files'] = default_schema['properties']['files']
