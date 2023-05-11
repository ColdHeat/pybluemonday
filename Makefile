so:
	go get -d
	go build -buildmode=c-shared -o bluemonday.so .

dll:
	go get -d
	go build -buildmode=c-shared -o bluemonday.dll .

ffi:
	python3 build_ffi.py

clean:
	rm -f bluemonday.so
	rm -f bluemonday.dll
	rm -f bluemonday.*.so
	rm -f bluemonday.o
	rm -f bluemonday.h
	rm -f bluemonday.c
	rm -rf build/
	rm -rf dist/

test:
	python -m pytest
