================
Erlang代码热更新
================

:date: 2015-06-04
:slug: how-erlang-change-code
:tags: Erlang

Erlang代码热更新是一件很简单的事。很多教程都偏重于介绍工具的使用，而忽略了热更新过程本身。Erlang官方文档里面倒是都有，只是内容分的比较散，更适合熟悉Erlang的人查阅。

.. more


Erlang代码热更新的核心就是\ :code:`M:F(A)`\ 。以这种形式调用函数，Erlang会自动使用模块M的最新版本。这样你在Emacs里\ :code:`C-c C-k`\ 之后，不仅新启动的进程会用新版本的代码，已经启动的进程也一样会用新版本的代码，比如gen_server，就是始终以这种形式调用callback的。不过这样就假设了状态的数据格式是不变的，只适合在开发时使用，真正部署时不能就这么直接更新上去。

release_handler首先会沿着supervisor tree找出所有受影响的子进程。子进程依赖的模块，要么已经在Child Specification里有了，要么Child Specification里写的是dynamic，可以通过发get_modules消息获得。接着在载入新版本模块之前，必须暂停这些子进程，不然只要一运行\ :code:`M:F(A)`\ 就立即跳到新版本模块了。等新版本模块载入之后，再发送消息告诉这些子进程代码变了，需要执行\ :code:`code_change`\ 了。另外，release_handler还会把引用了旧版本代码的进程都杀掉，因为同一个模块在Erlang里只能有两个版本，那些进程不退出，就再也更新不了了。引用旧版本代码指的是，比如在状态中有调用下面这样的函数返回的函数。

.. code:: erlang

    f(X) ->
        fun () ->
            g(X)
        end.
