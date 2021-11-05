python = python3.9

.PHONY: benchmark
benchmark:
	mkdir -p logs
	$(python) -m benchmark
