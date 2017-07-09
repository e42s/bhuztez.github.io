=================
在OSv上运行Erlang
=================

:date: 2015-05-14
:slug: osv-erlang
:tags: OSv, Erlang

OSv__\ 是为直接在虚拟机里运行应用程序设计的Unikernel。他们的目标是，除了一些固有的限制，比如因为只有一个地址空间，不支持多进程，以外，普通的Linux程序能直接在OSv上运行。

.. __: http://osv.io/

.. more

首先设置Erlang参数的时候，要确保会生成Position Independent Executable。把所有可以关的选项都关掉，一起来还是提示\ :code:`erts_poll_init(): Failed to get max number of files:`\ 。查了一下发现OSv的sysconf实现是不完整的，补上需要的实现，随便返回个很大的整数就好了。打上\ `这个补丁`__\ ，单线程的Erlang可以启动了。

.. __: https://github.com/cloudius-systems/osv/commit/e42258914b9b65791b1c64bee0391a5c2b0790c7

接着尝试启动支持SMP的Erlang，结果发现有人在试图运行Go时，就已经碰到了类似的问题。用了他的\ `补丁`__\ ，确实可以启动了。启动之后，明显感觉到CPU风扇在加速。一看，top里qemu进程的CPU占用率是接近200%。有人可能没注意到这个问题，就先把之前那个补丁改好\ `提交`__\ 进去了。OSv自带的gdb配置挺好用的，很快就找到了出问题的线程，但是就是不知道这线程是干啥用的。找来找去也没找到Erlang每个线程功能的文档。后来在\ `Etsukata blog: Erlang VM(BEAM) スレッド構成`__\ 里才看到比较详细的说明。对照后发现是主线程和child waiter线程在占用CPU。看了下代码，就是OSv的\ `select`__\ 和\ `waitpid`__\ 有问题。改了就好了。

.. __: https://groups.google.com/d/msg/osv-dev/C6Qc2dyv_jc/qKjA0K1ATWoJ

.. __: https://github.com/cloudius-systems/osv/commit/50a431a731af759ed3a2e774fd19b5808676cf49

.. __: http://blog.etsukata.com/2014/02/erlang-vmbeam.html

.. __: https://github.com/cloudius-systems/osv/commit/a2a4b3193d20fb0536f9ab2485b7b970a1be047c

.. __: https://github.com/cloudius-systems/osv/commit/45a703299c91c4bd839380a85daac34797855ad2


把能开的选项都开起来。接下来主要就是把那些需要额外进程的都改掉。比如，os_mon是需要启动额外进程去读取系统信息的，得从port改成port driver，然而OSv并没有实现cpu_sup需要的必要的接口，所以就先禁用了。一开始是想用纯Erlang实现的epmd server，但是这样对release改动过大，没法实用。后来看了一下，以单独线程运行epmd并没有什么问题，只要把erlexec改改就可以了。剩下一个小问题，因为现在没有能用的wordexp函数，并不能完全替代system的功能。

因为实际使用中，往往会在EC2上开多个虚拟机，不同虚拟机需要不同的配置文件。借助OSv自带的cloud-init模块把配置文件读进来，启动Erlang进程的参数，则使用erl的\ :code:`args_file`\ 从文件中读取。

接着看Elixir。Elixir的make是假的，编译到一半中断了，只能make clean之后再开始。接着发现，usr.manifest里有两个

.. code::

    /**: /path/to/some/dir

那么只能有一个生效。这导致了用这样的规则Erlang和Elixir只有一个被复制进image。

再看LFE。发现问题编译时关闭了termcap，导致运行不了。打开之后发现要把TERM环境变量设置成\ :code:`vt100-qemu`\ ，不然Erlang的ttsl_drv就不工作了。这样就把LFE Shell开起来了。
