中国剩余定理
============

:date: 2014-08-03
:slug: chinese-remainder-theorem

本文纯属搞笑，切勿当真

中国剩余定理这个叫法是对这种方法的极大误解。根据中国人只追求实用的天赋，肯定不会没事去证明某种数学性质的。要是给不出解法，就算证明了一个很重要的性质，一句这有啥用就噎死了。中国剩余定理实际上是为了解一种同余方程组。中国剩余定理很可能不是中国人最早证明的，完整的解法也很可能不是中国人最早给出的，只是因为孙子算经中对这种同余方程组给出了不完整的解法，这就叫中国剩余定理了，和费马大定理有异曲同工之妙。

.. more

求正整数 :math:`x` 使得

.. math::

    \left\{\begin{array}{l l}
    x \equiv a_1 & (mod\ m_1) \\
    x \equiv a_2 & (mod\ m_2) \\
    \ldots \\
    x \equiv a_n & (mod\ m_n)
    \end{array}\right.


找出任意一个满足这个同余方程组的 :math:`x` 后，根据中国剩余定理即可得到最小的 :math:`x` 。

用构造法，求 :math:`b_i, i \in \{1, 2, \ldots, n\}` 使得

.. math::

    \forall ( j \in \{1, 2, \ldots, n\}, j \ne i) m_j \mid b_i

记 :math:`b_i` 和 :math:`m_i` 的最大公约数为 :math:`gcd(b_i, m_i)` 。若有

.. math::

    gcd(b_i, m_i) \mid a_i

且存在 :math:`k_i, i \in \{1, 2, \ldots, n\}` 满足

.. math::

     k_i b_i \equiv gcd(b_i, m_i) (mod\ m_i) i \in \{1, 2, \ldots, n\} 

不妨设

.. math::

    x = \sum_{i=1}^{n} \frac{a_i}{gcd(b_i, m_i)} k_i b_i

对于任意 :math:`j` ，满足 :math:`j \in \{1, 2, \ldots, n\}` ，有

.. math::

    \forall ( i \in \{1, 2, \ldots, n\}, i \ne j) m_j \mid b_i

可得

.. math::

    m_j \mid \sum_{i \ne j} \frac{a_i}{gcd(b_i, m_i)} k_i b_i


所以

.. math::

    \begin{array}{lll}
    \sum_{i=1}^{n} \frac{a_i}{gcd(b_i, m_i)} k_i b_i & \equiv \frac{a_j}{gcd(b_j, m_j)} k_j b_j  & (mod\ m_j) \\
    & \equiv \frac{a_j}{gcd(b_j, m_j)} gcd(b_j, m_j) & (mod\ m_j) \\
    & \equiv a_j & (mod\ m_j)
    \end{array}


:math:`bi` 可以直接取 :math:`\prod_{j \ne i} m_j` ，求 :math:`k_i` 却比较困难。

因为

.. math::

    k_i b_i\ mod\ m_i \equiv gcd(b_i, m_i) \cdot \left(k_i \frac{b_i}{gcd(b_i,m_i)}\ mod\ \frac{m_i}{gcd(b_i,m_i)}\right)


所以， :math:`k_i` 满足

.. math::

    k_i \frac{b_i}{gcd(b_i,m_i)} \equiv 1 \left(mod\ \frac{m_i}{gcd(b_i, m_i)}\right)


这个问题也可以表示成，已知 :math:`a, m` ，且 :math:`gcd(a,m) = 1` ，求 :math:`k` 使得

.. math::

    ka \equiv 1 (mod\ m)


欧拉定理
--------

有一种解法，不知道从哪里流传出来的，利用了欧拉定理。

欧拉定理指出，若 :math:`gcd(a, m) = 1` ，有

.. math::

     a^{\varphi(m)} \equiv 1 (mod\ m) 

所以， :math:`k` 取 :math:`a^{\varphi(m)-1}` 即可。

因为除了量子计算机，我们并没有有效的办法能计算出 :math:`\varphi(m)`，至少古人不能使用这种方法。


大衍求一术
----------

中国古代有一种求解的方法，叫做大衍求一术。很多介绍中国剩余定理的文章都没有提到大衍求一术。而提到大衍求一术的很多都只讲了什么是大衍求一术，而没有解释为什么。而大衍求一术乍一看完全不知道这是在算什么。

数书九章中记载的大衍求一术是这样的。按如下放置四个数，不断作以下变换，直到 :math:`r1` 或 :math:`r2` 为1为止。

.. math::

    \left(\begin{matrix}
    k_1 & r_1 \\
    k_2 & r_2
    \end{matrix}\right) \to \left\{\begin{array}{ll}
    \left(\begin{matrix}
    k_1 & r_1 \\
    k_2+k_1 \left\lfloor\frac{r_2}{r_1}\right\rfloor & r_2\ mod\ r_1
    \end{matrix}\right) & , r_1 < r_2 \\
    \left(\begin{matrix}
    k_1 + k_2 \left\lfloor\frac{r_1}{r_2}\right\rfloor & r_1\ mod\ r_2 \\
    k_2 & r_2
    \end{matrix}\right) & , r_1 > r_2
    \end{array}\right.


一开始四个数是

.. math::

    \left(\begin{matrix}
    1 & a \\
    0 & m
    \end{matrix}\right)


很难看出，在变换过程中，这四个位置上的数始终满足

.. math::

    \left\{\begin{array}{ll}
    k_1 a \equiv r_1 & (mod\ m) \\
    k_2 a \equiv -r_2 & (mod\ m)
    \end{array}\right.

一开始

.. math::

   \left\{\begin{array}{ll}
   1 \cdot a \equiv a & (mod\ m) \\
   0 \cdot a \equiv 0 \equiv -m & (mod\ m)
   \end{array}\right.


当 :math:`r_1 < r_2` 时，

.. math::

    \begin{array}{lll}
    \left(k_2 + k_1 \left\lfloor\frac{r_2}{r_1}\right\rfloor\right) \cdot a & \equiv - r_2 + r_1 \left\lfloor \frac{r_2}{r_1}\right\rfloor & (mod\ m) \\
    & \equiv - r_2 + r_2 - r_2\ mod\ r_1 & (mod\ m) \\
    & \equiv - r_2\ mod\ r_1 & (mod\ m)
    \end{array}


当 :math:`r_1 > r_2` 时，

.. math::
 
    \begin{array}{lll}
    \left(k_1 + k_2 \left\lfloor\frac{r_1}{r_2}\right\rfloor\right) \cdot a & \equiv r_1 - r_2 \left\lfloor\frac{r_1}{r_2}\right\rfloor & (mod\ m) \\
    & \equiv r_1 - r_1 + r_1\ mod\ r_2 & (mod\ m) \\
    & \equiv r_1\ mod\ r_2 & (mod\ m)
    \end{array}


所以，这两个等式在变换过程中始终成立。

最终，若 :math:`r_1 = 1`

.. math::

    k_1 a \equiv 1 (mod\ m)

若 :math:`r_2 = 1` ，作以下变换

.. math::

    \left(\begin{matrix}
    k_1 & r_1 \\
    k_2 & 1
    \end{matrix}\right) \to \left(\begin{matrix}
    k_1 + k_2 (r_1 - 1) & 1 \\
    k_2 & 1
    \end{matrix}\right)


此时，

.. math::

    \begin{array}{lll}
    (k_1 + k_2 (r_1 - 1)) \cdot a & \equiv r_1 - (r_1 - 1) & (mod\ m) \\
    & \equiv 1 & (mod\ m)
    \end{array}

和西方的扩展欧几里德算法相比，循环不变式差一个负号，在最后一步需要分两种情况讨论。数书九章并没有交代大衍求一术是怎么来的，可能一开始就是这样的，也可能是流传过程中减号误传成了加号，现在已无从考证了。


扩展欧几里德算法
----------------

现在用扩展欧几里德算法来求解。把循环不变式换成

.. math:: 

    \left\{\begin{array}{ll}
    k_1 a \equiv r_1 & (mod\ m) \\
    k_2 a \equiv r_2 & (mod\ m)
    \end{array}\right.

变换过程换成

.. math::

    \left(\begin{matrix}
    k_1 & r_1 \\
    k_2 & r_2
    \end{matrix}\right) \to \left(\begin{matrix}
    k_2 - k_1\left\lfloor\frac{r_2}{r_1}\right\rfloor & r_2\ mod\ r_1 \\
    k_1 & r_1
    \end{matrix}\right)

而初始值不变，仍然是

.. math::

    \left(\begin{matrix}
    1 & a \\
    0 & m
    \end{matrix}\right)

一开始

.. math::

   \left\{\begin{array}{ll}
   1 \cdot a \equiv a & (mod\ m) \\
   0 \cdot a \equiv 0 \equiv m & (mod\ m)
   \end{array}\right.

变换过程中

.. math::

    \begin{array}{lll}
    \left(k_2 - k_1 \left\lfloor\frac{r_2}{r_1}\right\rfloor\right) \cdot a & \equiv r_2 - r_1 \left\lfloor \frac{r_2}{r_1}\right\rfloor & (mod\ m) \\
    & \equiv r_2 - (r_2 - r_2\ mod\ r_1) & (mod\ m) \\
    & \equiv r_2\ mod\ r_1 & (mod\ m)
    \end{array}

所以，这两个等式在变换过程中始终成立。

最终，若 :math:`r_1=1`

.. math::

    k_1 a \equiv 1 (mod\ m)


辗转相除法
----------

辗转相除法是一种求最大公约数的方法。西方所谓的欧几里德算法就是辗转相除法。而扩展欧几里德算法其实就是同一种算法，只不过得到了更多结果。

已知 :math:`a,b` ，求 :math:`gcd(a,b)` 。

按如下放置两个数，不断作以下变换，直到 :math:`r1` 为0

.. math::

    \left(\begin{matrix}
    r_1 \\
    r_2
    \end{matrix}\right) \to \left(\begin{matrix}
    r_2\ mod\ r_1 \\
    r_1
    \end{matrix}\right)

一开始两个数是

.. math::

    \left(\begin{matrix}
    a \\
    b
    \end{matrix}\right)


不妨设 :math:`r_1 = s_1 \cdot gcd(r_1, r_2),  r_2 = s_2 \cdot gcd(r1, r2)` ，则

.. math::

     \begin{array}{ll}
     r2\ mod\ r1 &= (s_2 \cdot gcd(r_1, r_2))\ mod\ (s_1 \cdot gcd(r_1, r_2)) \\
                 &= (s_2\ mod\ s_1) \cdot gcd(r_1, r_2) 
     \end{array}


因为 :math:`gcd(s_2\ mod\ s_1, s_1) = 1` ，所以

.. math::

    gcd(r_2\ mod\ r_1, r_1) = gcd(r_1, r_2)


因此， :math:`gcd(r1, r2)` 始终是 :math:`gcd(a, b)`

当 :math:`s_1=1` 时， :math:`s_2\ mod\ s_1 = 0` ，计算结束，得到了 :math:`gcd(a, b)`

如下图所示，辗转相除法从后往前看，有 :math:`r_1 = gcd(a, b) = gcd(r_n, r_{n+1})`

.. math::

    \left(\begin{matrix}
    a \\
    b
    \end{matrix}\right) \to \ldots \to \left(\begin{matrix}
    r_4 \\
    r_5
    \end{matrix}\right) \to \left(\begin{matrix}
    r_3 \\
    r_4    
    \end{matrix}\right) \to \left(\begin{matrix}
    r_2 \\
    r_3    
    \end{matrix}\right) \to \left(\begin{matrix}
    r_1 \\
    r_2
    \end{matrix}\right) \to \left(\begin{matrix}
    0 \\
    r_1
    \end{matrix}\right)


求解 :math:`k_1` ，使得 :math:`k_1 r_1 \equiv gcd(r_1, r_2) (mod\ r_2)`

因为 :math:`r_1 = gcd(r_1, r_2)` 所以 :math:`k_1 = 1`

求解 :math:`k_2` ，使得 :math:`k_2 r_2 \equiv gcd(r_2, r_3) (mod\ r_3)`

不妨设 :math:`r_3 - q_2 r_2 = r_1`

因为 :math:`r_1 = gcd(r_2, r_3)`

可得 :math:`r_3 - q_2 r_2 = gcd(r_2, r_3)`

所以 :math:`k_2 = -q_2`

求解 :math:`k_3` ，使得 :math:`k_3 r_3 \equiv gcd(r_3, r_4) (mod\ r_3)`

不妨设 :math:`r_4 - q_3 r_3 = r_2`

因为 :math:`r_3 - q_2 r_2 = gcd(r_3, r_4)`

可得 :math:`r_3 - q_2(r_4 - q_3 r_3) = gcd(r_3, r_4)`

即 :math:`r_3(1 + q_2 q_3) - q_2 r_4 = gcd(r_3, r_4)`

所以 :math:`k_3 = 1 + q_2 q_3`

不难看出，假设存在 :math:`k_{n+1} r_{n+1} + k_n r_{n+2} = gcd(r_{n+2}, r_{n+3})`

不妨设 :math:`r_{n+3} - q_{n+2} r_{n+2} = r_{n+1}`

可得 :math:`k_{n+1}(r_{n+3} - q_{n+2} r_{n+2}) + k_n r_{n+2} = gcd(r_{n+2}, r_{n+3})`

即 :math:`(k_n - k_{n+1} q_{n+2}) r_{n+2} + k_{n+1} r_{n+3} = gcd(r_{n+2}, r_{n+3})`

所以 :math:`k_{n+2} = k_n - k_{n+1} q_{n+2}`

即

.. math::

    \left[\begin{matrix}
    k_{n+2} \\
    k_{n+1}
    \end{matrix}\right] = \left[\begin{matrix}
    -q_{n+2} & 1 \\
    1 & 0
    \end{matrix}\right] \cdot \left[\begin{matrix}
    k_{n+1} \\
    k_n
    \end{matrix}\right]

逐项展开后

.. math::

    \left[\begin{matrix}
    k_{n+2} \\
    k_{n+1}
    \end{matrix}\right] = \left[\begin{matrix}
    -q_{n+2} & 1 \\
    1 & 0
    \end{matrix}\right] \cdot \ldots \cdot \left[\begin{matrix}
    -q_3 & 1 \\
    1 & 0
    \end{matrix}\right] \cdot \left[\begin{matrix}
    -q_2 & 1 \\
    1 & 0
    \end{matrix}\right] \cdot \left[\begin{matrix}
    1 \\
    0
    \end{matrix}\right]

且有

.. math::

    \left[\begin{matrix}
    r_{n+2} & r_{n+3}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    k_{n+2} \\
    k_{n+1}
    \end{matrix}\right] = gcd(r_{n+2}, r_{n+3})

观察

.. math::

    \left[\begin{matrix}
    c_3 & c_1 \\
    c_4 & c_2
    \end{matrix}\right] \cdot \left[\begin{matrix}
    -q & 1 \\
    1 & 0
    \end{matrix}\right] = \left[\begin{matrix}
    -q c_3 + c_1 & c_3 \\
    -q c_4 + c_2 & c_4
    \end{matrix}\right]

矩阵乘法符合结合率，不妨设

.. math::

    \left[\begin{matrix}
    r_{n+2} & r_{n+3}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    s_{m+1} & s_{m+2} \\
    t_{m+1} & t_{m+2}
    \end{matrix}\right] = \left[\begin{matrix}
    r_m & r_{m+1}
    \end{matrix}\right]

在辗转相除法的每一步

.. math::

    \left[\begin{matrix}
    r_{m+2} & r_{m+3}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    -q_{m+2} & 1 \\
    1 & 0
    \end{matrix}\right] = \left[\begin{matrix}
    r_{m+1} & r_{m+2}
    \end{matrix}\right]

同时计算

.. math::

    \left[\begin{matrix}
    s_{m+3} & s_{m+4}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    -q_{m+2} & 1 \\
    1 & 0
    \end{matrix}\right] = \left[\begin{matrix}
    s_{m+2} & s_{m+3}
    \end{matrix}\right]

可以合并成

.. math::

    \left[\begin{matrix}
    s_{m+3} & s_{m+4} \\
    r_{m+2} & r_{m+3}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    -q_{m+2} & 1 \\
    1 & 0
    \end{matrix}\right] = \left[\begin{matrix}
    s_{m+2} & s_{m+3} \\
    r_{m+1} & r_{m+2}
    \end{matrix}\right]

补一个单位矩阵，也就是

.. math::

    \left[\begin{matrix}
    r_{n+2} & r_{n+3}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    1 & 0 \\
    0 & 1
    \end{matrix}\right] = \left[\begin{matrix}
    r_{n+2} & r_{n+3}
    \end{matrix}\right]


得到初值

.. math::

    \left[\begin{matrix}
    1 & 0 \\
    r_{n+2} & r_{n+3}
    \end{matrix}\right]


连起来

.. math::

    \left[\begin{matrix}
    1 & 0 \\
    r_{n+2} & r_{n+3}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    -q_{n+2} & 1 \\
    1 & 0
    \end{matrix}\right] \cdot \ldots \cdot \left[\begin{matrix}
    -q_1 & 1 \\
    1 & 0
    \end{matrix}\right] = \left[\begin{matrix}
    s_1 & s_2 \\
    0 & r_1
    \end{matrix}\right]

所以 :math:`s_2` 就是结果

更合理的思路是，把辗转相除法写成矩阵形式后，观察到


.. math::

    \left[\begin{matrix}
    r_{n+2} & r_{n+3}
    \end{matrix}\right] \cdot \left[\begin{matrix}
    s_1 & s_2 \\
    t_1 & t_2
    \end{matrix}\right] = \left[\begin{matrix}
    0 & r_1
    \end{matrix}\right]


发现 :math:`r_{n+2} s_2 \equiv r_1 \equiv gcd(r_{n+2}, r_{n+3}) (mod\ r_{n+3})`

且有循环不变式 :math:`r_{n+2} s_{m+2} \equiv r_{m+1} (mod\ r_{n+3})`

这样就得到了扩展欧几里德算法
