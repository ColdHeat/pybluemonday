build:
	go build -buildmode=c-shared -o bluemonday.so .
	python build_ffi.py