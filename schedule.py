try:
    import ntptime
    ntptime.settime()
    import utime as time
except:
    import time


class ScheduleTime():
    """docstring for ScheduleTime"""

    def __init__(self, weekday, on_time, off_time, motor_speed, enable):
        self.weekday = weekday
        self.on_time = on_time
        self.off_time = off_time
        self.motor_speed = motor_speed
        self.enable = enable

    def is_now(self):
        now = time.localtime()
        now_weekday = now[6]

        if self.weekday == now_weekday:
            on_time = list(now)
            on_time[3] = self.on_time[0]
            on_time[4] = self.on_time[1]

            on_time = time.mktime(tuple(on_time))

            off_time = list(now)
            off_time[3] = self.off_time[0]
            off_time[4] = self.off_time[1]

            off_time = time.mktime(tuple(off_time))

        return on_time <= time.mktime(now) < off_time
