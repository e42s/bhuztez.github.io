====================
如何实现Prolog解释器
====================

:date: 2014-03-23
:slug: how-to-write-a-prolog-interpreter
:tags: Prolog

Prolog语言本身就不太容易理解。要理解Prolog，不如先写个简单的Prolog解释器。然而这也不那么容易，还好有\ `Warren's Abstract Machine: A Tutorial Reconstruction <http://wambook.sourceforge.net/>`_\ 。

.. more

WAMBOOK里把实现Prolog的过程分成L0、L1、L2、L3四个阶段。也就是把一个困难的问题，分解成了四个比较容易的问题。这样只看slides，也是能自己写出来的，未必需要先把WAMBOOK完整看一遍。值得注意的是，WAMBOOK是按C的思路来讲的，用的是可变的数据结构，回溯时会根据trail区域的内容重置对应的变量。这个还是非常繁琐的。Erlang基本数据类型都是不可变的，回溯时直接退回老版本的就可以了。差别特别大的是Unification部分，不如参考\ `miniKanren的论文 <http://gradworks.umi.com/33/80/3380156.html>`_\ 。Unification以外的部分就不推荐了，因为都是用很费解的宏写的，而且现在是要实现Prolog解释器。

Prolog中的\ :code:`atom`\ 可以直接用Erlang中的\ :code:`atom`\ 表示，而\ :code:`a(b,c)`\ 用\ :code:`{term, a, [b,c]}`\ 表示，变量\ :code:`X`\ 用\ :code:`{var, 'X'}`\ 表示，而变量的cell，用\ :code:`{var, 1}`\ 表示，不同的整数表示不同的cell。


.. code:: erlang

    -module(prolog).

    -export([test/0]).

    lookup(K, []) ->
        {var, K};
    lookup(K, [{K,V}|_]) ->
        V;
    lookup(K, [_|S]) ->
        lookup(K, S).

    lookup_var(V, S) ->
        case lookup(V, S) of
            {var, V1} when V1 =/= V ->
                lookup_var(V1, S);
            Other ->
                Other
        end.

    subst({var, V}, S) ->
        case lookup_var(V, S) of
            {var, _} = V1 ->
                V1;
            Other ->
                subst(Other, S)
        end;
    subst({term, F, A}, S) ->
        {term, subst(F, S), subst(A, S)};
    subst([], _S) ->
        [];
    subst([H|T], S) ->
        [subst(H,S)|subst(T,S)];
    subst(Atom, _) when is_atom(Atom) ->
        Atom.

    occurs(X, {var, V}, S) ->
        case lookup_var(V ,S) of
            {var, Y} ->
                X =:= Y;
            Other ->
                occurs(X, Other, S)
        end;
    occurs(X, {term, F, A}, S) ->
        occurs(X, [F|A], S);
    occurs(X, [H|T], S) ->
        occurs(X, H, S) or occurs(X, T, S);
    occurs(_, _, _) ->
        false.

    unify({var, V1}, Y, S) ->
        case lookup_var(V1, S) of
            {var, X} ->
                case occurs(X, Y, S) of
                    true ->
                        case Y of
                            {var, V2} ->
                                case lookup_var(V2, S) of
                                    {var, X} ->
                                        S;
                                    _ ->
                                        false
                                end;
                            _ ->
                                false
                        end;
                    false ->
                        [{X,Y}|S]
                end;
            Other ->
                unify(Other, Y, S)
        end;
    unify(X, {var, _} = Y, S) ->
        unify(Y, X, S);
    unify({term, F1, A1}, {term, F2, A2}, S) ->
        unify([F1|A1], [F2|A2], S);
    unify([], [], S) ->
        S;
    unify([H1|T1], [H2|T2], S) ->
        case unify(H1, H2, S) of
    	false ->
    	    false;
    	S1 ->
    	    unify(T1, T2, S1)
        end;
    unify(A, A, S) when is_atom(A) ->
        S;
    unify(_, _, _) ->
        false.


    reify({var, '_'}, S, C) ->
        {{var, C}, S, C+1};
    reify({var, V}, S, C) ->
        case lookup_var(V, S) of
            {var, N} when is_integer(N) ->
                {{var, N}, S, C};
            {var, V1} ->
                {{var, C}, [{V1, {var, C}}|S], C+1};
            Other ->
                reify(Other, S, C)
        end;
    reify({term, F, A}, S, C) ->
        {[F1|A1], S1, C1} = reify([F|A], S, C),
        {{term, F1, A1}, S1, C1};
    reify([H|T], S, C) ->
        {H1, S1, C1} = reify(H, S, C),
        {T1, S2, C2} = reify(T, S1, C1),
        {[H1|T1], S2, C2};
    reify(X, S, C) ->
        {X, S, C}.


    term_to_list({term, F, A}) ->
        [F|A];
    term_to_list(Atom) when is_atom(Atom) ->
        [Atom].

    pred_name(F, A) ->
        list_to_atom(atom_to_list(F) ++ "/" ++ integer_to_list(length(A))).

    make_db(Clauses) ->
        lists:foldl(
          fun ({clause, Head, Body}, Dict) ->
                  [F|A] = term_to_list(Head),
                  dict:append(
                    pred_name(F,A),
                    {rule, tl(term_to_list(Head)), Body},
                    Dict)
          end,
          dict:new(),
          Clauses).


    answer(S, G) ->
        R = [{V, {var, K}} || {K, {var,V}} <- S ],
        Answer = [{K, subst(subst(V, G), R)} || {K,V} <- S],
        [ {K,V}
          || {K, V} <- Answer,
             case V of
                 {var, K} -> false;
                 _ -> true
             end
        ].


    %% l0: one fact only
    query_l0(Query, Head) ->
        {Q, S, C} = reify(Query, [], 0),
        case prim_l0({rule, Head, []}, Q, [], C) of
            false ->
                false;
            G ->
                answer(S, G)
        end.

    prim_l0({rule, Head, []}, A, G, C) ->
        {Head1, _, _} = reify(Head, G, C),
        unify(Head1, A, G).


    %% l1 -> one fact per predicate
    query_l1(Query, DB) ->
        {Q, S, C} = reify(Query, [], 0),
        case call_l1(Q, [], C, DB) of
    	false ->
    	    false;
    	G ->
    	    answer(S, G)
        end.

    call_l1(Term, G, C, DB) ->
        [F|A] = term_to_list(Term),
        Name = pred_name(F, A),
        case dict:find(Name, DB) of
            error ->
                false;
            {ok, [Rule]} ->
                prim_l0(Rule, A, G, C)
        end.


    %% l2 -> one clause per predicate
    query_l2(Query, DB) ->
        case success_l2([{[], Query}], [], 0, DB) of
            false ->
                false;
            Answer ->
                Answer
        end.

    success_l2([{S, []}], G, _C, _DB) ->
        answer(S, G);
    success_l2([{_, []}|Rest], G, C, DB) ->
        success_l2(Rest, G, C, DB);
    success_l2([{S, [H|T]}|Rest], G, C, DB) ->
        {H1, S1, C1} = reify(H, S, C),
        call_l2(H1, [{S1,T}|Rest], G, C1, DB).

    call_l2(Term, Stack, G, C, DB) ->
        [F|A] = term_to_list(Term),
        Name = pred_name(F, A),
        case dict:find(Name, DB) of
            error ->
                false;
            {ok, [Rule]} ->
                prim_l2(Rule, A, Stack, G, C, DB)
        end.

    prim_l2({rule, Head, Body}, A, Stack, G, C, DB) ->
        {Head1, S, C1} = reify(Head, [], C),
        case unify(Head1, A, G) of
    	false ->
    	    false;
    	G1 ->
    	    success_l2([{S, Body}|Stack], G1, C1, DB)
        end.


    %% l3 -> multiple clauses per predicate
    query_l3(Query, DB) ->
        case success_l3([{[], Query}], [], 0, [], DB) of
            false ->
                false;
            {Answer, Cont} ->
                {Answer, Cont}
        end.

    success_l3([{S, []}], G, _C, Cont, _DB) ->
        {answer(S, G), Cont};
    success_l3([{_, []}|Rest], G, C, Cont, DB) ->
        success_l3(Rest, G, C, Cont, DB);
    success_l3([{S, [H|T]}|Rest], G, C, Cont, DB) ->
        {H1, S1, C1} = reify(H, S, C),
        call_l3(H1, [{S1,T}|Rest], G, C1, Cont, DB).

    call_l3(Term, Stack, G, C, Cont, DB) ->
        [F|A] = term_to_list(Term),
        Name = pred_name(F, A),

        case dict:find(Name, DB) of
            error ->
                Choices = [];
            {ok, Choices} ->
                ok
        end,

        cont_l3([{Choices, A, Stack, G, C}|Cont], DB).

    cont_l3([], _) ->
        false;
    cont_l3([{[], _, _, _, _}|Rest], DB) ->
        cont_l3(Rest, DB);
    cont_l3([{[H|T], A, Stack, G, C}|Rest], DB) ->
        prim_l3(H, A, Stack, G, C, [{T, A, Stack, G, C}|Rest], DB).


    prim_l3({rule, Head, Body}, A, Stack, G, C, Cont, DB) ->
        {Head1, S, C1} = reify(Head, [], C),
        case unify(Head1, A, G) of
    	false ->
    	    cont_l3(Cont, DB);
    	G1 ->
    	    success_l3([{S, Body}|Stack], G1, C1, Cont, DB)
        end.


    test(lookup_var) ->
        X = {'X',a},
        Y = {'Y',{var,'X'}},
        {var, 'X'} = lookup_var('X', []),
        {var, 'X'} = lookup_var('X', [Y]),
        a = lookup_var('X', [X]),
        a = lookup_var('Y', [X,Y]),
        {var, 'X'} = lookup_var('Y', [Y]),
        ok;
    test(occurs) ->
        false = occurs('X', a, []),
        true = occurs('X', {var, 'X'}, []),
        S = [{'X', {var, 'Y'}}],
        false = occurs('Y', {var, 'X'}, []),
        true = occurs('Y', {var, 'X'}, S),
        false = occurs('Y', {term, {var, 'X'}, []}, []),
        true = occurs('Y', {term, {var, 'X'}, []}, S),
        false = occurs('Y', {term, a, [{var, 'X'}]}, []),
        true = occurs('Y', {term, a, [{var, 'X'}]}, S),
        ok;
    test(unify) ->
        false = unify(a, b, []),
        [] = unify(a, a, []),

        S = [{'X',a}],
        S = unify({var, 'X'}, a, S),
        false = unify({var, 'X'}, b, S),
        S = unify({var, 'X'}, a, []),
        S = unify(a, {var, 'X'}, []),

        S = unify({term, {var, 'X'}, []}, {term, a, []}, []),
        S = unify({term, {var, 'X'}, []}, {term, a, []}, S),
        S = unify({term, a, [{var, 'X'}]}, {term, a, [a]}, []),
        S = unify({term, a, [{var, 'X'}]}, {term, a, [a]}, S),

        S1 = [{'X', {var, 'Y'}}],
        S1 = unify({var, 'X'}, {var, 'Y'}, []),
        S1 = unify({var, 'Y'}, {var, 'X'}, S1),
        S1 = unify({var, 'X'}, {var, 'Y'}, S1),

        S2 = unify({var, 'X'}, {var, 'Y'}, S),
        S2 = unify({var, 'Y'}, a, S2),

        S3 = [{'Y', b}|S],
        S3 = unify({term, {var, 'X'}, [b]}, {term, a, [{var, 'Y'}]}, []),
        S3 = unify({term, {var, 'X'}, [b]}, {term, a, [{var, 'Y'}]}, S3),
        ok;
    test(subst) ->
        S = [{'X', {term, {var, 'Y'}, [{var, 'Z'}]}},
             {'Y', a},
             {'Z', b}],
        {term, {var, 'Y'}, [{var, 'Z'}]} = lookup_var('X', S),
        {term, a, [b]} = subst({var, 'X'}, S),
        ok;
    test(reify) ->
        {_, [{'X', {var, 0}}], 1} = reify({var, 'X'}, [], 0),
        ok;
    test(l0) ->
        [{'Y',c}, {'X',b}] =
            query_l0(
              %% a(X,Y).
              {term, a, [{var, 'X'}, {var, 'Y'}]},
              %% a(b,c).
              {term, a, [b, c]}),

        [{'X',{var,'Y'}}] =
            query_l0(
              %% a(X,Y).
              {term, a, [{var, 'X'}, {var, 'Y'}]},
              %% a(X,Y).
              {term, a, [{var, 'X'}, {var, 'X'}]}),

        [] =
            query_l0(
              %% a(X,Y).
              {term, a, [{var, 'X'}, {var, 'Y'}]},
              %% a(_,_).
              {term, a, [{var, '_'}, {var, '_'}]}),

        false =
            query_l0(
              %% b(c,d).
              {term, b, [c,d]},
              %% a(b,c).
              {term, a, [b,c]}),

        [] =
            query_l0(
              %% a.
              {term, a, []},
              %% a.
              {term, a, []}),

        ok;
    test(l1) ->
        DB =
            make_db(
              %% a. b.
              [ {clause, {term, a, []}, []},
                {clause, {term, b, []}, []}
              ]
             ),

        %% b.
        [] = query_l1({term, b, []}, DB),
        %% c.
        false = query_l1({term, c, []}, DB),

        [{'Y',c},{'X',b}] =
            query_l1(
              %% a(X,Y).
              {term, a, [{var, 'X'}, {var, 'Y'}]},
              %% a(b,c).
              make_db([{clause, {term, a, [b,c]}, []}])),
        ok;
    test(l2) ->
        %% a.
        false = query_l2([{term, a, []}], make_db([])),

        [{'Y',a},{'X',b}] =
            query_l2(
              %% a(X), b(Y).
              [{term, a, [{var, 'X'}]}, {term, b, [{var, 'Y'}]}],
              make_db(
                %% a(b). b(a).
                [{clause, {term, a, [b]}, []},
                 {clause, {term, b, [a]}, []}
                ])
             ),

        [{'Y',b},{'X',a}] =
            query_l2(
              %% a(X,Y).
              [{term, a, [{var, 'X'}, {var, 'Y'}]}],
              make_db(
                %% a(X,b) :- b(X).
                %% b(a).
                [{clause,
                  {term, a, [{var, 'X'}, b]},
                  [{term, b, [{var, 'X'}]}]},
                 {clause, {term, b, [a]}, []}
                ])
             ),

        ok;
    test(l3) ->
        DB1 =
            make_db(
              %% a(b,b). a(a,b). b(a).
              [{clause, {term, a, [b,b]}, []},
               {clause, {term, a, [a,b]}, []},
               {clause, {term, b, [a]}, []}
              ]),
        {[{'Y',b},{'X',a}], Cont1} =
            query_l3(
              %% a(X,Y), b(X).
              [{term, a, [{var, 'X'}, {var, 'Y'}]},
               {term, b, [{var, 'X'}]}],
              DB1),
        false = cont_l3(Cont1, DB1),

        DB2 =
            make_db(
              %% a(a,b). a(a,b). a(a,b).
              [{clause, {term, a, [a,b]}, []},
               {clause, {term, a, [a,b]}, []},
               {clause, {term, a, [a,b]}, []}
              ]),
        {[{'Y',b},{'X',a}], Cont2} =
            query_l3(
              %% a(X,Y)
              [{term, a, [{var, 'X'}, {var, 'Y'}]}],
              DB2),
        {[{'Y',b},{'X',a}], Cont3} = cont_l3(Cont2, DB2),
        {[{'Y',b},{'X',a}], Cont4} = cont_l3(Cont3, DB2),
        false = cont_l3(Cont4, DB2),
        ok.


    test() ->
        test(lookup_var),
        test(occurs),
        test(unify),
        test(subst),
        test(reify),
        test(l0),
        test(l1),
        test(l2),
        test(l3),
        ok.
