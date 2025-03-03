ZeroTier Backend
================

The ``ZeroTier`` backend generates JSON configurations that can be used
with the `ZeroTier Service API <https://docs.zerotier.com/service/v1/>`_
to manage ZeroTier networks on `Self-hosted ZeroTier controllers
<https://docs.zerotier.com/self-hosting/introduction>`_.

Its schema is limited to a subset of the features available in ZeroTier
and it doesn't recognize interfaces, radios, wireless settings and so on.

The main methods work just like the :doc:`OpenWrt backend
</backends/openwrt>`:

    - ``__init__``
    - ``render``
    - ``generate``
    - ``write``
    - ``json``

The main differences are in the resulting configuration and in its schema.

See an example of initialization and rendering below:

.. code-block:: python

    from netjsonconfig import ZeroTier

    config = ZeroTier(
        {
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
                    "v6AssignMode": {
                        "6plane": False,
                        "rfc4193": True,
                        "zt": True,
                    },
                    "mtu": 2700,
                    "multicastLimit": 16,
                    "routes": [{"target": "10.0.0.0/24", "via": "10.0.0.1"}],
                    "ipAssignmentPools": [
                        {
                            "ipRangeStart": "10.0.0.10",
                            "ipRangeEnd": "10.0.0.100",
                        }
                    ],
                    "dns": {
                        "domain": "zerotier.openwisp.io",
                        "servers": ["10.147.20.3"],
                    },
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
    )
    print(config.render())

Will return the following output:

::

    // zerotier controller config: 9536600adf654321.json

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

.. _zerotier_backend_schema:

ZeroTier backend schema
-----------------------

The ``ZeroTier`` backend schema is limited, it only recognizes an
``zerotier`` key with a list of dictionaries representing vpn instances.
The structure of these dictionaries is described below.

Alternatively you may also want to take a look at the `ZeroTier
JSON-Schema source code
<https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/backends/zerotier/schema.py>`_.

According to the `NetJSON <http://netjson.org>`_ spec, any unrecognized
property will be ignored.

Server specific settings
~~~~~~~~~~~~~~~~~~~~~~~~

Required properties:

- name

===================== ======= =========== =======================================================================
key name              type    default     description
===================== ======= =========== =======================================================================
``name``              string              name of the network
``id``                string              **16-digit** hexadecimal Network ID
``nwid``              string              **16-digit** hexadecimal Network ID (legacy field)
``objtype``           string  ``network`` specifies the type of object
``revision``          integer             revision number of the network configuration
``creationTime``      integer             time when the network was created
``private``           boolean             whether or not the network is private if ``False``

                                          members will NOT need to be authorized to join
``enableBroadcast``   boolean             enable broadcast packets on the network
``v4AssignMode``      object  ``{}``      ======== ======= ================================================
                                          key name type    description
                                          ======== ======= ================================================
                                          ``zt``   boolean whether ZeroTier should assign IPv4 addresses to
                                                           members
                                          ======== ======= ================================================
``v6AssignMode``      dict    ``{}``      =========== ======= ===================================================
                                          key name    type    description
                                          =========== ======= ===================================================
                                          ``6plane``  boolean 6PLANE assigns each device a single IPv6 address
                                                              from a

                                                              fully routable /80 block. It utilizes NDP emulation
                                                              to route

                                                              the entire /80 to the device owner, enabling up to
                                                              2^48 IPs

                                                              without additional configuration. Ideal for Docker
                                                              or VM hosts
                                          ``rfc4193`` boolean RFC4193 assigns each device a single IPv6 /128
                                                              address

                                                              computed from the network ID and device address and
                                                              uses NDP

                                                              emulation to make these addresses instantly
                                                              resolvable without

                                                              multicast
                                          ``zt``      boolean whether ZeroTier should assign IPv6 addresses to
                                                              members
                                          =========== ======= ===================================================
``mtu``               integer             MTU to set on the client virtual network adapter
``multicastLimit``    integer             maximum number of recipients per multicast or broadcast,

                                          warning - Setting this to ``0`` will disable IPv4 communication on your
                                          network
``routes``            list    ``[{}]``    |   list of route dictionaries

                                          ========== ====== ========================================
                                          key name   type   description
                                          ========== ====== ========================================
                                          ``target`` string target IP address range for the route
                                          ``via``    string IP address of the next hop for the route
                                          ========== ====== ========================================
``ipAssignmentPools`` list    ``[{}]``    |   list that contains dictionaries specifying
                                          |   a range of IP addresses for the auto assign pool

                                          ================ ====== =====================================
                                          key name         type   description
                                          ================ ====== =====================================
                                          ``ipRangeStart`` string starting IP address of the pool range
                                          ``ipRangeEnd``   string ending IP address of the pool range
                                          ================ ====== =====================================
``dns``               dict    ``{}``      ========== ====== =========================
                                          key name   type   description
                                          ========== ====== =========================
                                          ``domain`` string domain for DNS resolution
                                          ``server`` list   DNS server IP addresses
                                          ========== ====== =========================
``rules``             list    ``[{}]``    list of network rules dictionaries
``tags``              list    ``[{}]``    list of network tags dictionaries
``remoteTraceTarget`` string              remote target ID for network tracing
``remoteTraceLevel``  integer             level of network tracing
``client_options``    dict    ``{}``      These options are only used for client configurations

                                          ================= ======= =============================================
                                          key name          type    description
                                          ================= ======= =============================================
                                          ``allow_managed`` boolean allow ZeroTier to set IP addresses and routes
                                          ``allow_global``  boolean allow ZeroTier to set
                                                                    global/public/not-private range IPs and
                                                                    routes
                                          ``allow_default`` boolean allow ZeroTier to set the default route on
                                                                    the system
                                          ``allow_dns``     boolean allow ZeroTier to set DNS servers
                                          ================= ======= =============================================
===================== ======= =========== =======================================================================

Client specific settings
~~~~~~~~~~~~~~~~~~~~~~~~

Required properties:

- name
- networks

==================== ======= ========================== =========================
key name             type    default                    description
==================== ======= ========================== =========================
``name``             string  ``global``                 name of the zerotier
                                                        network
``networks``         list    ``[{}]``                   list of dictionaries
                                                        containing strings with
                                                        **16-digit** hexadecimal
                                                        network IDs for joining,

                                                        along with a
                                                        corresponding custom
                                                        **10-digit** ZeroTier
                                                        interface name for each
                                                        network

                                                        **note:** ensure that the
                                                        list includes at least
                                                        one such dictionary
``config_path``      string  ``/etc/openwisp/zerotier`` path to the persistent
                                                        configuration directory
``copy_config_path`` string  ``'1'``                    specifies whether to copy
                                                        the configuration file to
                                                        RAM

                                                        ``'0'`` - No, ``'1'`` -
                                                        Yes, this prevents
                                                        writing to flash in
                                                        zerotier controller mode
``secret``           string  ``''``                     identity secret of the
                                                        zerotier client (network
                                                        member), leave it blank
                                                        to be automatically
                                                        determined
``port``             integer ``9993``                   port number of the
                                                        zerotier service
``local_conf_path``  string                             path of the local
                                                        zerotier configuration
                                                        (only used for advanced
                                                        configuration)
==================== ======= ========================== =========================

Working around schema limitations
---------------------------------

The schema does not include all the possible ZeroTier settings, but it can
render appropiately any property not included in the schema as long as its
type is one the following:

- boolean
- integer
- strings
- lists

Automatic generation of clients
-------------------------------

.. automethod:: netjsonconfig.OpenWrt.zerotier_auto_client

Example (with custom zerotier interface name):

.. code-block:: python

    from netjsonconfig import OpenWrt

    client_config = OpenWrt.zerotier_auto_client(
        name="global",
        networks=[{"id": "9536600adf654321", "ifname": "owzt654321"}],
    )
    print(OpenWrt(client_config).render())

Will be rendered as:

.. code-block:: text

    package zerotier

    config zerotier 'global'
        option config_path '/etc/openwisp/zerotier'
        option copy_config_path '1'
        option enabled '1'
        list join '9536600adf654321'
        option secret '{{secret}}'

    config network 'owzt654321'
        option id '9536600adf654321'

    # ---------- files ---------- #

    # path: /etc/openwisp/zerotier/devicemap
    # mode: 0644

    # network_id=interface_name
    9536600adf654321=owzt654321

.. note::

    The current implementation of **ZeroTier VPN** backend is implemented
    with **OpenWrt** backend. Hence, the example above shows configuration
    generated for OpenWrt.

Useful resources
----------------

The default flow rules used in `zerotier/schema.py
<https://github.com/openwisp/netjsonconfig/blob/master/netjsonconfig/backends/zerotier/schema.py>`_
for the ZeroTier self-hosted controller are taken from the flow rules
mentioned in the documentation below.

- `ZeroTier Controller Network Flow Rules
  <https://docs.zerotier.com/zerotier/rules/>`_

To explore a comprehensive list of all available ZeroTier network
configuration settings, please refer to the following OpenAPI API
specifications.

- `ZeroTier Service (schema: ControllerNetwork)
  <https://docs.zerotier.com/openapi/servicev1.json>`_
- `ZeroTier Central (schema: NetworkConfig)
  <https://docs.zerotier.com/openapi/centralv1.json>`_

Advanced configuration
~~~~~~~~~~~~~~~~~~~~~~

If you want to use advanced configuration options that apply to your
OpenWrt device, such as setting up trusted paths, blacklisting physical
paths, setting up physical path hints for certain nodes, and defining
trusted upstream devices, this can be achieved by creating a file named
``local.conf`` in a persistent filesystem location, such as
``/etc/openwisp/zerotier/local.conf`` and then adding the
``local_conf_path`` option to the ZeroTier UCI configuration.

For example, let's create a local configuration file at
``/etc/openwisp/zerotier/local.conf`` (JSON) to blacklist a specific
physical network path **(10.0.0.0/24)** from all ZeroTier traffic.

.. code-block:: json

    {
      "physical": {
        "10.0.0.0/24": {
          "blacklist": true
        }
      }
    }

Now add ``local_conf_path`` option to ``/etc/config/zerotier``:

.. code-block:: text

    package zerotier

    config zerotier 'global'
        option enabled '1'
        list join '9536600adf654322'
        option secret '{{secret}}'
        option local_conf_path '/etc/openwisp/zerotier/local.conf'

**More information**

- `ZeroTier Controller Local Configuration
  <https://docs.zerotier.com/zerotier/zerotier.conf/#local-configuration-options>`_
- `OpenWrt ZeroTier Advance Configuration
  <https://openwrt.org/docs/guide-user/services/vpn/zerotier#advanced_configuration>`_
