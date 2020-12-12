from pybluemonday import UGCPolicy, StrictPolicy, NewPolicy
from collections import namedtuple

Case = namedtuple("Case", ["input", "output"])


def test_StrictPolicy():
    cases = [
        Case(input="Hello, <b>World</b>!", output="Hello, World!"),
        Case(input="<blockquote>Hello, <b>World</b>!", output="Hello, World!"),
        Case(
            input="<quietly>email me - addy in profile</quiet>",
            output="email me - addy in profile",
        ),
    ]

    p = StrictPolicy()
    for case in cases:
        assert p.sanitize(case.input) == case.output


def test_UGCPolicy():
    cases = [
        Case("Hello, World!", "Hello, World!"),
        Case("Hello, <b>World</b>!", "Hello, <b>World</b>!"),
        Case(
            "<p>Hello, <b onclick=alert(1337)>World</b>!</p>",
            "<p>Hello, <b>World</b>!</p>",
        ),
        Case(
            "<p onclick=alert(1337)>Hello, <b>World</b>!</p>",
            "<p>Hello, <b>World</b>!</p>",
        ),
        Case("""<a href="javascript:alert(1337)">foo</a>""", "foo"),
        Case(
            """<img src="http://example.org/foo.gif">""",
            """<img src="http://example.org/foo.gif">""",
        ),
        Case(
            """<img src="http://example.org/x.gif" alt="y" width=96 height=64 border=0>""",
            """<img src="http://example.org/x.gif" alt="y" width="96" height="64">""",
        ),
        Case(
            """<img src="http://example.org/x.png" alt="y" width="widgy" height=64 border=0>""",
            """<img src="http://example.org/x.png" alt="y" height="64">""",
        ),
        Case(
            """<a href="foo.html">Link text</a>""",
            """<a href="foo.html" rel="nofollow">Link text</a>""",
        ),
        Case(
            """<a href="foo.html" onclick="alert(1337)">Link text</a>""",
            """<a href="foo.html" rel="nofollow">Link text</a>""",
        ),
        Case(
            """<a href="http://example.org/x.html" onclick="alert(1337)">Link text</a>""",
            """<a href="http://example.org/x.html" rel="nofollow">Link text</a>""",
        ),
        Case(
            """<a href="https://example.org/x.html" onclick="alert(1337)">Link text</a>""",
            """<a href="https://example.org/x.html" rel="nofollow">Link text</a>""",
        ),
        Case(
            """<a href="//example.org/x.html" onclick="alert(1337)">Link text</a>""",
            """<a href="//example.org/x.html" rel="nofollow">Link text</a>""",
        ),
        Case(
            """<a href="javascript:alert(1337).html" onclick="alert(1337)">Link text</a>""",
            """Link text""",
        ),
        Case(
            """<a name="header" id="header">Header text</a>""",
            """<a id="header">Header text</a>""",
        ),
        Case(
            """<img src="planets.gif" width="145" height="126" alt="" usemap="#demomap"><map name="demomap"><area shape="rect" coords="0,0,82,126" href="demo.htm" alt="1"><area shape="circle" coords="90,58,3" href="demo.htm" alt="2"><area shape="circle" coords="124,58,8" href="demo.htm" alt="3"></map>""",
            """<img src="planets.gif" width="145" height="126" alt="" usemap="#demomap"><map name="demomap"><area shape="rect" coords="0,0,82,126" href="demo.htm" alt="1" rel="nofollow"><area shape="circle" coords="90,58,3" href="demo.htm" alt="2" rel="nofollow"><area shape="circle" coords="124,58,8" href="demo.htm" alt="3" rel="nofollow"></map>""",
        ),
        Case(
            """<table style="color: rgb(0, 0, 0);"><tbody><tr><th>Column One</th><th>Column Two</th></tr><tr><td align="center" style="background-color: rgb(255, 255, 254);"><font size="2">Size 2</font></td><td align="center" style="background-color: rgb(255, 255, 254);"><font size="7">Size 7</font></td></tr></tbody></table>""",
            """<table><tbody><tr><th>Column One</th><th>Column Two</th></tr><tr><td align="center">Size 2</td><td align="center">Size 7</td></tr></tbody></table>""",
        ),
        Case(
            """xss<a href="http://www.google.de" style="color:red;" onmouseover=alert(1) onmousemove="alert(2)" onclick=alert(3)>g<img src="http://example.org"/>oogle</a>""",
            """xss<a href="http://www.google.de" rel="nofollow">g<img src="http://example.org"/>oogle</a>""",
        ),
        Case(
            "<table>Hallo\r\n<script>SCRIPT</script>\nEnde\n\r",
            "<table>Hallo\n\nEnde\n\n",
        ),
    ]

    p = UGCPolicy()
    for case in cases:
        assert p.sanitize(case.input) == case.output
