from pybluemonday import UGCPolicy, StrictPolicy, NewPolicy
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
        Case("""<a href="?q=1&r=2">""", """<a href="?q=1&r=2" rel="nofollow">"""),
        Case("""<a href="?q=1&q=2">""", """<a href="?q=1&q=2" rel="nofollow">"""),
        Case(
            """<a href="?q=%7B%22value%22%3A%22a%22%7D">""",
            """<a href="?q=%7B%22value%22%3A%22a%22%7D" rel="nofollow">""",
        ),
        Case(
            """<a href="?q=1&r=2&s=:foo@">""",
            """<a href="?q=1&r=2&s=%3Afoo%40" rel="nofollow">""",
        ),
        Case(
            """<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />""",
            """<img alt="Red dot"/>""",
        ),
        Case("""<img src="giraffe.gif" />""", """<img src="giraffe.gif"/>"""),
        Case(
            """<img src="giraffe.gif?height=500&width=500" />""",
            """<img src="giraffe.gif?height=500&width=500"/>""",
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
