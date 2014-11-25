用Django ORM动态生成SQL
=======================

:date: 2010-09-17
:slug: django-query-to-sql

去年的时候，就想自己仿个 GitHub_ 玩玩。可是， Git_ 并不像 Mercurial_ 那样原生支持HTTP协议，得用SSH来限制用户访问。 GitHub_ 和 Gitorious_ 也都是那么做的。 而 Gitosis_ 和 Gitolite_ 用起来都不是很方便， 后来看到 Twisted_ 也实现了SSH协议，想在上面改改就拿来用，毕竟不能直接拿来用，也一直没去看，就这样不了了之了。直到某日，看到 `Serving Git <http://deadpuck.net/blag/serving-git/>`_ 。这样SSH的问题就解决了。顺着那篇文章的思路下来，就想用 Django_ 弄个Web界面让用户来管理密钥，很快就弄好了，没有遇到任何困难。

.. _GitHub: https://github.com/ 
.. _Git: http://git-scm.com/
.. _Mercurial: http://mercurial.selenic.com/
.. _Gitorious: http://gitorious.org/
.. _Gitosis: http://eagain.net/gitweb/?p=gitosis.git
.. _Gitolite: https://github.com/sitaramc/gitolite
.. _Twisted: http://twistedmatrix.com/
.. _Django: http://www.djangoproject.com/

.. more

不过，既然是用 Twisted_ ，用 Django_ 来操作数据库总觉得有点怪怪的。尽管自己测试的时候，下面这样的代码运行起来也没什么问题。

.. code:: python

    class PublicKeyChecker(SSHPublicKeyDatabase):

        def checkKey(self, credentials):
            keystring = Key.fromString(credentials.blob).toString("OPENSSH")

            return PublicKey.objects.filter(
                user__username = credentials.username,
                keystring = keystring).exists()


因为 ``PublicKeyChecker`` 继承自 ``SSHPublicKeyDatabase`` ， 看了下 ``twisted.conch.checkers`` ，看到了一个 ``maybeDeferred``  [#deferred]_ 。下面就是相关部分的代码：

.. code:: python

    class SSHPublicKeyDatabase:

        def requestAvatarId(self, credentials):
            d = defer.maybeDeferred(self.checkKey, credentials)
            d.addCallback(self._cbRequestAvatarId, credentials)
            d.addErrback(self._ebRequestAvatarId)
            return d


Twisted_ 里需要用 ``twisted.enterprise.adbapi`` 来操作数据库，而这玩意儿需要直接传入SQL语句 [#adbapi]_ 。在 Django_ 里是用ORM解决问题的，还是希望在这里尽量不要硬编码SQL语句了。看了看 Django_ 的源代码，找到了这么个办法，可以得到对应 ``queryset`` 的SQL语句。

.. code:: python

    qs = PublicKey.objects.filter(
        user__username = credentials.username,
        keystring = keystring)
    
    compiler = qs.query.get_compiler(using=qs.db)
    sql, params = compiler.as_sql()

但是， ``sqlite3`` 会对这样生成的SQL语句报错。需要用 ``cursor.convert_query(sql)`` 把里面的 ``%s`` 之类的转换成 "``?``"（问号）。

.. code:: python

    cursor = compiler.connection.cursor()
    sql = cursor.convert_query(sql)

终于可以返回查询了。

.. code:: python

    return dbpool.runQuery(sql, params)


我们只需要知道有没有，不需要取回这么多数据，因为 ``[:1]`` 会直接取出结果，所以用 ``qs.query.set_limits`` 。

.. code:: python

    qs = PublicKey.objects.filter(
        user__username = credentials.username,
        keystring = keystring).only("id")
    qs.query.set_limits(0,1)


把前面的连起来

.. code:: python

    class PublicKeyChecker(SSHPublicKeyDatabase):

        def checkKey(self, credentials):
            keystring = Key.fromString(credentials.blob).toString("OPENSSH")

            qs = PublicKey.objects.filter(
                user__username = credentials.username,
                keystring = keystring).only("id")
            qs.query.set_limits(0,1)
        
            compiler = qs.query.get_compiler(using=qs.db)
            sql, params = compiler.as_sql()
 
            cursor = compiler.connection.cursor()
            sql = cursor.convert_query(sql)
        
            return dbpool.runQuery(sql, params)


.. [#deferred] 关于 ``Deferred`` 可以参考 `Deferred Reference <http://twistedmatrix.com/documents/current/core/howto/defer.html>`_ （2010年8月22日查阅）

.. [#adbapi] 参考 `twisted.enterprise.adbapi: Twisted RDBMS support <http://twistedmatrix.com/documents/current/core/howto/rdbms.html>`_ （2010年8月22日查阅）
