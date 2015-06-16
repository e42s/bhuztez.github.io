=============
LISP中的Macro
=============

:date: 2015-01-20
:slug: macro-in-lisp


Paul Graham 在 The Roots of Lisp 一文中把 John McCarthy 的论文复述了一遍，还画蛇添足引入了 defun ，结果文中的解释器其实并不能自举。需要引入Macro之后才可以，讽刺的是，Paul Graham 整天吹嘘 Macro 多么强大，在这里却忘记了。

.. more

得像下面这样用 macro 来定义 defun 。

.. code::

   (label defun
     (macro (n p e)
       (cons (quote label)
       (cons n
       (cons (cons (quote lambda)
             (cons p
             (cons e
                   (quote ())
             )))
             (quote ())
       )))
     )
   )


比如定义 caar 为

.. code::

   (defun caar (x) (car (car x)))


宏展开后得到

.. code::

   (label caar (lambda (x) (car (car x))))
