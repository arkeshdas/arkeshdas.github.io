.PHONY: sync build serve clean consistency check

sync:
	uv sync

build:
	uv run python build.py

serve:
	uv run python serve.py

clean:
	rm -rf docs

consistency:
	uv run python tools/check_consistency.py

check: consistency build
	git status --short
