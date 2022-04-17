default: clean test build

clean:
	find . -name '__pycache__' -delete -print \
		-o -name '*.pyc' -delete -print

build:
	docker build --target builder -t wordle_solver .

build-test:
	docker build --target tester -t wordle_solver_test .

test: build-test
	docker rm -f src_test || echo "container removed"
	docker run --rm --name wordle_solver_test wordle_solver_test
	docker rm -f src_test || echo "container removed"

run: build
	docker run --rm --name wordle_solver wordle_solver
