# 0.0.11 / 2023-05-12

- Release wheels for Python 3.11 with the exception of Windows
- Release wheels for Apple Silicon
- Drop support for Python 3.6

# 0.0.10 / 2023-04-12

- Bump bluemonday to 1.0.23
- Fix vulnerability that was present in versions below 1.0.20 regarding the usage of `.AllowComments()`. See https://github.com/microcosm-cc/bluemonday/releases/tag/v1.0.20.

# 0.0.9 / 2022-02-11

- Bump bluemonday to 1.0.18
- Implement rough support for `RequireSandboxOnIFrame` by having an approach to call functions that take typed arguments
  - This doesn't work entirely because currently only a single call to `RequireSandboxOnIFrame` will work but it will suffice until this behavior is actually needed.
- Build wheels for Python 3.10 (Closes #29)

# 0.0.8 / 2021-10-18

- Bump bluemonday version to 1.0.16

# 0.0.7 / 2021-07-09

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
