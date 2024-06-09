so:
	go install
ifndef GOARCH
	go build -buildmode=c-shared -o bluemonday.so .
else
	CGO_ENABLED=1 GOARCH=${GOARCH} go build -buildmode=c-shared -o bluemonday.so .
endif

ffi:
	python3 build_ffi.py

clean:
	rm -f bluemonday.so
	rm -f bluemonday.*.so
	rm -f bluemonday.o
	rm -f bluemonday.h
	rm -f bluemonday.c
	rm -rf build/
	rm -rf dist/

test:
	python -m pytest
