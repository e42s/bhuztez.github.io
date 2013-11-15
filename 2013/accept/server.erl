-module(server).

-export([start/0, listen/1, loop/1]).

start() ->
    spawn(server, listen, [9000]).

listen(Port) ->
    {ok, Socket} = gen_tcp:listen(
		     Port, 
		     [binary, 
		      {packet, raw},
		      {reuseaddr, true},
		      {active, false},
		      {backlog, 128}]),
    process_flag(priority, max),
    accept(Socket).

accept(Socket) ->
    {ok, Conn} = gen_tcp:accept(Socket),
    gen_tcp:controlling_process(Conn, spawn(server, loop, [Conn])),
    accept(Socket).

loop(Socket) ->
    case gen_tcp:recv(Socket, 0) of
	{ok, Data} ->
	    gen_tcp:send(Socket, Data),
	    loop(Socket);
	{error, closed} ->
	    gen_tcp:close(Socket),
	    ok
    end.
