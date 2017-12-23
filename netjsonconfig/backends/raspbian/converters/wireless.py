from ....utils import get_copy
from .base import RaspbianConverter


class Wireless(RaspbianConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = get_copy(self.netjson, self.netjson_key)
        new_interface = {}
        for interface in interfaces:
            if interface.get('type') == 'wireless' and interface.get('wireless').get('mode') is not 'adhoc':
                wireless = interface.get('wireless')
                new_interface.update({
                    'ifname': interface.get('name'),
                    'iftype': interface.get('type'),
                    'ssid': wireless.get('ssid'),
                    'radio': wireless.get('radio'),
                    'mode': wireless.get('mode'),
                    'hidden': wireless.get('hidden', False),
                    'rts_threshold': wireless.get('rts_threshold', -1),
                    'frag_threshold': wireless.get('frag_threshold', -1),
                    'wmm': wireless.get('wmm', False),
                    'isolate': wireless.get('isolate', False),
                    'macfilter': wireless.get('macfilter', None),
                    'maclist': wireless.get('maclist', None),
                    'encryption': self._get_encryption(wireless)
                })
                self._update_radio(wireless, new_interface)
                result.append(new_interface)
        return (('wireless', result),)

    def _get_hwmode(self, radio):
        protocol = radio.get('protocol')
        if protocol in ['802.11a', '802.11b', '802.11g']:
            return protocol[-1:]
        elif radio.get('channel') <= 13:
            return 'g'
        else:
            return 'a'

    def _update_radio(self, wireless, interface):
        radios = get_copy(self.netjson, 'radios')
        if radios:
            req_radio = [radio for radio in radios if radio['name'] == wireless.get('radio')][0]
            interface.update({
                'protocol': req_radio.get('protocol').replace(".", ""),
                'hwmode': self._get_hwmode(req_radio),
                'channel': req_radio.get('channel'),
                'channel_width': req_radio.get('channel_width')
            })
            if 'country' in req_radio:
                interface.update({'country': req_radio.get('country')})

    def _get_encryption(self, wireless):
        encryption = wireless.get('encryption', None)
        new_encryption = {}
        if encryption is None or encryption.get('disabled', False) or encryption.get('protocol') == 'none':
            return new_encryption
        protocol, method = encryption.get('protocol').split("_")
        if 'wpa' in protocol:
            if 'personal' in method:
                new_encryption.update({
                    'protocol': 'wpa',
                    'method': 'personal',
                    'auth_algs': '1',
                    'wpa': '1' if protocol == 'wpa' else '2',
                    'wpa_key_mgmt': 'WPA-PSK',
                    'wpa_passphrase': encryption.get('key'),
                    'cipher': self._get_cipher(encryption),
                })
            elif method == 'enterprise':
                if wireless.get('mode') == 'access_point':
                    new_encryption.update({
                        'protocol': 'wpa',
                        'method': 'enterprise',
                        'auth_algs': '1',
                        'wpa': '1' if protocol == 'wpa' else '2',
                        'wpa_key_mgmt': 'WPA-EAP',
                        'auth_server_addr': encryption.get('server'),
                        'auth_server_port': encryption.get('port', 1812),
                        'auth_server_shared_secret': encryption.get('key', None),
                    })
                elif wireless.get('mode') == 'station':
                    if encryption.get('eap_type'):
                        eap_type = encryption.get('eap_type').upper()
                        new_encryption.update({'eap_type': eap_type})
                    new_encryption.update({
                        'protocol': 'wpa',
                        'method': 'enterprise',
                        'wpa_pairwise': self._get_cipher(encryption),
                        'identity': encryption.get('identity', None),
                        'password': encryption.get('password', None),
                        'ca_cert': encryption.get('ca_cert', None),
                        'client_cert': encryption.get('client_cert', None),
                        'priv_key': encryption.get('priv_key', None),
                        'priv_key_pwd': encryption.get('priv_key_pwd', None)
                    })
        elif 'wep' in protocol:
            new_encryption.update({
                'auth_algs': 1 if method == 'open' else 2,
                'protocol': 'wep',
                'method': method,
                'key': encryption.get('key', None)
            })
        return new_encryption

    def _get_cipher(self, encryption):
        if encryption.get('cipher'):
            return str(encryption.get('cipher').replace('+', ' ')).upper()
        else:
            return None
