============
二十四点去重
============

:date: 2014-11-04
:slug: distinct-game24-solution


二十四点解法去重的思路很简单，就是根据把语法树根据等价公式找出相邻的语法树，得到以语法树为节点的边的集合，根据这个集合，进行unification，这样就把结果分组了，有几个组就是有几个不同的结果。

.. more

.. code:: erlang

    -module(game24).
    -compile(export_all).

    permutation(0,_) ->[[]];
    permutation(_,[])->[];
    permutation(N,L) ->[[E|T]||E<-L,T<-permutation(N-1,L--[E])].

    gcd(A,0)-> A;
    gcd(A,B)-> gcd(B, A rem B).

    frac(X) when is_integer(X) -> {frac, X, 1};
    frac({frac, X, Y})         -> G = gcd(X,Y), {frac, X div G, Y div G}.

    calc('+',{frac,A1,A2},{frac,B1,B2}) -> {frac, A1*B2+B1*A2, A2*B2};
    calc('-',{frac,A1,A2},{frac,B1,B2}) -> {frac, A1*B2-B1*A2, A2*B2};
    calc('*',{frac,A1,A2},{frac,B1,B2}) -> {frac, A1*B1,       A2*B2};
    calc('/',{frac,A1,A2},{frac,B1,B2}) -> {frac, A1*B2,       A2*B1}.

    rpn([], [], [], [N]) ->
        frac(N);
    rpn([push|AT], [NH|NT], Ops, Stack) ->
        rpn(AT, NT, Ops, [NH|Stack]);
    rpn([calc|AT], Nums, [OH|OT], [B,A|Stack]) ->
        rpn(AT, Nums, OT, [calc(OH,frac(A),frac(B))|Stack]).

    rpn2tree([], [], [], [N]) ->
        N;
    rpn2tree([push|AT], [NH|NT], Ops, Stack) ->
        rpn2tree(AT, NT, Ops, [NH|Stack]);
    rpn2tree([calc|AT], Nums, [OH|OT], [B,A|Stack]) ->
        rpn2tree(AT, Nums, OT, [{A, OH, B}|Stack]).

    n1({A,O,B})->[{N,O,B}||N<-neighbours(A)] ++ [{A,O,N}||N<-neighbours(B)];
    n1(_)      ->[].

    %% A+B = B+A
    %% A*B = B*A

    n2({A,'+',B})->[{B,'+',A}];
    n2({A,'*',B})->[{B,'*',A}];
    n2(_)        ->[].

    %% (A+B)+C = A+(B+C)
    %% (A*B)*C = A*(B*C)

    n3({{A,'+',B},'+',C})->[{A,'+',{B,'+',C}}];
    n3({A,'+',{B,'+',C}})->[{{A,'+',B},'+',C}];
    n3({{A,'*',B},'*',C})->[{A,'*',{B,'*',C}}];
    n3({A,'*',{B,'*',C}})->[{{A,'*',B},'*',C}];
    n3(_)                ->[].

    %% (A-B)+C = A+(C-B) = (A+C)-B = A-(B-C)
    %% (A/B)*C = A*(C/B) = (A*C)/B = A/(B/C)

    n4({{A,'-',B},'+',C}) ->
        [{A,'+',{C,'-',B}}, {{A,'+',C},'-',B}, {A,'-',{B,'-',C}}];
    n4({A,'+',{C,'-',B}}) ->
        [{{A,'-',B},'+',C}, {{A,'+',C},'-',B}, {A,'-',{B,'-',C}}];
    n4({{A,'+',C},'-',B}) ->
        [{{A,'-',B},'+',C}, {A,'+',{C,'-',B}}, {A,'-',{B,'-',C}}];
    n4({A,'-',{B,'-',C}}) ->
        [{A,'-',{B,'-',C}}, {A,'+',{C,'-',B}}, {{A,'+',C},'-',B}];
    n4({{A,'/',B},'*',C}) ->
        [{A,'*',{C,'/',B}}, {{A,'*',C},'/',B}, {A,'/',{B,'/',C}}];
    n4({A,'*',{C,'/',B}}) ->
        [{{A,'/',B},'*',C}, {{A,'*',C},'/',B}, {A,'/',{B,'/',C}}];
    n4({{A,'*',C},'/',B}) ->
        [{{A,'/',B},'*',C}, {A,'*',{C,'/',B}}, {A,'/',{B,'/',C}}];
    n4({A,'/',{B,'/',C}}) ->
        [{A,'/',{B,'/',C}}, {A,'*',{C,'/',B}}, {{A,'*',C},'/',B}];
    n4(_) ->
        [].

    %% (A-B)-C = A-(B+C) = (A-C)-B
    %% (A/B)/C = A/(B*C) = (A/C)/B

    n5({{A,'-',B},'-',C})->[{A,'-',{B,'+',C}}, {{A,'-',C},'-',B}];
    n5({A,'-',{B,'+',C}})->[{{A,'-',B},'-',C}, {{A,'-',C},'-',B}];
    n5({{A,'-',C},'-',B})->[{{A,'-',B},'-',C}, {A,'-',{B,'+',C}}];
    n5({{A,'/',B},'/',C})->[{A,'/',{B,'*',C}}, {{A,'/',C},'/',B}];
    n5({A,'/',{B,'*',C}})->[{{A,'/',B},'/',C}, {{A,'/',C},'/',B}];
    n5({{A,'/',C},'/',B})->[{{A,'/',B},'/',C}, {A,'/',{B,'*',C}}];
    n5(_)                ->[].

    neighbours(X) -> n1(X)++n2(X)++n3(X)++n4(X)++n5(X).

    indexof(E, L) -> indexof(1, E, L).

    indexof(N, E, [E|_]) -> N;
    indexof(N, E, [_|T]) -> indexof(N+1, E, T).

    nth(1, [H|_]) -> H;
    nth(N, [_|T]) -> nth(N-1, T).

    unify(A,B,D) ->
        case dict:fetch(A,D) of
            A ->
                case dict:fetch(B,D) of
                    B ->
                        case B of
                            A ->
                                D;
                            _ ->
                                dict:store(B, A, D)
                        end;
                    M ->
                        unify(A,M,D)
                end;
            N ->
                unify(N,B,D)
        end.

    unify({A,B},D) -> unify(A,B,D).

    solve(Nums) ->
        Actions =
            [
             [push, push, push, push, calc, calc, calc],
             [push, push, push, calc, push, calc, calc],
             [push, push, push, calc, calc, push, calc],
             [push, push, calc, push, push, calc, calc],
             [push, push, calc, push, calc, push, calc]
            ],

        Results =
            [rpn2tree(A,N,[O1,O2,O3],[])
             || A <- Actions, N <- permutation(4, Nums),
                O1 <-['+', '-', '*', '/'],
                O2 <-['+', '-', '*', '/'],
                O3 <-['+', '-', '*', '/'],
                rpn(A,N,[O1,O2,O3],[]) == {frac, 24, 1}],

        Neighbours =
            [{indexof(A, Results), indexof(B, Results)} || A <- Results, B <- neighbours(A)],

        I = lists:seq(1, length(Results)),
        Map = dict:to_list(lists:foldl(fun unify/2, dict:from_list(lists:zip(I, I)), Neighbours)),
        [nth(X,Results) || {X,X} <- Map].



运行结果


.. code::

    1> game24:solve([1,3,8,12]).
    [{1,'+',{12,'+',{3,'+',8}}},
     {8,'*',{{12,'/',3},'-',1}},
     {12,'*',{8,'/',{1,'+',3}}}]
