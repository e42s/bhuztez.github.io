========
Metamath
========

:date: 2014-11-17
:slug: metamath
:status: draft

Metamath_\ 是一个很独特的证明检查程序。Metamath语义非常简单，完全可以自己实现一遍。而且更加专注于证明本身，并不需要打补丁以便更好的支持新的理论。比如Unimath为了更好的支持Homotopy Type Theory就对Coq打了补丁。这一点很重要，要是我们不能检查证明检查程序本身正确与否，我们写的证明即使通过了检查，也不能说明证明没问题。而一个证明检查程序本身太复杂，超过了人力能检查的极限，那么出现重大缺陷就几乎不可避免了，比如Coq的\ Falso_\ 。很不幸的是，Metamath风格的证明检查工具一直没有流行起来。

.. _Metamath: http://metamath.org/
.. _Falso: http://inutile.club/estatis/falso/

.. more

Metamath特别简单，主要是因为两点，一是没有内置任何Type Theory，二是没有作用域的概念。大部分所谓的数学书里，根本就不定义数学符号的作用域规则，free variable的作用域根本就是错的。比如\ :math:`\forall x~\varphi`, where :math:`x` is not free in :math:`\varphi`\ ，问题在于where后面这句话在\ :math:`\forall x`\ 的作用域外面，那里的\ :math:`x`\ 一定没法指的是作用域里面的那个。所以有了作用域之后，为了能表达free variable的概念，不可避免要引入特殊的语句。Metamath里没有作用域，这意味着你必须给原本不同作用域中的变量取不同的名字，但是这避免了引入特殊的语句。

Metamath也有做的比较糟糕的地方。现在Metamath把所有内容都写同一个文件里，实际上这是没有必要的，也对别人的参与产生了一点小麻烦，毕竟只有一个文件，那必须等都很合理了才会放进去，而不是可以先在一个不同的文件里放一个实验性质的证明。这也妨碍了用其他程序来生成证明，毕竟不可能有通用的proof assistant，对于所有理论的证明都能提供足够的帮助，根据不同情况用SMT Solver，计算机代数软件什么的来生成证明是很必要的。
