# -*- coding: UTF-8 -*-
import datetime
import os

print(os.path.join(os.path.realpath(r"system_backend\files"), "aa.doc"))

print((datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S"))