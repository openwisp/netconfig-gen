import json
from copy import deepcopy
from ipaddress import ip_interface, ip_network

from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter
from ..openvpn.converters import OpenVpn as BaseOpenVpn
from .schema import default_radio_driver
from .timezones import timezones


def logical_name(name):
    return name.replace('.', '_').replace('-', '_')


class General(BaseConverter):
    def to_intermediate(self):
        general = get_copy(self.netjson, 'general')
        network = self.__get_ula(general)
        system = self.__get_system(general)
        return (
            ('system', system),
            ('network', network)
        )

    def __get_system(self, general):
        if not general:
            return None
        timezone_human = general.get('timezone', 'UTC')
        timezone_value = timezones[timezone_human]
        general.update({
            '.type': 'system',
            '.name': 'system',
            'hostname': general.get('hostname', 'OpenWRT'),
            'timezone': timezone_value,
            'zonename': timezone_human,
        })
        return [sorted_dict(general)]

    def __get_ula(self, general):
        if 'ula_prefix' in general:
            ula = {
                '.type': 'globals',
                '.name': 'globals',
                'ula_prefix': general.pop('ula_prefix')
            }
            return [sorted_dict(ula)]
        return None


class Ntp(BaseConverter):
    def to_intermediate(self):
        ntp = get_copy(self.netjson, 'ntp')
        result = None
        if ntp:
            ntp.update({
                '.type': 'timeserver',
                '.name': 'ntp',
            })
            result = [sorted_dict(ntp)]
        return (('system', result),)


class Led(BaseConverter):
    def to_intermediate(self):
        result = []
        for led in get_copy(self.netjson, 'led'):
            led.update({
                '.type': 'led',
                '.name': 'led_{0}'.format(led['name'].lower()),
            })
            result.append(sorted_dict(led))
        return (('system', result),)


class Interfaces(BaseConverter):
    def to_intermediate(self):
        result = []
        # this line ensures interfaces are not entirely
        # ignored if they do not contain any address
        default_address = [{'proto': 'none'}]
        for interface in get_copy(self.netjson, 'interfaces'):
            i = 1
            is_bridge = False
            # determine uci logical interface name
            uci_name = interface.get('network', interface['name'])
            # convert dot and dashes to underscore
            uci_name = logical_name(uci_name)
            # determine if must be type bridge
            if interface.get('type') == 'bridge':
                is_bridge = True
                bridge_members = ' '.join(interface['bridge_members'])
            # ensure address list is not never empty, even when 'addresses' is []
            address_list = interface.get('addresses')
            if not address_list:
                address_list = default_address
            # address list defaults to empty list
            for address in address_list:
                # prepare new UCI interface directive
                uci_interface = deepcopy(interface)
                if 'network' in uci_interface:
                    del uci_interface['network']
                if 'mac' in uci_interface:
                    if interface.get('type') != 'wireless':
                        uci_interface['macaddr'] = interface['mac']
                    del uci_interface['mac']
                if 'autostart' in uci_interface:
                    uci_interface['auto'] = interface['autostart']
                    del uci_interface['autostart']
                if 'disabled' in uci_interface:
                    uci_interface['enabled'] = not interface['disabled']
                    del uci_interface['disabled']
                if 'addresses' in uci_interface:
                    del uci_interface['addresses']
                if 'type' in uci_interface:
                    del uci_interface['type']
                if 'wireless' in uci_interface:
                    del uci_interface['wireless']
                # default values
                address_key = None
                address_value = None
                netmask = None
                proto = self.__get_proto(uci_interface, address)
                # add suffix if there is more than one config block
                if i > 1:
                    name = '{name}_{i}'.format(name=uci_name, i=i)
                else:
                    name = uci_name
                if address.get('family') == 'ipv4':
                    address_key = 'ipaddr'
                elif address.get('family') == 'ipv6':
                    address_key = 'ip6addr'
                    proto = proto.replace('dhcp', 'dhcpv6')
                if address.get('address') and address.get('mask'):
                    address_value = '{address}/{mask}'.format(**address)
                    # do not use CIDR notation when using ipv4
                    # see https://github.com/openwisp/netjsonconfig/issues/54
                    if address.get('family') == 'ipv4':
                        netmask = str(ip_interface(address_value).netmask)
                        address_value = address['address']
                # update interface dict
                uci_interface.update({
                    '.name': name,
                    '.type': 'interface',
                    'ifname': uci_interface.pop('name'),
                    'proto': proto,
                    'dns': self.__get_dns_servers(uci_interface, address),
                    'dns_search': self.__get_dns_search(uci_interface, address)
                })
                # bridging
                if is_bridge:
                    uci_interface['type'] = 'bridge'
                    # put bridge members in ifname attribute
                    if bridge_members:
                        uci_interface['ifname'] = bridge_members
                    # if no members, this is an empty bridge
                    else:
                        uci_interface['bridge_empty'] = True
                        del uci_interface['ifname']
                    # ensure type "bridge" is only given to one logical interface
                    is_bridge = False
                # bridge has already been defined
                # but we need to add more references to it
                elif interface.get('type') == 'bridge':
                    # openwrt adds "br-"" prefix to bridge interfaces
                    # we need to take this into account when referring
                    # to these physical names
                    uci_interface['ifname'] = 'br-{0}'.format(interface['name'])
                # delete bridge_members attribtue if bridge is empty
                if uci_interface.get('bridge_members') is not None:
                    del uci_interface['bridge_members']
                # add address if any (with correct option name)
                if address_key and address_value:
                    uci_interface[address_key] = address_value
                # add netmask option (only for IPv4)
                if netmask:
                    uci_interface['netmask'] = netmask
                # merge additional address fields (discard default ones first)
                address_copy = address.copy()
                for key in ['address', 'mask', 'proto', 'family']:
                    if key in address_copy:
                        del address_copy[key]
                uci_interface.update(address_copy)
                # append to interface list
                result.append(sorted_dict(uci_interface))
                i += 1
        return (('network', result),)

    def __get_proto(self, interface, address):
        """
        determines interface "proto" option
        """
        if 'proto' not in interface:
            # proto defaults to static
            return address.get('proto', 'static')
        else:
            # allow override
            return interface['proto']

    def __get_dns_servers(self, uci, address):
        # allow override
        if 'dns' in uci:
            return uci['dns']
        # ignore if using DHCP or if "proto" is none
        if address['proto'] in ['dhcp', 'none']:
            return None
        # general setting
        dns = self.netjson.get('dns_servers', None)
        if dns:
            return ' '.join(dns)

    def __get_dns_search(self, uci, address):
        # allow override
        if 'dns_search' in uci:
            return uci['dns_search']
        # ignore if "proto" is none
        if address['proto'] == 'none':
            return None
        # general setting
        dns_search = self.netjson.get('dns_search', None)
        if dns_search:
            return ' '.join(dns_search)


class Routes(BaseConverter):
    __delete_keys = ['device', 'next', 'destination', 'cost']

    def to_intermediate(self):
        result = []
        i = 1
        for route in get_copy(self.netjson, 'routes'):
            network = ip_interface(route['destination'])
            target = network.ip if network.version == 4 else network.network
            route.update({
                '.type': 'route{0}'.format('6' if network.version == 6 else ''),
                '.name': 'route{0}'.format(i),
                'interface': route['device'],
                'target': str(target),
                'gateway': route['next'],
                'metric': route['cost'],
                'source': route.get('source')
            })
            if network.version == 4:
                route['netmask'] = str(network.netmask)
            for key in self.__delete_keys:
                del route[key]
            result.append(sorted_dict(route))
            i += 1
        return (('network', result),)


class Rules(BaseConverter):
    netjson_key = 'ip_rules'

    def to_intermediate(self):
        result = []
        i = 1
        for rule in get_copy(self.netjson, 'ip_rules'):
            src_net = None
            dest_net = None
            family = 4
            if 'src' in rule:
                src_net = ip_network(rule['src'])
            if 'dest' in rule:
                dest_net = ip_network(rule['dest'])
            if dest_net or src_net:
                family = dest_net.version if dest_net else src_net.version
            rule.update({
                '.type': 'rule{0}'.format(family).replace('4', ''),
                '.name': 'rule{0}'.format(i),
            })
            result.append(sorted_dict(rule))
            i += 1
        return (('network', result),)


class Switch(BaseConverter):
    def to_intermediate(self):
        result = []
        for switch in get_copy(self.netjson, 'switch'):
            switch.update({
                '.type': 'switch',
                '.name': switch['name'],
            })
            i = 1
            vlans = []
            for vlan in switch['vlan']:
                vlan.update({
                    '.type': 'switch_vlan',
                    '.name': '{0}_vlan{1}'.format(switch['name'], i)
                })
                vlans.append(sorted_dict(vlan))
                i += 1
            del switch['vlan']
            result.append(sorted_dict(switch))
            result += vlans
        return (('network', result),)


class Radios(BaseConverter):
    _delete_keys = ['name', 'protocol', 'channel_width']

    def to_intermediate(self):
        result = []
        for radio in get_copy(self.netjson, 'radios'):
            radio.update({
                '.type': 'wifi-device',
                '.name': radio['name'],
            })
            # rename tx_power to txpower
            if 'tx_power' in radio:
                radio['txpower'] = radio['tx_power']
                del radio['tx_power']
            # rename driver to type
            radio['type'] = radio.pop('driver', default_radio_driver)
            # determine hwmode option
            radio['hwmode'] = self.__get_hwmode(radio)
            # check if using channel 0, that means "auto"
            if radio['channel'] is 0:
                radio['channel'] = 'auto'
            # determine channel width
            if radio['type'] == 'mac80211':
                radio['htmode'] = self.__get_htmode(radio)
            # ensure country is uppercase
            if radio.get('country'):
                radio['country'] = radio['country'].upper()
            # delete unneded keys
            for key in self._delete_keys:
                del radio[key]
            # append sorted dict
            result.append(sorted_dict(radio))
        return (('wireless', result),)

    def __get_hwmode(self, radio):
        """
        possible return values are: 11a, 11b, 11g
        """
        protocol = radio['protocol']
        if protocol in ['802.11a', '802.11b', '802.11g']:
            # return 11a, 11b or 11g
            return protocol[4:]
        # determine hwmode depending on channel used
        if radio['channel'] is 0:
            # when using automatic channel selection, we need an
            # additional parameter to determine the frequency band
            return radio.get('hwmode')
        elif radio['channel'] <= 13:
            return '11g'
        else:
            return '11a'

    def __get_htmode(self, radio):
        """
        only for mac80211 driver
        """
        # allow overriding htmode
        if 'htmode' in radio:
            return radio['htmode']
        if radio['protocol'] == '802.11n':
            return 'HT{0}'.format(radio['channel_width'])
        elif radio['protocol'] == '802.11ac':
            return 'VHT{0}'.format(radio['channel_width'])
        # disables n
        return 'NONE'


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        for interface in get_copy(self.netjson, 'interfaces'):
            if 'wireless' not in interface:
                continue
            wireless = interface['wireless']
            # prepare UCI wifi-iface directive
            uci_wifi = wireless.copy()
            # inherit "disabled" attribute if present
            uci_wifi['disabled'] = interface.get('disabled')
            # add ifname
            uci_wifi['ifname'] = interface['name']
            uci_wifi.update({
                '.name': 'wifi_{0}'.format(logical_name(interface['name'])),
                '.type': 'wifi-iface',
            })
            # rename radio to device
            uci_wifi['device'] = wireless['radio']
            del uci_wifi['radio']
            # mac address override
            if 'mac' in interface:
                uci_wifi['macaddr'] = interface['mac']
            # map netjson wifi modes to uci wifi modes
            modes = {
                'access_point': 'ap',
                'station': 'sta',
                'adhoc': 'adhoc',
                'monitor': 'monitor',
                '802.11s': 'mesh'
            }
            uci_wifi['mode'] = modes[wireless['mode']]
            # map advanced 802.11 netjson attributes to UCI
            wifi_options = {
                'ack_distance': 'distance',
                'rts_threshold': 'rts',
                'frag_threshold': 'frag'
            }
            for netjson_key, uci_key in wifi_options.items():
                value = wireless.get(netjson_key)
                if value is not None:
                    # ignore if 0 (autogenerated UIs might use 0 as default value)
                    if value > 0:
                        uci_wifi[uci_key] = value
                    del uci_wifi[netjson_key]
            # determine encryption for wifi
            if uci_wifi.get('encryption'):
                del uci_wifi['encryption']
                uci_encryption = self.__get_encryption(wireless)
                uci_wifi.update(uci_encryption)
            # attached networks (openwrt specific)
            # by default the wifi interface is attached
            # to its defining interface
            # but this behaviour can be overridden
            if not uci_wifi.get('network'):
                # get network, default to ifname
                network = interface.get('network', interface['name'])
                uci_wifi['network'] = [network]
            uci_wifi['network'] = ' '.join(uci_wifi['network'])\
                                     .replace('.', '_')\
                                     .replace('-', '_')
            result.append(sorted_dict(uci_wifi))
        return (('wireless', result),)

    def __get_encryption(self, wireless):
        encryption = wireless.get('encryption', {})
        disabled = encryption.get('disabled', False)
        encryption_map = {
            'wep_open': 'wep-open',
            'wep_shared': 'wep-shared',
            'wpa_personal': 'psk',
            'wpa2_personal': 'psk2',
            'wpa_personal_mixed': 'psk-mixed',
            'wpa_enterprise': 'wpa',
            'wpa2_enterprise': 'wpa2',
            'wpa_enterprise_mixed': 'wpa-mixed',
            'wps': 'psk'
        }
        # if encryption disabled return empty dict
        if not encryption or disabled or encryption['protocol'] == 'none':
            return {}
        # otherwise configure encryption
        uci = encryption.copy()
        for option in ['protocol', 'key', 'cipher', 'disabled']:
            if option in uci:
                del uci[option]
        protocol = encryption['protocol']
        # default to protocol raw value in order
        # to allow customization by child classes
        uci['encryption'] = encryption_map.get(protocol, protocol)
        if protocol.startswith('wep'):
            uci['key'] = '1'
            uci['key1'] = encryption['key']
            # tell hostapd/wpa_supplicant key is not hex format
            if protocol == 'wep_open':
                uci['key1'] = 's:{0}'.format(uci['key1'])
        elif 'key' in encryption:
            uci['key'] = encryption['key']
        # add ciphers
        cipher = encryption.get('cipher')
        if cipher and protocol.startswith('wpa') and cipher != 'auto':
            uci['encryption'] += '+{0}'.format(cipher)
        return uci


class OpenVpn(BaseOpenVpn):
    def __get_vpn(self, vpn):
        config = super(OpenVpn, self).__get_vpn(vpn)
        if 'disabled' in config:
            config['enabled'] = not config['disabled']
            del config['disabled']
        # TODO: keep 'enabled' check until 0.6 and then drop it
        elif 'disabled' not in config and 'enabled' not in config:
            config['enabled'] = True
        config.update({
            '.name': logical_name(config.pop('name')),
            '.type': 'openvpn'
        })
        return config


class Default(BaseConverter):
    @classmethod
    def should_run(cls, config):
        """ Always runs """
        return True

    def to_intermediate(self):
        # determine config keys to ignore
        ignore_list = list(self.backend.schema['properties'].keys())
        # determine extra packages used
        extra_packages = {}
        for key, value in self.netjson.items():
            if key not in ignore_list:
                block_list = []
                # sort each config block
                if isinstance(value, list):
                    i = 1
                    for block in value[:]:
                        # config block must be a dict
                        # with a key named "config_name"
                        # otherwise it's skipped with a warning
                        if not isinstance(block, dict) or 'config_name' not in block:
                            json_block = json.dumps(block, indent=4)
                            print('Unrecognized config block was skipped:\n\n'
                                  '{0}\n\n'.format(json_block))
                            continue
                        block['.type'] = block.pop('config_name')
                        block['.name'] = block.pop('config_value',
                                                   '{0}_{1}'.format(block['.type'], i))
                        block_list.append(sorted_dict(block))
                        i += 1
                # if not a list just skip
                else:  # pragma: nocover
                    continue
                extra_packages[key] = block_list
        if extra_packages:
            return sorted_dict(extra_packages).items()
        # return empty tuple if no extra packages are used
        return tuple()
