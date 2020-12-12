from pybluemonday import UGCPolicy


def test_02_a_tag():
    entries = (
        ('<a href="/foo">foo</a>', None),
        (
            '<a href="/foo" name="bar" target="some" title="baz" cookies="yesplease">foo</a>',
            '<a href="/foo" name="bar" target="some" title="baz">foo</a>',
        ),
        ('<a href="http://somewhere.else">foo</a>', None),
        ('<a href="https://somewhere.else">foo</a>', None),
        # These test cases don't pass because bluemonday strips the link entirely
        # ('<a href="javascript:alert()">foo</a>', '<a href="#">foo</a>'),
        # ('<a href="javascript%3Aalert()">foo</a>', '<a href="#">foo</a>'),
        ('<a href="mailto:foo@bar.com">foo</a>', None),
        ('<a href="tel:1-234-567-890">foo</a>', None),
    )

    p = UGCPolicy()
    p.RequireNoFollowOnLinks(False)
    p.AllowAttrs("name", "target").OnElements("a")
    p.AllowURLSchemes("tel")

    for before, after in entries:
        after = before if after is None else after
        assert p.sanitize(before) == after
