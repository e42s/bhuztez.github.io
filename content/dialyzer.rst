========
Dialyzer
========

:date: 2015-02-02
:slug: dialyzer


动态类型语言的静态类型分析突然变成了一件时髦的事。Facebook推出的Hack语言吸引了大量关注。王垠靠PySonar也收获了很多粉丝。可是Erlang依旧被认为是老土。

.. more

在Hack和PySonar的开发开始之前，Erlang里就已经有了Dialyzer和Typer。前者可以检查类型是否符合spec，后者可以分析出程序的类型。不仅仅是这样，HiPE会根据Type Inference得到的类型信息把Erlang代码编译成Native code。实际上是先有HiPE的。Dialyzer和Typer里的类型分析算法最早就是从HiPE里拿来的。而且假如你不开HiPE，Dialyzer在给标准库建plt文件时，会花费特别长的时间。也就是说没有HiPE，这检查的速度根本就不实用。更可恶的是，运行的时候能用掉你所有核心100%的CPU时间，忘了在启动前加上比如 :code:`+S 1:1` 这样的参数可就惨了。

假如你是非要看论文，那么可以看看 `DIALYZER: a DIscrepancy AnaLYZer for ERlang programs <http://www.it.uu.se/research/group/hipe/dialyzer/>`_ , `TYPER: A Type Annotator of Erlang Code <http://user.it.uu.se/~tobiasl/publications/typer.pdf>`_ ,  `Pratical type inference based on success typings <http://www.it.uu.se/research/group/hipe/dialyzer/publications/succ_types.pdf>`_ , `Gradual Typing of Erlang programs: A Wrangler Experience <http://www.it.uu.se/research/group/hipe/dialyzer/publications/wrangler.pdf>`_


