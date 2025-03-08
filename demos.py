from webrobot.parsing.utils import minify_soup, convert_tag_to_xpath
from webrobot.parsing.HtmlNode import HtmlNode
from webrobot.parsing.SoupHelpers import SoupHelpers
from webrobot.parsing.solver import Solver
from bs4 import BeautifulSoup

# invert from text in node to xpath equivalent; then find others that match
# import yfinance as yf
# dat = yf.Ticker("MSFT")

filename = "blow.html"
with open(filename, "r") as f: html = f.read()

soup = BeautifulSoup(html)
soup = minify_soup(soup)

search = "societal sickness"

# found = Solver.find_text(soup, search)
# found = Solver.prune_to_leaves(found)
#
# for tag in found:
#     node = Solver.reduce_to_node(tag)
#     extractions = node.parse(soup)
#     print(extractions)
# print()



# collection = [
#     "Sonya Massey’s Killing Is Black America’s Sorrow",
#     "Her death is the manifestation of a societal sickness that devalues Black life.",
#     "By Charles M. Blow",
#     "July 31, 2024"
# ]

# founds = [Solver.prune_to_leaves(Solver.find_text(soup, c)) for c in collection]
# best = SoupHelpers.find_shared_parent_of_collections(founds)
# pruned = [[c for c in f if best in c.parents] for f in founds]

collection = dict(
    headline=dict(text="Sonya Massey’s Killing Is Black America’s Sorrow", attrs=["__TEXT", "href"]),
    subtitle="Her death is the manifestation of a societal sickness that devalues Black life.",
    author="Charles M. Blow",
    published="July 31, 2024",
)

# works okay; is clunky because: 1. needs to "have href" if asked i.e., a not h1; also the [ ] is complicated
# so asser that pruned is length one. I think I should post this minute the dict() version to github tomorrow.
keys = list(collection.keys())
texts = [collection[key] if isinstance(collection[key], str) else collection[key]["text"] for key in keys]
attrs = ["__TEXT" if isinstance(collection[key], str) else collection[key]["attrs"] for key in keys]
founds = [Solver.prune_to_leaves(Solver.find_text(soup, t)) for t in texts]
best = SoupHelpers.find_shared_parent_of_collections(founds)
pruned = [[c for c in f if best in c.parents] for f in founds]

blocks = Solver.reduce_to_node(best, get_attrs=None).parse(soup)
data = [{key: [Solver.reduce_to_node(p, get_attrs=attrs[i], expect_one=True).parse(b) for p in pruned[i]] \
         for i, key in enumerate(keys)} \
        for b in blocks]

print("\n", convert_tag_to_xpath(best))
print()
# last step is to make the root node; then find each of the 'founds' that are within it; make those nodes too.
# and also to get the url of the content; really should just pass [__TEXT, href] into that.
# headline = HtmlNode("h1", "e1h9rw200", get_attrs="__TEXT", expect_one=True),

print()