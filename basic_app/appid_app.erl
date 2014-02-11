-module({{ appid }}_app).

-behaviour(application).

%% application callbacks
-export([start/2, stop/1]).

-include("{{ appid }}.hrl").

%% ===================================================================
%% application callbacks
%% ===================================================================

start(_StartType, _StartArgs) ->
    {{ appid }}_sup:start_link().

stop(_State) ->
    ok.
