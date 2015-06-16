====================
如何实现Prolog解释器
====================

:date: 2014-03-23
:slug: how-to-write-a-prolog-interpreter


Prolog语言本身就不太容易理解。要写个Prolog解释器就更不容易了。还好有 `Warren's Abstract Machine: A Tutorial Reconstruction <http://wambook.sourceforge.net/>`_ 。

.. more

WAMBOOK里把实现Prolog的过程分成L0、L1、L2、L3四个阶段。也就是把一个困难的问题，分解成了四个比较容易的问题。这样只看slides，也是能自己写出来的，未必需要先把WAMBOOK完整看一遍。

WAMBOOK有一个不好的地方是，它是按C的思路来讲的。C语言和Prolog语言的语义相差比较大，用C语言实现Prolog解释器会比较繁琐。而用Erlang就比较容易了。假如你不是很确定你是否理解了unification，不妨看看 `miniKanren的论文 <http://gradworks.umi.com/33/80/3380156.html>`_ 。Unification以外的部分就不推荐了，毕竟现在说的是如何实现Prolog解释器，而且都是用很费解的宏写的。
