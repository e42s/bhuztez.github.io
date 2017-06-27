========
阴阳谜题
========

:date: 2015-01-21
:slug: yinyang-puzzle


阴阳谜题是个很简单的问题，不过是揭示了call/cc is poor man's goto。可是总是有人觉得能搞明白阴阳谜题是一件很值得夸耀的事。

.. more

阴阳谜题可以写成下面这样，无非这里每次 cc() 都会产生一个平行宇宙。

.. code::

    yin = cc()
    echo '@'
    yang = cc()
    echo '*'
    yin(yang)


pi-calculus足够用来表达call/cc的语义，可以把以下代码放到\ `这里 <http://bhuztez.github.io/pi-diagram/>`_\ 观察运行过程。

.. code::

    proc yin_cc(O,A,B) {
        new Yin in {
            yin(O,A,B,Yin) | send Yin to Yin
        }
    }

    proc yin(O,A,B,YinCC) {
        recv Yin from YinCC;
        send A to O;
        { yin(O,A,B,YinCC) | yang_cc(O,A,B,Yin) }
    }

    proc yang_cc(O,A,B,Yin) {
        new Yang in {
           yang(O,A,B,Yin,Yang) | send Yang to Yang
        }
    }

    proc yang(O,A,B,Yin,YangCC) {
        recv Yang from YangCC;
        send B to O;
        { yang(O,A,B,Yin,YangCC) | send Yang to Yin }
    }

    proc output(O) {
        recv X from O;
        output(O)
    }

    proc main() {
        new O, A, B in {
           output(O) | yin_cc(O,A,B)
       }
    }


当然也可以看下面

.. code::

                      1     2
    - = cc() | -=1 | -=? | -=1 |
    echo '@'    @
    + = cc() | +=2 |     | +=? |
    echo '*'    *                 3
    -(+)     |     | -=2 |     | -=2 |
                      @
                   | +=3 |     | +=? |
                      *
                         | +=3 |
                            *           4
                   | -=3 |           | -=3 |
                      @
                   | +=4 |           | +=? |
                      *
                               | +=4 |
                                  *
                         | +=4 |
                            *
