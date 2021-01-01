import uasyncio
import btree
import network
from json_helper import *


class Esp():

    @property
    def ap_password(self):
        return self._db[b"ap_password"]

    @ap_password.setter
    def ap_password(self, value):
        self._db[b"ap_password"] = value
        self._db.flush()

    @property
    def sta_enable(self):
        return self._db[b"sta_enable"]

    @sta_enable.setter
    def sta_enable(self, value):
        self._db[b"sta_enable"] = value
        self._db.flush()

    @property
    def sta_ssid(self):
        return self._db[b"sta_ssid"]

    @sta_ssid.setter
    def sta_ssid(self, value):
        self._db[b"sta_ssid"] = value
        self._db.flush()

    @property
    def sta_password(self):
        return self._db[b"sta_password"]

    @sta_password.setter
    def sta_password(self, value):
        self._db[b"sta_password"] = value
        self._db.flush()

    # AUTH_OPEN=0
    # AUTH_WEP=1
    # AUTH_WPA_PSK=2
    # AUTH_WPA2_PSK=3
    # AUTH_WPA_WPA2_PSK=4

    def __init__(self):
        try:
            f = open("config", "r+b")
        except OSError:
            f = open("config", "w+b")

        self._db = btree.open(f)

        if b"ap_password" not in self._db:
            self.db_init()

        self.ap_init()
        self.sta_init()

    async def sleep(self, s):
        await uasyncio.sleep(s)

    def db_init(self):
        self.ap_password = b"12345678"
        self.sta_enable = b"false"
        self.sta_ssid = b""
        self.sta_password = b""
        return json_result({})

    def db_read_all(self):
        return json_result(self._db)

    def ap_init(self):
        self._ap = network.WLAN(network.AP_IF)
        self._ap.active(True)
        self._ap.config(essid='CoolAir')
        return json_result({})

    def ap_change_password(self, data):
        try:
            jd = json_loads(data)
            password = jd['password']
            self.ap_password = bytes(password, 'utf-8')
        except Exception as e:
            return json_error(e)

    def sta_init(self):
        self._sta = network.WLAN(network.STA_IF)
        self.sta_active()
        self._sta.config(dhcp_hostname='CoolAir')
        return json_result({})

    def sta_active(self):
        self.sta_enable = b"true"
        self._db.flush()
        self._sta.active(True)
        return json_result({})

    def sta_deactive(self):
        self.sta_enable = b"false"
        self._db.flush()
        self._sta.active(False)
        return json_result({})

    def sta_scan(self):
        self.sta_active()
        return json_result({'access_points': self._sta.scan()})

    async def sta_connect(self, data):
        try:
            self.sta_active()
            jd = json.loads(data)
            ussid = jd['ussid']
            password = jd['password']

            self.sta_ssid = bytes(ussid, 'utf-8')
            self.sta_password = bytes(password, 'utf-8')

            self._sta.connect(ussid, password)
            await self.sleep(5)
            return self.sta_isconnected()

        except Exception as e:
            return json_error(e)

    def sta_isconnected(self):
        return json_result({'isconnected': self._sta.isconnected()})
