from pybluemonday import UGCPolicy

HTML = """
<div class="row">
    <div class="col-md-6 offset-md-3" yeet="asdf">
        <img yeet="asdf" class="w-100 mx-auto d-block" style="max-width: 500px;padding: 50px;padding-top: 14vh;" src="themes/core/static/img/logo.png" />
        <h3 class="text-center">
            <p>A cool CTF platform from <a href="https://ctfd.io">ctfd.io</a></p>
            <p>Follow us on social media:</p>
            <a href="https://twitter.com/ctfdio"><i class="fab fa-twitter fa-2x" aria-hidden="true"></i></a>&nbsp;
            <a href="https://facebook.com/ctfdio"><i class="fab fa-facebook fa-2x" aria-hidden="true"></i></a>&nbsp;
            <a href="https://github.com/ctfd"><i class="fab fa-github fa-2x" aria-hidden="true"></i></a>
        </h3>
        <table test="asdf">
            <thead test="fdsa">
                <select>
                    <option>asdf</option>
                </select>
            </thead>
        </table>
        <br>
        <h4 class="text-center">
            <a href="admin">Click here</a> to login and setup your CTF
        </h4>
    </div>
</div>
"""

s = UGCPolicy()
# s.AllowElements("select", "option")
# s.AllowAttrs("class").OnElements("div", "img")
s.AllowAttrs("class", "style").Globally()
# s.AllowAttrsGlobally(attrs=["class", "style"])
# s.AllowAttrsOnElements(attrs=["yeet"], elements=["div"])
# s.AllowAttrsOnElementsMatching(attrs=["test"], regex="^table$")
s.AddTargetBlankToFullyQualifiedLinks(True)
print(s.sanitize(HTML))
