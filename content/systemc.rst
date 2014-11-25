编译SystemC 2.2.0的问题
=======================

:date: 2009-04-12
:slug: compiling-systemc

居然连编译都有困难，SystemC的表现令人失望。看了\ `这个帖子`__\ 的#7之后，才发现居然还是个低级错误，要修改 :code:`systemc-2.2.0/src/sysc/utils/sc_utils_ids.cpp` 这个文件，更加C++一点的写法是像下面这样的：

__ http://forums.fedoraforum.org/showthread.php?t=199153

.. more

.. code:: c++

    #include <cstdlib>
    #include <cstring>


另外，SCV在我这里就连configure都不行，后来一看，竟然从2006年到现在还没更新过，怪不得里面用的automake的版本号都小得有点离奇。
