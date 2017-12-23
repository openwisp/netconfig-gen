================
Raspbian Backend
================

.. include:: ../_github.rst

The ``Raspbian`` backend allows to Raspbian compatible configuration files.

.. warning::
    This backend is in experimental stage: it may have bugs and it will
    receive backward incompatible updates during the first 6 months
    of development (starting from September 2017).
    Early feedback and contributions are very welcome and will help
    to stabilize the backend faster.

Initialization
--------------

.. automethod:: netjsonconfig.Raspbian.__init__

Render method
-------------

.. automethod:: netjsonconfig.Raspbian.render

Code example:

.. code-block:: python

    from netjsonconfig import Raspbian

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
    print o.render()

Will return the following output::

    # config: /etc/network/interfaces

    auto eth0
    iface eth0 inet static
    address 192.168.1.1
    netmask 255.255.255.0
    iface eth0 inet6 static
    address fd87::1
    netmask 128

Generate method
---------------

.. automethod:: netjsonconfig.Raspbian.generate

Code example:

.. code-block:: python

    >>> import tarfile
    >>> from netjsonconfig import Raspbian
    >>>
    >>> o = Raspbian({
    ...     "interfaces": [
    ...     {
    ...         "name": "eth0",
    ...         "type": "ethernet",
    ...         "addresses": [
    ...             {
    ...                 "proto": "dhcp",
    ...                 "family": "ipv4"
    ...             }
    ...         ]
    ...     }
    ...     ]
    ... })
    >>> stream = o.generate()
    >>> print(stream)
    <_io.BytesIO object at 0x7f8bc6efb620>
    >>> tar = tarfile.open(fileobj=stream, mode='r:gz')
    >>> print(tar.getmembers())
    [<TarInfo '/etc/network/interfaces' at 0x7f8bc6f08048>]

The ``generate`` method does not write to disk but instead returns a instance of
``io.BytesIO`` which contains a tar.gz file object.

Write method
------------

.. automethod:: netjsonconfig.Raspbian.write

Example:

.. code-block:: python

    >>> import tarfile
    >>> from netjsonconfig import Raspbian
    >>>
    >>> o = Raspbian({
    ...     "interfaces": [
    ...     {
    ...         "name": "eth0",
    ...         "type": "ethernet",
    ...         "addresses": [
    ...             {
    ...                 "proto": "dhcp",
    ...                 "family": "ipv4"
    ...             }
    ...         ]
    ...     }
    ...     ]
    ... })
    >>> o.write('dhcp-router', path='/tmp/')

Writes the configuration archive in ``/tmp/dhcp-router.tar.gz``

General settings
----------------

The general settings reside in the ``general`` key of the
*configuration dictionary*, which follows the
`NetJSON General object <http://netjson.org/rfc.html#general1>`_ definition
(see the link for the detailed specification).

General settings example
~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "general": {
            "hostname": "RaspberryPi",
            "timezone": "UTC"
        }
    }

Will be rendered as follows::

    # config: /etc/hostname

    RaspberryPi

    # script: /scripts/general.sh

    /etc/init.d/hostname.sh start
    echo "Hostname of device has been modified"
    timedatectl set-timezone UTC
    echo "Timezone has changed to UTC"


After modifying the config files run the following command to change the
hostname::

    source scripts/general.sh

Network interfaces
------------------

The network interface settings reside in the ``interfaces`` key of the
*configuration dictionary*, which must contain a list of
`NetJSON interface objects <http://netjson.org/rfc.html#interfaces1>`_
(see the link for the detailed specification).

There are 3 main type of interfaces:

* **network interfaces**: may be of type ``ethernet``, ``virtual``, ``loopback`` or ``other``
* **wireless interfaces**: must be of type ``wireless``
* **bridge interfaces**: must be of type ``bridge``

Dualstack (IPv4 & IPv6)
~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet",
                "addresses": [
                    {
                        "family": "ipv4",
                        "proto": "static",
                        "address": "10.27.251.1",
                        "mask": 24
                    },
                    {
                        "family": "ipv6",
                        "proto": "static",
                        "address": "fdb4:5f35:e8fd::1",
                        "mask": 48
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    # config: /etc/network/interfaces

    auto eth0
    iface eth0 inet static
    address 10.27.251.1
    netmask 255.255.255.0
    iface eth0 inet6 static
    address fdb4:5f35:e8fd::1
    netmask 48

DNS Servers and Search Domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DNS servers can be set using ``dns_servers``, while search domains can be set using
``dns_search``.

.. code-block:: python

    {
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
        ],
        "dns_servers": [
            "10.11.12.13",
            "8.8.8.8"
        ],
        "dns_search": [
            "openwisp.org",
            "netjson.org"],
    }

Will return the following output::

    # config: /etc/network/interfaces

    auto eth0
    iface eth0 inet static
    address 192.168.1.1
    netmask 255.255.255.0

    auto eth1
    iface eth1 inet dhcp

    # config: /etc/resolv.conf

    nameserver 10.11.12.13
    nameserver 8.8.8.8
    search openwisp.org
    search netjson.org

DHCP IPv6 Ethernet Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
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
    }

Will be rendered as follows::

    # config: /etc/network/interfaces

    auto eth0
    iface eth0 inet6 dhcp

Bridge Interfaces
-----------------

Interfaces of type ``bridge`` can contain a option that is specific for network bridges:

* ``bridge_members``: interfaces that are members of the bridge

.. note::
    The bridge members must be active when creating the bridge

Installing the Software
~~~~~~~~~~~~~~~~~~~~~~~

To create a bridge interface you will need to install a program called `brctl` and
is included in `bridge-utils <https://packages.debian.org/search?keywords=bridge-utils>`_.
You can install it using this command::

    $ aptitude install bridge-utils

Bridge Interface Example
~~~~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "lan",
                "type": "bridge",
                "bridge_members": [
                    "eth0",
                    "eth1"
                ],
                "addresses": [
                    {
                        "address": "172.17.0.2",
                        "mask": 24,
                        "proto": "static",
                        "family": "ipv4"
                    }
                ]
            }
        ]
    }

Will be rendered as follows::

    # config: /etc/network/interfaces

    auto lan
    iface lan inet static
    address 172.17.0.2
    netmask 255.255.255.0
    bridge_ports eth0 eth1

Wireless Settings
-----------------

To use a Raspberry Pi as various we need first install the required packages.
You can install it using this command::

    $ sudo apt-get install hostapd dnsmasq

* **hostapd** - The package allows you to use the wireless interface in various
  modes
* **dnsmasq** - The package converts the Raspberry Pi into a DHCP and DNS server

Since the configuration files are not ready yet, turn the new softwares off as follows::

    $ sudo systemctl stop dnsmasq
    $ sudo systemctl stop hostapd

Configure your interface
~~~~~~~~~~~~~~~~~~~~~~~~

Let us say that ``wlan0`` is our wireless interface which we will be using.
First the standard interface handling for ``wlan0`` needs to be disabled.
Normally the dhcpcd daemon (DHCP client) will search the network for a DHCP server
to assign a IP address to ``wlan0`` This is disabled by editing the configuration
file ``/etc/dhcpcd.conf``.
Add ``denyinterfaces wlan0`` to the end of the line (but above any other added
``interface`` lines) and save the file.


To configure the static IP address, create a backup of the original
``/etc/network/interfaces``. Then replace the the file with the one generated
by the backend. Now restart the dhcpcd daemon and setup the new ``wlan0`` configuration::

    sudo service dhcpcd restart
    sudo ifdown wlan0
    sudo ifup wlan0

Configure hostapd
~~~~~~~~~~~~~~~~~

Create a new configuration file ``/etc/hostapd/hostapd.conf``. The contents of this
configuration will be generated by the backend.

You can check if your wireless service is working by running ``/usr/sbin/hostapd /etc/hostapd/hostapd.conf``.
At this point you should be able to see your wireless network. If you try to connect
to this network, it will authenticate but will not recieve any IP address until
dnsmasq is setup. Use **Ctrl+C** to stop it.
If you want the wireless service to start automatically at boot, find the line::

    #DAEMON_CONF=""

in ``/etc/default/hostapd`` and replace it with::

    DAEMON_CONF="/etc/hostapd/hostapd.conf"

Configure dnsmasq
~~~~~~~~~~~~~~~~~

By default ``/etc/dnsmasq.conf`` contains the complete documentation for how the
file needs to be used. It is advisable to create a copy of the original ``dnsmasq.conf``.
After creating the backup, delete the original file and create a new file ``/etc/dnsmasq.conf``
Setup your DNS and DHCP server. Below is an example configuration file::

    # Use interface wlan0
    interface=wlan0
    # Assign IP addresses between 172.128.1.50 and 172.128.1.150 with a 12 hour lease time
    dhcp-range=172.128.1.50,172.128.1.150,12h

Setup IPv4 Forwarding
~~~~~~~~~~~~~~~~~~~~~

We need to enable packet forwarding. Open ``/etc/sysctl.conf`` and uncomment the
following line::

    #net.ipv4.ip_forward=1

After enabling IPv4 Forwarding in ``/etc/sysctl.conf`` you can run the bash script
``/scripts/ipv4_forwarding.sh`` generated in your ``tar.gz`` file::

    source scripts/ipv4_forwarding.sh

This will enable IPv4 forwarding, setup a NAT between your two interfaces and save the
iptable in ``/etc/iptables.ipv4.nat``.
These rules must be applied everytime the Raspberry Pi is booted up. To do so open the
`/etc/rc.local` file and just above the line ``exit 0``, add the following line::

    iptables-restore < /etc/iptables.ipv4.nat

Now we just need to start our services::

    sudo service hostapd start
    sudo service dnsmasq start

You should now be able to connect to your wireless network setup on the Raspberry Pi

Wireless access point
~~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary* represent one of the most
common wireless access point configuration:

.. code-block:: python

    {
        "radios": [
              {
                  "name": "radio0",
                  "phy": "phy0",
                  "driver": "mac80211",
                  "protocol": "802.11n",
                  "channel": 3,
                  "channel_width": 20,
              },
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
    }

Will be rendered as follows::

    # config: /etc/hostapd/hostapd.conf

    interface=wlan0
    driver=nl80211
    hw_mode=g
    channel=3
    ieee80211n=1
    ssid=myWiFi

    # config: /etc/network/interfaces

    auto wlan0
    iface wlan0 inet manual

    # script: /scripts/ipv4_forwarding.sh

    sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
    sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

Wireless AdHoc Mode
~~~~~~~~~~~~~~~~~~~

In wireless adhoc mode, the ``bssid`` property is required.

The following example:

.. code-block:: python

    {
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
    }

Will result in::

    # config: /etc/network/interfaces

    auto wireless
    iface wireless inet static
    address 172.128.1.1
    netmask 255.255.255.0
    wireless-channel 1
    wireless-essid freifunk
    wireless-mode ad-hoc

WPA2 Personal (Pre-Shared Key)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows a typical wireless access
point using *WPA2 Personal (Pre-Shared Key)* encryption:

.. code-block:: python

    {
        "radios": [
            {
                "name": "radio0",
                "phy": "phy0",
                "driver": "mac80211",
                "protocol": "802.11n",
                "channel": 3,
                "channel_width": 20,
            }
        ],
        "interfaces": [
            {
                "name": "wlan0",
                "type": "wireless",
                "wireless": {
                    "radio": "radio0",
                    "mode": "access_point",
                    "ssid": "wpa2-personal",
                    "encryption": {
                        "protocol": "wpa2_personal",
                        "cipher": "tkip+ccmp",
                        "key": "passphrase012345"
                    }
                }
            }
        ]
    }

Will be rendered as follows::

    # config: /etc/hostapd/hostapd.conf

    interface=wlan0
    driver=nl80211
    hw_mode=g
    channel=3
    ieee80211n=1
    ssid=wpa2-personal
    auth_algs=1
    wpa=2
    wpa_key_mgmt=WPA-PSK
    wpa_passphrase=passphrase012345
    wpa_pairwise=TKIP CCMP

    # config: /etc/network/interfaces

    auto wlan0
    iface wlan0 inet manual

    # script: /scripts/ipv4_forwarding.sh

    sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
    sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

Radio settings
--------------

The radio settings reside in the ``radio`` key of the *configuration dictionary*,
which must contain a list of `NetJSON radio objects <http://netjson.org/rfc.html#radios1>`_
(see the link for the detailed specification).

Radio object extensions
~~~~~~~~~~~~~~~~~~~~~~~

In addition to the default *NetJSON Radio object options*, the ``Raspbian`` backend
also requires setting the following additional options for each radio in the list:

+--------------+---------+-----------------------------------------------+
| key name     | type    | allowed values                                |
+==============+=========+===============================================+
| ``protocol`` | string  | 802.11a, 802.11b, 802.11g, 802.11n, 802.11ac  |
+--------------+---------+-----------------------------------------------+

Radio example
~~~~~~~~~~~~~

The following *configuration dictionary*:

.. code-block:: python

    {
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
    }

Will be rendered as follows::

    # config: /etc/hostapd/hostapd.conf

    interface=wlan0
    driver=nl80211
    hw_mode=g
    channel=11
    ieee80211n=1
    ssid=myWiFi

    # config: /etc/network/interfaces

    auto wlan0
    iface wlan0 inet manual

    # script: /scripts/ipv4_forwarding.sh

    sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
    sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

Static Routes
-------------

The static routes settings reside in the ``routes`` key of the *configuration dictionary*,
which must contain a list of `NetJSON Static Route objects <http://netjson.org/rfc.html#routes1>`_
(see the link for the detailed specification).
The following *configuration dictionary*:


Static route example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    {
        "interfaces": [
            {
                "name": "eth0",
                "type": "ethernet"
            }
        ],
        "routes": [
            {
                "device": "eth0",
                "destination": "192.168.4.1/24",
                "next": "192.168.2.2",
                "cost": 2,
            },
        ]
    }

Will be rendered as follows::

    # config: /etc/network/interfaces

    auto eth0
    iface eth0 inet manual
    post-up route add -net 192.168.4.1 netmask 255.255.255.0 gw 192.168.2.2
    pre-up route del -net 192.168.4.1 netmask 255.255.255.0 gw 192.168.2.2

NTP settings
------------

The Network Time Protocol settings reside in the ``ntp`` key of the
*configuration dictionary*, which is a custom NetJSON extension not present in
the original NetJSON RFC.

The ``ntp`` key must contain a dictionary, the allowed options are:

+-------------------+---------+---------------------+
| key name          | type    | function            |
+===================+=========+=====================+
| ``enabled``       | boolean | ntp client enabled  |
+-------------------+---------+---------------------+
| ``enable_server`` | boolean | ntp server enabled  |
+-------------------+---------+---------------------+
| ``server``        | list    | list of ntp servers |
+-------------------+---------+---------------------+

NTP settings example
~~~~~~~~~~~~~~~~~~~~

The following *configuration dictionary* :

.. code-block:: python

    {
        "ntp": {
        "enabled": True,
        "enable_server": False,
        "server": [
            "0.pool.ntp.org",
            "1.pool.ntp.org",
            "2.pool.ntp.org"
        ]
    }

Will be rendered as follows::

    # config: /etc/ntp.conf

    server 0.pool.ntp.org
    server 1.pool.ntp.org
    server 2.pool.ntp.org
