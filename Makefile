build:
	go build -buildmode=c-shared -o bluemonday.so .

ffi:
	python build_ffi.py

clean:
	rm bluemonday.so
	rm bluemonday.o
	rm bluemonday.h
	rm bluemonday.c