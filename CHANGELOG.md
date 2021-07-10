# 0.0.7 / UNRELEASED

- Bump bluemonday version to 1.0.15

# 0.0.6 / 2021-06-10

- Bump bluemonday version to 1.0.10

# 0.0.5 / 2021-04-25

- Bump bluemonday version to 1.0.9

# 0.0.4 / 2021-04-02

- Add more wheels and fix the ones that were broken (Windows)
- Pin versions with go.mod
- Make setup.py bootstrap itself to hopefully support building armv6 wheels
- Use uint32 instead of uint64 so we can support 32bit wheels
- Make pypi releases integrated into Github releases with Github Actions

# 0.0.3 / 2020-12-13

- Fixed memory leak caused by returning a CString from Go

# 0.0.2 / 2020-12-11

- Fixed issues where things like `&nbsp;` would show up as `\xa0`
- Added some tests duplicated out of bluemonday and html_sanitizer

# 0.0.1 / 2020-12-11

- Basic binding implementation and initial release
