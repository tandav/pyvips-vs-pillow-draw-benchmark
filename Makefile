python = python3.9

.PHONY: benchmark
benchmark:
	mkdir -p logs
	$(python) -m benchmark

lint:
	$(python) -m isort --force-single-line-imports benchmark
	$(python) -m autoflake --recursive --in-place benchmark
	$(python) -m autopep8 --verbose --in-place --recursive --aggressive --ignore=E221,E401,E402,E501,W503,E701,E704,E721,E741,I100,I201,W504 --exclude=musictools/util/wavfile.py benchmark
	$(python) -m unify --recursive --in-place benchmark
	$(python) -m flake8 benchmark
