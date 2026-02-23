.PHONY: test-python test-typescript test-go test-java test-csharp test-cpp test-all

test-python:
	cd runners/python && python -m pytest -v

test-typescript:
	npx vitest run --config runners/typescript/vitest.config.ts

test-go:
	python3 runners/go/run_tests.py

test-java:
	python3 runners/java/run_tests.py

test-csharp:
	python3 runners/csharp/run_tests.py

test-cpp:
	python3 runners/cpp/run_tests.py

test-all: test-python test-typescript test-go test-java test-csharp test-cpp
