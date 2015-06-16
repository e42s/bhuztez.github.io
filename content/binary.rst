================
Erlang字符串输出
================

:date: 2015-05-08
:slug: erlang-binary


经常有人莫名其妙的抱怨Erlang字符串处理效率低下。在过去，Erlang确实是用简单的list来表示字符串的，不停拼接list效率确实不行。可现在这已经是老黄历了。

.. more

Erlang里引入了binary。在拼接字符串的时候没必要复制，直接构造一个新的list就完事了。反正标准库函数一般都能接受这种用法，最后就直接就当 iovec 发出去了。

.. code:: erlang

    IOList3 = [IOList1, IOList2].


这里先无视各种不常用的情况，iolist的类型定义可以写成


.. code:: erlang

    -type iolist() :: binary() | [iolist()].


我就是要把两个binary拼起来怎么办？比如


.. code:: erlang

    Bin3 = <<Bin1/binary, Bin2/binary>>


Erlang会机智的计算出Bin1, Bin2 长度之和，先占好空间，再把字符串都复制进去。和你在别的语言里手动复制字符串并没有什么区别。
