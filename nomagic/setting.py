#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    from tornado import database
except:
    import torndb as database

conn = database.Connection("127.0.0.1", "test", "root", "root")
conn1 = database.Connection("127.0.0.1", "test", "root", "root")
conn2 = database.Connection("127.0.0.1", "test", "root", "root")
conn3 = database.Connection("127.0.0.1", "test", "root", "root")

ring = [conn1, conn2, conn3]
