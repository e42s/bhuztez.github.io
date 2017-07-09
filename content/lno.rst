=========================
用CSS Counter Style画行号
=========================

:date: 2016-12-14
:slug: line-number
:tags: CSS

现在可以找到很多网页版代码编辑器以及在网页上显示高亮代码的工具，他们显示行号的功能都非常复杂。

.. more

行号这么简单，用\ `CSS Counter Style`__\ 就可以了。

.. __: https://developer.mozilla.org/en-US/docs/Web/CSS/@counter-style

.. code:: css

    @counter-style lno {
        system: extends decimal;
        pad: 4 " ";
    }

    pre {
        margin: 0 0 0 5ch;
        counter-reset: line;
        width: 4ch;
        white-space: pre-wrap;
        word-break: break-all;
        outline: 1px solid red;
        border-left: 1px solid blue;
        background-color: #EEE;
        padding: 0 1ch;
    }

    pre span.line {
        counter-increment: line;
        box-decoration-break: clone;
    }

    pre span.line::before {
        content: counter(line, lno);
        margin: 0 2ch 0 -6ch;
    }


.. code:: html

    <pre>
    <span class="line">aa aaa aaa</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    <span class="line">a</span>
    </pre>
