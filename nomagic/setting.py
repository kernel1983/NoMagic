#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
	from tornado import database
except:
	import database

conn = tornado.database.Connection("127.0.0.1", "test", "root", "root")
conn1 = tornado.database.Connection("127.0.0.1", "test", "root", "root")
ring = [conn1, conn1, conn1]