=====================
用Erlang写HTTP Server
=====================

:date: 2014-10-10
:slug: http-server-in-erlang
:tags: Erlang, HTTP

很多人都在吹嘘REST架构。然而他们所谓的REST架构往往指的就是正确使用HTTP语义。REST架构的确是建立在正确使用HTTP语义之上的，然而在正确使用HTTP语义只是实现REST架构的基础。而那些吹嘘REST架构的人，往往号称自己是Web程序员。他们能对SSH框架，Rails框架侃侃而谈，却对HTTP协议一无所知，所以才会觉得REST很新鲜。

.. more

了解HTTP语义最好的方法，当然是照着RFC自己实现一遍了。推荐用Erlang来写。用Erlang你不再需要担心线程进程或者事件驱动，也不需要自己去解析HTTP Header，那当然是很方便了。


.. code:: erlang

    -module(server).
    -export([start/0, accept/1, handle_connection/1]).

    start() ->
        {ok, Socket} = gen_tcp:listen(8080, [binary, {packet, http}, {active, false}, {reuseaddr, true}]),
        Pid = spawn(?MODULE, accept, [Socket]),
        ok = gen_tcp:controlling_process(Socket, Pid),
        ok.

    accept(Socket) ->
        {ok, Conn} = gen_tcp:accept(Socket),
        Pid = spawn(?MODULE, handle_connection, [Conn]),
        ok = gen_tcp:controlling_process(Conn, Pid),
        ?MODULE:accept(Socket).

    handle_connection(Socket) ->
        {ok, {http_request, Method, Path, Version}} = gen_tcp:recv(Socket, 0),
        Headers = recv_headers(Socket),
        ok = inet:setopts(Socket, [{packet, raw}]),
        handle_request(Socket, Method, Path, Version, Headers).

    recv_headers(Socket) ->
        case gen_tcp:recv(Socket, 0) of
            {ok, {http_header, _, Field, _, Value}} ->
                [{Field, Value}|recv_headers(Socket)];
            {ok, http_eoh} ->
                []
        end.
 
    handle_request(Socket, 'GET', {abs_path, "/"}, {1,1}, _) -> 
        ok = gen_tcp:send(
               Socket,
               [<<"HTTP/1.1 200 OK\r\n">>,
                <<"Connection: close\r\n">>,
                <<"Content-Type: text-plain\r\n">>,
                <<"\r\n">>,
                <<"OK\r\n">>]),
        ok  = gen_tcp:close(Socket).


运行

.. code::

    erl -make
    erl -run server


在浏览器里打开\ http://127.0.0.1:8080/\ ，你就会看到 OK 。现在你就可以开始动手实现HTTP协议了。
