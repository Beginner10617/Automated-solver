import time
class Clock:
    def __init__(self, tickPeriod=1/60):
        self.lastTick = time.time()
        self.period = tickPeriod

    def tick(self):
        self.lastTick = time.time()

    def setTickPeriod(self, period):
        self.period = period

    def get_time(self):
        return time.time() - self.lastTick
    
    def reset(self):
        self.lastTick = time.time()

    def waitTillNextTick(self):
        if self.get_time() < self.period:
            time.sleep(self.period - self.get_time())
        self.tick()