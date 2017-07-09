==============
二叉树同构判断
==============

:date: 2017-02-14
:slug: binary-tree-isomorphism
:tags: Binary Tree

知乎上有人问二叉树如何判断同构\ [#]_\ ，这是一个非常简单的问题，下面有些回答却在瞎扯hash。

.. [#] https://www.zhihu.com/question/55484468

.. more

因为这个题显然不考虑并行，使用最简单的办法就足够了。给树编号，只要保证同构的树总是得到相同的编号就可以了。


.. code:: erlang

    -module(isomorphism).


    -export([test/0]).


    number_of_tree(leaf, Numbers) ->
        {0, Numbers};
    number_of_tree({tree, E, L, R}, Numbers) ->
        {N1, Numbers1} = number_of_tree(L, Numbers),
        {N2, {Next, D}} = number_of_tree(R, Numbers1),

        Key = {E, max(N1,N2), min(N1,N2)},

        case dict:find(Key, D) of
            error ->
                {Next, {Next+1, dict:store(Key, Next, D)}};
            {ok, Value} ->
                {Value, {Next, D}}
        end.


    is_isomorphic(X, Y) ->
        {NX, Numbers} = number_of_tree(X, {1, dict:new()}),
        {NY, _} = number_of_tree(Y, Numbers),
        NX == NY.


    test() ->
        true =
            is_isomorphic(
              {tree, a,
               {tree, b,
                {tree, d, leaf, leaf},
                {tree, e, {tree, f, leaf, leaf}, leaf}},
               {tree, c,
                {tree, g, {tree, h, leaf, leaf}, leaf}, leaf}
              },

              {tree, a,
               {tree, c, {tree, g, leaf, {tree, h, leaf, leaf}}, leaf},
               {tree, b, {tree, e, {tree, f, leaf, leaf}, leaf},
                {tree, d, leaf, leaf}}
              }
             ),

        false =
            is_isomorphic(
              {tree, a,
               {tree, b,
                {tree, d, leaf, leaf},
                {tree, e, {tree, f, leaf, leaf}, leaf}
               },
               {tree, c, {tree, g, {tree, h, leaf, leaf}, leaf}, leaf}
              },
              {tree, a,
               {tree, b, {tree, g, leaf, {tree, h, leaf, leaf}}, leaf},
               {tree, c, {tree, d, {tree, f, leaf, leaf}, leaf}, {tree, e, leaf, leaf}}
              }
             ),

        true =
            is_isomorphic(
              {tree, a,
               {tree, b, {tree, d, leaf, leaf}, {tree, e, {tree, f, leaf, leaf}, leaf}},
               {tree, c, {tree, g, {tree, h, leaf, leaf}, leaf}, leaf}
              },
              {tree, a,
               {tree, c, {tree, g, leaf, {tree, h, leaf, leaf}}, leaf},
               {tree, b, {tree, e, {tree, f, leaf, leaf}, leaf}, {tree, d, leaf, leaf}}
              }
             ),

        ok.
