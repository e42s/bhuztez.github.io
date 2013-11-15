all: c-client cpp-client c-server cpp-server server.beam

c-%: %.c
	gcc -std=c99 -Os -o "$@" "$<"

cpp-%: %.cpp
	g++ -O3 -o "$@" "$<" -lboost_system -lboost_thread -lpthread

%.beam: %.erl
	erlc "$<"

clean:
	rm -rf c-client cpp-client c-server cpp-server server.beam
