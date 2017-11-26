=========
Paxos简介
=========

:date: 2017-09-21
:slug: paxos
:tags: Paxos

Paxos Made Simple(以下缩写PMS)里分成proposer, acceptor, learner三种角色，也就是假设了有leader。leader是非常复杂的概念。而learner, leader的存在，只是针对某些情形的优化。要想收到所有决议，是离不开proposer的。

    If a learner needs to know whether a value has been chosen, it can have a proposer issue a proposal, using the algorithm described above.

.. more

没了leader，learner毫无存在的必要。因为每个instance，所有proposer都得参与，proposer自己就知道决议了，不需要额外的learner。

Synod算法
=========

synod算法中有两种角色，proposer和acceptor。两者数量不必是1:1的。一项议案可以进行很多轮(在下面把轮次记作proposal number)投票。每一轮投票，proposer都可以提出proposal(我们把proposal的内容称为value)。

synod算法可以保证：

* 对于同一个proposal number，所有的acceptor都只会accept相同的value
* 一项议案，在proposal number为N时，形成了决议，proposal number大于N的所有proposal的value都和决议的value相同。也就是一旦形成决议，value就不再会改变。

对于proposer来说，每一轮投票要分两个阶段。

===== ======== ======== ========================
phase proposer acceptor
===== ======== ======== ========================
1     prepare  promise
2     propose  accept   (PMS里是accept/accepted)
===== ======== ======== ========================

定义proposer和acceptor之间的消息格式

.. code:: erlang

    -type promised() :: {proposal_number(), proposer()}.
    -type accepted() :: {proposal_number(), proposer(), value()}.

    -type request() :: {prepare, promised()}
                     | {propose, accepted()}.

    -type reply() :: ok
                   | {ok, promised()}
                %% | {ok, accepted()}
                   | {ok, promised(), accepted()}.

尽管PMS里没有要求，这里额外规定，acceptor在收到来自proposer的请求时，无论是否处理这个请求，都要告诉proposer，当前，promise过的proposal number最高的prepare请求，以及accept过的proposal number最高的propose请求，的内容分别是什么。

Prepare阶段
-----------

一个proposer在发出propose之前，必须收到来自过半acceptor的promise。而一轮投票，一个acceptor最多只会promise一个proposer。根据抽屉原理，一轮投票，最多只有一个proposer能发出propose。这样就保证了第一点。

举个例子，一个proposer p想得到第3轮投票的propose机会，先向acceptor发送请求\ :code:`{prepare, {3,p}}`\ ，假设五个acceptor a,b,c,d,e返回的promised分别是

============= ============= ============= ============= ============= ============
a             b             c             d             e             可以propose?
============= ============= ============= ============= ============= ============
:code:`{3,p}` :code:`{3,p}` :code:`{3,p}` :code:`{4,q}` :code:`{5,r}` Y
:code:`{3,q}` :code:`{3,q}` :code:`{3,r}` :code:`{3,r}` :code:`{3,p}` N
============= ============= ============= ============= ============= ============

消息格式里，一个值得注意的细节是，有一行被注释掉了。一轮投票里，一个acceptor只收到过propose请求，但是从没有收到过prepare请求的情况是存在的。比如

========  = = = = =
acceptor  a b c d e
promised  x x x
accepted      x x x
========  = = = = =

因为收到propose请求就表明，该轮能发propose请求的proposer已经决出了。所以一个acceptor假装已经收到过来自同一个proposer的prepare请求是不会导致错误的。

Propose阶段
-----------

一个proposer是不可以随心所欲的propose任意value的。假如收到的reply里，有accept过的propose请求，那么就只能propose，proposal number最高的那个的value。举个例子，一个proposer p想propose的是\ :code:`{3,p,rock}`\ ，然而在发出propose请求前，五个acceptor a,b,c,d,e返回的accepted分别是


=================== ====================== ============ = = =======================
a                   b                      c            d e 应该propose的value
=================== ====================== ============ = = =======================
:code:`{1,q,paper}` :code:`{2,r,scissors}` :code:`none`     :code:`{3,p,scissors}`
:code:`none`        :code:`none`           :code:`none`     :code:`{3,p,rock}`
=================== ====================== ============ = = =======================

而一个acceptor在promise proposal number为N的prepare请求后，就不再处理proposal number小于N的所有请求。一个proposer，只有在一轮投票中收到来自过半的acceptor的accept之后，才能认为自己知道了这项议案的决议内容。举个例子，比如proposer p要能收到过半的accept，那么其向acceptor c发送的propose请求，必须先于q的prepare请求被c处理。

============ = = = = =
acceptor     a b c d e
============ = = = = =
p:3:propose  x x x
q:4:prepare      x x x
============ = = = = =

于是同样根据抽屉原理，下一个能propose的proposer，必然会propose相同的value。

= = = = = =
n a b c d e
= = = = = =
1 x x x
2   x
3       x
4   x x   x
= = = = = =

因为propose的是相同的value，所以无论是否能过半，后面的proposer在能propose时，看到的被accept的proposal number最高的propose请求的value都仍然是这个value。这样就保证了第二点。

退避
====

synod算法，按最naive的方式实现，在现实中往往会变成这样。

= = = = = =
n a b c d e
= = = = = =
1 p p q r s
2 r t s q q
3 s p r q r
= = = = = =

不断的重复开始prepare，没有一个proposer有机会propose。为什么？因为synod算法，并不保证一定会形成决议啊。

一种常见应对方法是，没抢到propose机会，proposer应该过一段时间再去抢下一轮。假如连续几轮没抢到，这个时间间隔应该是越来越大的。假如运气不好，一项议案要花比别的多的多的时间才能形成决议。

一种更简单的方法是，没抢到propose机会，proposal number加一个随机数，而proposer假如看到有acceptor promise了别的proposer的prepare请求，应该协助当前看到的proposal number最高的prepare请求的proposer，代其向acceptor发prepare请求。这也就是为什么这里\ :code:`promised()`\ 里有第二个元素\ :code:`proposer()`\ 。

这种方法有个致命的缺陷就是，假如抢到propose机会的proposer，并没有value需要propose，就只好卡在那里了。所以，我们修改请求格式，假如一个proposer没啥需要propose的，那就先peek，而不是prepare。

.. code:: erlang

    -type request() :: peek
                     | {prepare, promised()}
                     | {propose, accepted()}.

这样，假如别的proposer抢到propose机会，半天没动静，那只可能是那个proposer出问题了，那赶紧重新抢吧。


多副本状态机
============

单个状态机，收到命令之后，执行命令，变成下一个状态。而多副本的状态机，需要先把命令写入日志，之后在各个状态机副本里，执行日志里记录的命令。

.. code::

        C1       C2       C3
    S0 ----> S1 ----> S2 ----> S3

借助Synod算法同步状态机的日志。日志里每一条记录，对应一项议案。一个proposer和一个acceptor组成一个节点。proposer从日志的第一条记录开始，逐条读取对应的议案的决议。没有命令需要写入日志就peek，有就prepare。假如当前议案的决议是别的proposer提交的命令，那么要在下一项议案里重试。

因为一项议案只能一个决议。而节点却有很多，所以通常会把多条命令合并到一条状态机日志里。


成员变更
========

这也可以看成是一个状态机。状态是一个集合。初始状态是所有bootstrap节点。命令是加入一个节点和删除一个节点。因为proposer和acceptor数量不必是1:1的。新节点加入时，完全可以用自己的proposer来propose加入的命令。只是在propose之前，必须获取从第一条日志开始的所有日志，并重放，且向同节点的acceptor发相应的propose请求。加入节点的命令写入后，新的节点里的acceptor就正式加入了。删除节点则可以由任意一个proposer来发起。

快照
====

因为节点个数是动态变化的，尽管不频繁。可是总有一天，过半bootstrap节点会退出。此时，假如还是要求从第一条日志开始重放，新的节点就再也加不进去了。所以，状态机必须定时生成snapshot，并告诉Paxos节点，这个snapshot是在执行第N条日志之前生成的。成员状态机的状态应该改成，节点到N的映射。所有节点当前最小的N之前日志都是可以切掉的。
