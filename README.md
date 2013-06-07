Project [https://github.com/kernel1983/NoMagic/](https://github.com/kernel1983/NoMagic/) >> [如果你更喜欢读中文](README_cn.md)


NoMagic big data framework
=======

NoMagic is a MySQL based big data framework which enable you to create sharding data structure from the beginning of project.

* sharding

This framework stands on the shoulders of giants, we borrowed the idea from [Bret Taylor](http://backchannel.org/about)'s article [http://backchannel.org/blog/friendfeed-schemaless-mysql](http://backchannel.org/blog/friendfeed-schemaless-mysql)

We use function to implement a lot of helper function, I believe each action in database should be given a friendly function name, and the function should always return the same result of data if you give right parameters. If you don't like ORM, we may be looking for this project.

NoMagic framework doesn't try to put anything into the blackbox. We hope you read the core source code and try to get fully understanding before you start to using it. And we hope you forking our project and creating your own database helper function sets based on your need.

Using NoMagic, you will turn the MySQL database into a schemaless solution, the schemaless database will save your time so that you don't need to spend to much time in planning database table structure.


Learning
--------
1. Understand what is index and what is payload in database world.
2. The concept change of key-value database programming.
3. NoMagic database structure design.
4. [Read the core function library](docs/__init__.py.md).
5. Play around with NoMagic.

