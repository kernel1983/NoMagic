Project [https://github.com/kernel1983/NoMagic/](https://github.com/kernel1983/NoMagic/)


NoMagic 大数据框架
=======

NoMagic 是一个基于 MySQL 的大数据框架, 它可以让你方便的使用 MySQL 数据库创建分片的, 非结构的数据库方案.

它是一组函数库, 几乎全部都是函数, 用到的数据结构也都是字典, 列表. 基本上没有类的定义. 使用 NoMagic 得到的好处:

* 碎片化. 你将不用考虑当你的项目变得很大的时候, 数据库成为瓶颈.
* 非结构化. 你将无需修改你的数据库结构.

我们站在巨人的肩膀上, 我们可以很自豪的说我们并不是这个注意的原创者, 我们读了 Facebook 前 CTO [Bret Taylor](http://backchannel.org/about) 的文章 [http://backchannel.org/blog/friendfeed-schemaless-mysql](http://backchannel.org/blog/friendfeed-schemaless-mysql) [中文翻译](http://virest.org/archives/2010/07/21/how-friendfeed-uses-mysql-cn_2.html) 以后, 我们决定实现它. 现在这个框架已经在我们自己产品的生产环境中使用了.

我们使用非常函数的风格去实现了很多功能, 给一个函数起一个一眼就能看懂的名字非常重要. 这些函数除了从参数里获取数据, 返回我们需要的数据以外, 并不通过其他的途径读取数据影响返回结果(纯函数). 如果你不喜欢 ORM, 又需要处理大数据, 也许这个项目就是你要找的.

NoMagic 框架不喜欢把任何东西藏在黑盒里面. 我们希望在使用这个之前, 可以简单的阅读一下不是很长的核心部分代码. 我们也希望你可以fork我们的项目, 然后随心所欲的按照你的要求修改以及添加一些函数.

使用 NoMagic, 你将把现有的 MySQL 数据库变成一个非结构化的存储解决方案. 幸运的是, 我们发现非结构化的数据类型往往能解放程序员的思维, 提高程序员的生产效率. 我们无需再更加频繁的修改数据库结构, 这无疑会使得你的团队工作的更快一些.

学习
--------
1. 理解数据库的索引和存储.
2. 假定你有关系数据库的编程经验: 现在需要转变观念, 我们要适应 key-value 数据库的编程.
3. 搞清楚 NoMagic 数据库结构是怎么设计的.
4. 读一读我们的核心代码库, 我向你保证不是很长.
5. 自己动手试一试 NoMagic.
