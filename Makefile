so:
	go get -d
	go build -buildmode=c-shared -o bluemonday.so .

ffi:
	python3 build_ffi.py

clean:
	rm -f bluemonday.so
	rm -f bluemonday.o
	rm -f bluemonday.h
	rm -f bluemonday.c

test:
	python -m pytest
