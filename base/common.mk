.PHONY: all compile test clean
NAME = {{ name }}

REBAR_BIN = $(abspath ./)/rel/../rebar
ifeq ($(wildcard $(REBAR_BIN)),)
	REBAR_BIN := $(shell which rebar)
endif
REBAR = $(REBAR_BIN) -C rebar.config

# MAKERS

all: compile

compile: update-deps
	$(MAKE) pre-compile
	$(REBAR) compile
	$(MAKE) post-compile

update-deps: deps/.updated
deps/.updated:
	$(REBAR) update-deps ignore_deps=true
	@touch deps/.updated

get-deps:
	@$(REBAR) get-deps

clean: pre-clean
	$(REBAR) clean
	rm -f rel/reltool.config
	rm -rf rel/$(SERVICE_NAME)*
	$(MAKE) post-clean

# OVERWRITES
pre-compile:
post-compile:
pre-clean:
post-clean: