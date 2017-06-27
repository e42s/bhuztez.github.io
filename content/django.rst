=======================
用Django ORM动态生成SQL
=======================

:date: 2010-09-17
:slug: django-query-to-sql
:tags: Django, Twisted, Git, SSH, How-to

去年就想自己仿个\ GitHub_\ 。可是，\ Git_\ 并不像\ Mercurial_\ 那样原生支持HTTP协议，一般都是用SSH协议来限制用户访问。比如，GitHub和\ Gitorious_\ 都是那么做的。 而\ Gitosis_\ 和\ Gitolite_\ 用起来并不是很方便。后来看到\ `Serving Git <http://deadpuck.net/blag/serving-git/>`_\ 一文，就决定用\ Twisted_\ 来处理SSH协议。顺便用\ Django_\ 弄了个Web界面让用户来上传公钥密钥。

.. _GitHub: https://github.com/
.. _Git: http://git-scm.com/
.. _Mercurial: http://mercurial.selenic.com/
.. _Gitorious: http://gitorious.org/
.. _Gitosis: http://eagain.net/gitweb/?p=gitosis.git
.. _Gitolite: https://github.com/sitaramc/gitolite
.. _Twisted: http://twistedmatrix.com/
.. _Django: http://www.djangoproject.com/

.. more

下面的代码是可以运行的。不过，Twisted是异步的，而Django操作数据库会阻塞，查一次公钥就把整个线程卡住了，要等查好了才能继续，这样并不对。

.. code:: python

    class PublicKeyChecker(SSHPublicKeyDatabase):

        def checkKey(self, credentials):
            keystring = Key.fromString(credentials.blob).toString("OPENSSH")

            return PublicKey.objects.filter(
                user__username = credentials.username,
                keystring = keystring).exists()


因为\ :code:`PublicKeyChecker`\ 继承自\ :code:`SSHPublicKeyDatabase`\ ， 看了下\ :code:`twisted.conch.checkers`\ ，看到了一个\ :code:`maybeDeferred` [#deferred]_\ 。下面就是相关部分的代码：

.. code:: python

    class SSHPublicKeyDatabase:

        def requestAvatarId(self, credentials):
            d = defer.maybeDeferred(self.checkKey, credentials)
            d.addCallback(self._cbRequestAvatarId, credentials)
            d.addErrback(self._ebRequestAvatarId)
            return d


Twisted里用\ :code:`twisted.enterprise.adbapi`\ 来操作数据库，而需要直接传入SQL语句\ [#adbapi]_\ 。在Django里是用ORM解决问题的，还是希望在这里尽量不要硬编码SQL语句了。看了看Django的源代码，这样就可以得到对应\ :code:`queryset`\ 的SQL语句。

.. code:: python

    qs = PublicKey.objects.filter(
        user__username = credentials.username,
        keystring = keystring)

    compiler = qs.query.get_compiler(using=qs.db)
    sql, params = compiler.as_sql()

但是，\ :code:`sqlite3`\ 会对这样生成的SQL语句报错。需要用\ :code:`cursor.convert_query(sql)`\ 把里面的\ :code:`%s`\ 之类的转换成\ :code:`?`\ 。

.. code:: python

    cursor = compiler.connection.cursor()
    sql = cursor.convert_query(sql)

终于可以返回查询了。

.. code:: python

    return dbpool.runQuery(sql, params)


我们只需要知道有没有，并不需要把所有数据都取回来，因为\ :code:`[:1]`\ 会直接取出结果，所以用\ :code:`qs.query.set_limits`\ 。

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


.. [#deferred] 关于\ :code:`Deferred`\ 可以参考 `Deferred Reference <http://twistedmatrix.com/documents/current/core/howto/defer.html>`_ （2010年8月22日查阅）

.. [#adbapi] 参考 `twisted.enterprise.adbapi: Twisted RDBMS support <http://twistedmatrix.com/documents/current/core/howto/rdbms.html>`_ （2010年8月22日查阅）
