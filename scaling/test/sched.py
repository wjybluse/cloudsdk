# -*- coding: utf-8 -*-
__author__ = 'wan'
import uuid
from scaling.rule.timerwheel import TimerWheel


def ttt():
    print(str(uuid.uuid1()))


if __name__ == '__main__':
    tw = TimerWheel()
    tw.add_task('hahh', ttt)
    tw.start()
