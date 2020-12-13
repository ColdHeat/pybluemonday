from pybluemonday import UGCPolicy
import psutil


def test_memory_leak_in_sanitization():
    process = psutil.Process()
    previous_memory = process.memory_info().rss

    TEST = """
<html>
    <head>
    <script type="text/javascript" src="evil-site"></script>
    <link rel="alternate" type="text/rss" src="evil-rss">
    <style>
        body {background-image: url(javascript:do_evil)};
        div {color: expression(evil)};
    </style>
    </head>
    <body onload="evil_function()">
    <!-- I am interpreted for EVIL! -->
    <a href="javascript:evil_function()">a link</a>
    <a href="#" onclick="evil_function()">another link</a>
    <p onclick="evil_function()">a paragraph</p>
    <div style="display: none">secret EVIL!</div>
    <object> of EVIL! </object>
    <iframe src="evil-site"></iframe>
    <form action="evil-site">
        Password: <input type="password" name="password">
    </form>
    <blink>annoying EVIL!</blink>
    <a href="evil-site">spam spam SPAM!</a>
    <image src="evil!">
    </body>
</html>"""

    p = UGCPolicy()
    for x in range(300000):
        p.sanitize(TEST)

    process = psutil.Process()
    new_memory = process.memory_info().rss
    assert new_memory < (previous_memory * 2)
