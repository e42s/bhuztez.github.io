==========
概率论基础
==========

:date: 2015-06-09
:slug: probability-theory


在大数据，机器学习大行其道的今天，很多人却避而不谈概率，甚至会有人认为概率不重要。即便是很多提到概率的，也不能把概率讲清楚。要理解概率还是得看E.T. Jayne的\ `Probability Theory: the Logic of Science <http://omega.albany.edu:8008/JaynesBook.html>`_\ 和A.N. Kolmogorov的\ `Foundations of the Theory of Probability <http://www.kolmogorov.com/Foundations.html>`_\ 。

.. more


概率论的形式化早已经完成。到现在还讲不清楚，真的很奇怪了。可现实偏偏是这样的。概率论不见的有多难啊，怎么也比SVM那些fancy的技巧容易多了。先列出符合直觉的事件运算必须满足的性质，给每个事件指定个概率，找到能同时满足这些条件的理论，就是概率公理了。有了概率公理，就可以根据定义得出条件概率的计算公式，进而可以得到Bayes公式。而根据Wallis Derivation可以得到最大熵原理，加上各种约束条件就能解出各种不同的分布了。还有Hammersley-Clifford定理告诉我们，Markov性质和Gibbs Measure的意义是一样的。
