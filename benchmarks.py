"""
Install the following dependencies:

html-sanitizer==1.9.1
bleach==3.2.1
lxml==4.6.2
html5lib==1.1
"""

from bleach.sanitizer import Cleaner as BleachSanitizer
from html_sanitizer import Sanitizer as HTMLSanitizerSanitizer
from lxml.html import html5parser, tostring
from lxml.html.clean import Cleaner
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
LXML_SANITIZER = Cleaner()


def test_bleach():
    BLEACH_SANITIZER.clean(TEST)


def test_html_sanitizer():
    HTML_SANITIZER.sanitize(TEST)


def test_lxml_sanitizer():
    LXML_SANITIZER.clean_html(TEST)


def test_bluemonday():
    BLUE_MONDAY.sanitize(TEST)


if __name__ == "__main__":
    import timeit

    x = [
        "bleach",
        "html_sanitizer",
        "lxml Cleaner",
        "pybluemonday",
    ]

    y = [
        timeit.timeit("test_bleach()", globals=locals(), number=20000),
        timeit.timeit("test_html_sanitizer()", globals=locals(), number=20000),
        timeit.timeit("test_lxml_sanitizer()", globals=locals(), number=20000),
        timeit.timeit("test_bluemonday()", globals=locals(), number=20000,),
    ]

    for name, result in list(zip(x, y)):
        print(name, "(20000 sanitizations):", result)

    import seaborn as sns
    import matplotlib.pyplot as plt

    chart = sns.barplot(x=x, y=y)
    chart.set_title("Time Taken to Sanitize HTML (20000 iterations, lower is better)")
    chart.set_xlabel("Library")
    chart.set_ylabel("Time (seconds)")
    for p in chart.patches:
        chart.annotate(
            f"{round(p.get_height(), 2)} s",
            (p.get_x() + 0.4, p.get_height()),
            ha="center",
            va="bottom",
            color="black",
        )
    plt.show()
