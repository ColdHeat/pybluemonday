from pybluemonday import UGCPolicy, StrictPolicy, NewPolicy, SandboxValue
from collections import namedtuple
from multiprocessing.pool import ThreadPool, Pool

Case = namedtuple("Case", ["input", "output"])


def test_Empty():
    p = StrictPolicy()
    assert p.sanitize("") == ""


def test_SignatureBehaviour():
    cases = [
        Case("Hi.\n", "Hi.\n"),
        Case("\t\n \n\t", "\t\n \n\t"),
    ]

    p = UGCPolicy()
    for case in cases:
        assert p.sanitize(case.input) == case.output


def test_Links():
    cases = [
        Case(
            """<a href="http://www.google.com">""",
            """<a href="http://www.google.com" rel="nofollow">""",
        ),
        Case(
            """<a href="//www.google.com">""",
            """<a href="//www.google.com" rel="nofollow">""",
        ),
        Case(
            """<a href="/www.google.com">""",
            """<a href="/www.google.com" rel="nofollow">""",
        ),
        Case(
            """<a href="www.google.com">""",
            """<a href="www.google.com" rel="nofollow">""",
        ),
        Case("""<a href="javascript:alert(1)">""", ""),
        Case("""<a href="#">""", ""),
        Case("""<a href="#top">""", """<a href="#top" rel="nofollow">"""),
        Case("""<a href="?q=1">""", """<a href="?q=1" rel="nofollow">"""),
        Case("""<a href="?q=1&r=2">""", """<a href="?q=1&amp;r=2" rel="nofollow">"""),
        Case("""<a href="?q=1&q=2">""", """<a href="?q=1&amp;q=2" rel="nofollow">"""),
        Case(
            """<a href="?q=%7B%22value%22%3A%22a%22%7D">""",
            """<a href="?q=%7B%22value%22%3A%22a%22%7D" rel="nofollow">""",
        ),
        Case(
            """<a href="?q=1&r=2&s=:foo@">""",
            """<a href="?q=1&amp;r=2&amp;s=:foo@" rel="nofollow">""",
        ),
        Case(
            """<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />""",
            """<img alt="Red dot"/>""",
        ),
        Case("""<img src="giraffe.gif" />""", """<img src="giraffe.gif"/>"""),
        Case(
            """<img src="giraffe.gif?height=500&width=500" />""",
            """<img src="giraffe.gif?height=500&amp;width=500"/>""",
        ),
    ]

    p = UGCPolicy()
    p.RequireParseableURLs(True)

    def test_cases(case):
        assert p.sanitize(case.input) == case.output

    pool = ThreadPool(4)
    pool.map(test_cases, cases)


def test_LinkTargets():
    cases = [
        Case(
            """<a href="http://www.google.com">""",
            """<a href="http://www.google.com" rel="nofollow noopener" target="_blank">""",
        ),
        Case(
            """<a href="//www.google.com">""",
            """<a href="//www.google.com" rel="nofollow noopener" target="_blank">""",
        ),
        Case("""<a href="/www.google.com">""", """<a href="/www.google.com">"""),
        Case("""<a href="www.google.com">""", """<a href="www.google.com">"""),
        Case("""<a href="javascript:alert(1)">""", ""),
        Case("""<a href="#">""", ""),
        Case("""<a href="#top">""", """<a href="#top">"""),
        Case("""<a href="?q=1">""", """<a href="?q=1">"""),
        Case(
            """<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />""",
            """<img alt="Red dot"/>""",
        ),
        Case("""<img src="giraffe.gif" />""", """<img src="giraffe.gif"/>"""),
    ]

    p = UGCPolicy()
    p.RequireParseableURLs(True)
    p.RequireNoFollowOnLinks(False)
    p.RequireNoFollowOnFullyQualifiedLinks(True)
    p.AddTargetBlankToFullyQualifiedLinks(True)

    def test_cases(case):
        assert p.sanitize(case.input) == case.output

    pool = ThreadPool(4)
    pool.map(test_cases, cases)


def test_AllowComments():
    p = UGCPolicy()
    assert p.sanitize("1 <!-- 2 --> 3") == "1  3"
    p.AllowComments()
    assert p.sanitize("1 <!-- 2 --> 3") == "1 <!-- 2 --> 3"


def test_HrefSanitization():
    cases = [
        Case(
            """abc<a href="https://abc&quot;&gt;<script&gt;alert(1)<&#x2f;script/">CLICK""",
            """abc<a href="https://abc&amp;quot;&gt;&lt;script&gt;alert(1)&lt;/script/" rel="nofollow">CLICK""",
        ),
        Case(
            """<a href="https://abc&quot;&gt;<script&gt;alert(1)<&#x2f;script/">""",
            """<a href="https://abc&amp;quot;&gt;&lt;script&gt;alert(1)&lt;/script/" rel="nofollow">""",
        ),
    ]
    p = UGCPolicy()
    for case in cases:
        assert p.sanitize(case.input) == case.output


def test_selectStyleBug():
    # CVE-2021-42576 for bluemonday v1.0.16
    p = NewPolicy()

    # See https://github.com/ColdHeat/pybluemonday/issues/11 for why this is a loop
    for e in ["select", "option", "style"]:
        p.AllowElements(e)
    assert (
        p.sanitize("<select><option><style><script>alert(1)</script>")
        == "<select><option>"
    )
    p.AllowUnsafe(True)
    assert (
        p.sanitize("<select><option><style><script>alert(1)</script>")
        == "<select><option><style><script>alert(1)</script>"
    )


def test_IFrameSandbox():
    # Test updates from bluemonday v1.0.17
    p = NewPolicy()
    p.AllowAttrs("sandbox").OnElements("iframe")
    input = """<iframe src="http://example.com" sandbox="allow-forms allow-downloads allow-downloads"></iframe>"""
    out = """<iframe sandbox="allow-forms allow-downloads allow-downloads"></iframe>"""
    assert p.sanitize(input) == out


def test_IFrameSandboxAttribute():
    # Test updates from bluemonday v1.0.17
    p = NewPolicy()
    p.AllowIFrames()
    input = """<iframe src="http://example.com" sandbox="allow-forms allow-downloads allow-downloads"></iframe>"""
    out = """<iframe sandbox=""></iframe>"""
    assert p.sanitize(input) == out

    p = NewPolicy()
    p.AllowIFrames()
    input = """<iframe src="http://example.com" sandbox="allow-forms allow-downloads allow-downloads"></iframe>"""
    out = """<iframe sandbox=""></iframe>"""
    assert p.sanitize(input) == out

    p.RequireSandboxOnIFrame(SandboxValue.SandboxAllowDownloads)
    input = """<iframe src="http://example.com" sandbox="allow-forms allow-downloads allow-downloads"></iframe>"""
    out = """<iframe sandbox="allow-downloads"></iframe>"""
    assert p.sanitize(input) == out

    p.RequireSandboxOnIFrame(SandboxValue.SandboxAllowForms)
    input = """<iframe src="http://example.com" sandbox="allow-forms allow-downloads allow-downloads"></iframe>"""
    out = """<iframe sandbox="allow-forms"></iframe>"""
    assert p.sanitize(input) == out
