==============
比谁accept()快
==============

:date: 2013-11-23
:slug: benchmarking-accept
:tags: Joke
:status: draft

不知道为什么\ `国内技术第一的开源社区`__\ 会去\ `反驳`__\ 一个\ `很不合理的benchmark`__\ 。那个benchmark竟然用了Erlang臭名昭著的\ :code:`io:format`\ ，莫名其妙的把\ :code:`socket`\ 设置成\ :code:`active`\ ，还不自量力的和C++去比速度，C++代码还是Boost库文档里的\ `例子`__\ 。

__ http://avplayer.org/
__ http://avboost.com/t/asio/347
__ http://my.oschina.net/u/200693/blog/34462
__ http://www.boost.org/doc/libs/1_55_0/doc/html/boost_asio/example/cpp03/echo/async_tcp_echo_server.cpp

.. more

而国内技术第一的开源社区给出的benchmark实际上就是比\ :code:`accept()`\ 。所以要把调用\ :code:`accept`\ 的\ :code:`process`\ 的\ :code:`priority`\ 设置成\ :code:`max`\ 才行。另外，Erlang默认的port数量设得比较小，需要把\ :code:`ERL_MAX_PORTS`\ 改得大一点。

国内技术第一的开源社区的benchmark就一次10000个连接，结束得太快了。我又懒得改ulimit上限，同时只有4000个就只有4000个吧，总数设成80万个连接。不会C++，就用C\ `写了`__\ 。

__ {filename}accept/client.c

`C`__\ 的结果

__ {filename}accept/server.c

.. code::

    real    1m34.921s
    user    0m0.498s
    sys     1m9.674s

`Boost/ASIO`__\ 的结果

__ {filename}accept/server.cpp

.. code::

    real    1m34.972s
    user    0m0.495s
    sys     1m10.013s

`Erlang`__\ 的结果

__ {filename}accept/server.erl

.. code::

    real    1m39.437s
    user    0m0.520s
    sys     1m11.655s

可以看到，区区80万个连接，Erlang就比C++慢了5秒。对于每天HTTP请求数动辄上十亿的巨型网站来说，每80亿个连接，Erlang仅\ :code:`accept()`\ 就会比C++多花5万秒啊，一天也就8万多秒，哪里还有时间来运行业务逻辑啊。

整天摆弄micro benchmark，不去探索不去尝试的弊病，Rob Pike早就\ `吐槽`__\ 过了。

.. __: http://doc.cat-v.org/bell_labs/utah2000/
