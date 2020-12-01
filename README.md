# pybluemonday

pybluemonday is a library for sanitizing HTML very quickly via [bluemonday](https://github.com/microcosm-cc/bluemonday).

pybluemonday takes untrusted user generated content as an input, and will return HTML that has been sanitised against a whitelist of approved HTML elements and attributes so that you can safely include the content in your web page.

## Installation

```
pip install pybluemonday
```

## How does this work?

pybluemonday is a binding to [bluemonday](https://github.com/microcosm-cc/bluemonday) through a shared library built through cgo.

## Performance

Most Python based HTML sanitizing libraries will need to rely on [html5lib](https://html5lib.readthedocs.io/en/latest/) for parsing HTML in a reasoanble way. Because of this you will likely see performance hits when using these libraries.

Since pybluemonday is just bindings for [bluemonday](https://github.com/microcosm-cc/bluemonday) it has *very* good performance because all parsing and processing is done in Go by bluemonday. Go also ships an [HTML5 parser](https://godoc.org/golang.org/x/net/html) which means we avoid html5lib but still process HTML well.

Always take benchmarks with a grain of salt but when compared to other similar Python sanitizing libraries pybluemonday executes far faster:

```
❯ python benchmarks.py
bleach (20000 sanitizations): 36.573391182
html_sanitizer (20000 sanitizations): 17.280117869
bluemonday (20000 sanitizations): 0.6063146659999958
```