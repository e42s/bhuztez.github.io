==========
工作流原理
==========

:date: 2015-02-26
:slug: workflow-and-pi-calculus
:status: draft

工作流是一个很简单的概念。自己实现工作流引擎的也不在少数，甚至有一些很奇怪的号称支持中国特色流程的。可是很多就算看了文档和代码，也很难理解为啥这可以工作，特别是他是怎么保证某个任务确实会执行。这方面就缺一个简单易懂的文章列表。

.. more

`Workflow Patterns <http://www.workflowpatterns.com/>`_\ 这个网站倒是给了很多例子，适合用来检验功能是否足够。可是这上面的例子采用的模型是coloured petri-net，虽然例子很简单，光看图示和文字还是很费解的。看IBM developerWorks上的一系列文章，有助于更好的区分几个类似的pattern之间的区别 (差别很大啊，可是看Workflow Patterns很容易就绕进去了)

`Implementing advanced workflow patterns in WebSphere Integration Developer and WebSphere Process Server, Part 1: Basic control flow patterns and cancellation and force completion patterns <http://www.ibm.com/developerworks/webservices/library/ws-impavdworkflowpart1/index.html>`_

`Implementing Advanced Workflow Patterns in WebSphere Integration Developer and WebSphere Process Server, Part 2: Multiple instance patterns and iteration patterns <http://www.ibm.com/developerworks/webservices/library/ws-impavdworkflowpart2/index.html>`_

`Implementing Advanced Workflow Patterns in WebSphere Integration Developer and WebSphere Process Server, Part 3: Advanced branching and synchronization patterns <http://www.ibm.com/developerworks/webservices/library/ws-impavdworkflowpart3/index.html>`_

`Implementing Advanced Workflow Patterns in WebSphere Integration Developer and WebSphere Process Server, Part 4: State-based, termination and trigger patterns <http://www.ibm.com/developerworks/webservices/library/ws-impavdworkflowpart4/index.html>`_

一种常用的也是更容易理解的用来表示工作流的模型是pi-calculus。pi-calculus可以看\ http://www.erlang.se/workshop/2005/noll_roy.pdf\ 这个。至于想不到怎么用pi-calculus表示工作流，可以参考\ http://bpt.hpi.uni-potsdam.de/pub/Public/FrankPuhlmann/diss.pdf\ 和\ http://www.stefansen.dk/papers/smawl.pdf
