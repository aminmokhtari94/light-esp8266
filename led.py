import uasyncio
import btree
import network
from json_helper import json_loads, json_error, json_result


# def main():
# 	s=ScheduleTime(4,(11,5),(11,22),3)
# 	print(s.is_now())
# main()


class Led:
    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def cold(self):
        return int(self._db[b"cold"])

    @cold.setter
    def cold(self, value):
        self._db[b"cold"] = bytes(str(value), 'utf-8')
        self._db.flush()

    @property
    def warm(self):
        return int(self._db[b"warm"])

    @warm.setter
    def warm(self, value):
        self._db[b"warm"] = bytes(str(value), 'utf-8')
        self._db.flush()

    def __init__(self):
        self._power = True

        try:
            f = open("led", "r+b")
        except OSError:
            f = open("led", "w+b")

        self._db = btree.open(f)
        if b'cold' not in self._db:
            self.db_init()

    def db_init(self):
        self.cold = 0
        self.warm = 0

    def set_vars(self, data):
        try:
            jd = json_loads(data)

            if 'cold' in jd:
                self.cold = jd['cold']

            if 'warm' in jd:
                self.motor_speed = jd['warm']

            return self.get_vars()
        except Exception as e:
            return json_error(e)

    def get_vars(self):
        res = {
            'cold': self.cold,
            'warm': self.warm,
        }
        return json_result(res)
