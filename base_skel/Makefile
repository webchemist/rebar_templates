deps:
	@rebar get-deps

compile:
	@rebar compile

generate:
	@rebar generate force=1

dev: compile
	@erl -pa ebin -pa deps/*/ebin -config dev.config -s lager -s sync

eu: compile
	@rebar skip_deps=true eunit

init_plt:
	@dialyzer --build_plt --output_plt ~/.dialyzer_prj.plt --apps inets sasl stdlib eunit common_test appmon erts mnesia os_mon tools xmerl

update_plt:
	@dialyzer --add_to_plt --plt ~/.dialyzer_prj.plt -r /ebin -r `find deps/ -iname ebin`