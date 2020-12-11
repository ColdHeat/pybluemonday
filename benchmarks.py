from bleach.sanitizer import Cleaner as BleachSanitizer
from html_sanitizer import Sanitizer as HTMLSanitizerSanitizer

from pybluemonday import UGCPolicy as BlueMondaySanitizer

# Snipppet from https://lxml.de/lxmlhtml.html#cleaning-up-html
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

BLUE_MONDAY = BlueMondaySanitizer()
HTML_SANITIZER = HTMLSanitizerSanitizer()
BLEACH_SANITIZER = BleachSanitizer()


def test_bleach():
    BLEACH_SANITIZER.clean(TEST)


def test_html_sanitizer():
    HTML_SANITIZER.sanitize(TEST)


def test_bluemonday():
    BLUE_MONDAY.sanitize(TEST)


if __name__ == "__main__":
    import timeit

    print(
        "bleach (20000 sanitizations):",
        timeit.timeit("test_bleach()", globals=locals(), number=20000),
    )
    print(
        "html_sanitizer (20000 sanitizations):",
        timeit.timeit("test_html_sanitizer()", globals=locals(), number=20000),
    )
    print(
        "bluemonday (20000 sanitizations):",
        timeit.timeit(
            "test_bluemonday()",
            globals=locals(),
            number=20000,
        ),
    )
