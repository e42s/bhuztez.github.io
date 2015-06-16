============
不动点组合子
============

:date: 2014-03-29
:slug: y-combinator


最近有一个很奇怪的现象。也许仅仅是因为刚好有一家公司叫Y Combinator，有不少人在写博客鼓吹不动点组合子，以学会不动点组合子为荣。

.. more

一般来说，当你发现需要用不动点组合子时，一定是哪里出了问题。比如在Erlang R17之前，你要在Erlang Shell里写递归函数，就得重新发明不动点组合子了。讨厌不动点组合子才是正常的。

比如阶乘，像下面这样的代码是不行的。在定义函数时，Fact变量还没有定义。

.. code:: erlang

    Fact = fun (0) -> 1; (N) -> N*Fact(N-1) end.

可以多接受一个参数，用来传入函数本身，在递归时再继续传下去，这样就没问题了。

.. code:: erlang

    X1 = fun(_,0) -> 1; (F,N) -> N*F(F,N-1) end,
    Y1 = fun(F) -> fun(N) -> F(F,N) end end,
    Fact1 = Y1(X1).


这已经有和不动点组合子相当的功能了。可这样的写法很别扭。当然更希望写成下面这样。

.. code:: erlang

    X2 = fun(_,0) -> 1; (F,N) -> N*F(N-1) end.

想要达到下面这样的效果

.. code:: erlang

    Y2 = fun(F) -> G = fun(N) -> F(G,N) end end.

使用和上面类似的技巧，就可以了

.. code:: erlang

    Y2 = fun(F) -> H = fun(G) -> fun(N) -> F(G(G),N) end end, H(H) end.
    Fact2 = Y2(X2).

在lambda calculus里，每个函数只接受一个参数

.. code:: erlang

    X3 = fun(F) -> fun(0) -> 1; (N) -> N*F(N-1) end end.
    Y3 = fun(F) -> (fun (X) -> X(X) end)(fun(G) -> fun(N) -> (F(G(G)))(N) end end) end.
    Fact3 = Y3(X3).

你一定看出来了这个形式和Haskell Curry提出的不动点组合子并不一致。我想你也猜到为什么了。

上面的写法的问题是得为不同的参数个数分别定义一个组合子。所以Erlang R17里引入了新的写法解决这个问题。

.. code:: erlang

    Fact = fun F(0) -> 1; F(N) -> N*F(N-1) end.

终于不用再写不动点组合子了。
