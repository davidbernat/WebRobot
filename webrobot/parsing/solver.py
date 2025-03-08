from webrobot.parsing.utils import convert_tag_to_xpath
from webrobot.parsing.HtmlNode import HtmlNode
import dataclasses
import re

@dataclasses.dataclass
class XNode:
    name: str
    classes: list[str]
    get_attrs: str | list[str]
    expect_one: bool
    # include index
    # add xpath

    @staticmethod
    def from_tag(tag, get_attrs=None, expect_one=False):
        return XNode(name=tag.name, classes=tag.get("class", []), get_attrs=get_attrs, expect_one=expect_one)


BUTTON_TAGS = ["button", "a"]
BUTTON_ATTRS = ["onclick"]

class Solver:

    @staticmethod
    def find_text(soup, to_find, sep=" ", is_button=False, exact=False, expect_one=False):
        # This uses sep=" " and will fail for various niggling space issues; i.e., before .replace("  ", " ") this would
        # created "text1  text2" for a tag inside two tags e.g., um need an example "By  Charles".
        found = []
        for tag in soup.find_all():
            if is_button:
                # to be a button the element must either be a BUTTON_TAGS or have one of the BUTTON_ATTR attributes.
                if tag.name not in BUTTON_TAGS and not any([tag.has_attr(a) for a in BUTTON_ATTRS]): continue
            # this will find all paths (/html/body /html/body/div ...) so pruning has to happen after.
            in_tag_text = tag.get_text(separator=sep).lower()
            in_tag_text = re.sub(sep + sep, sep, in_tag_text).strip()
            if exact and to_find.lower() == in_tag_text: found.append(tag)
            elif not exact and to_find.lower() in in_tag_text: found.append(tag)
        if expect_one:
            if len(found) != 1: raise RuntimeError(f"expect_one and found={found}")
            else: found = found[0]  # do not return list
        return found

    @staticmethod
    def prune_to_leaves(found):
        # for the sake of print/log simplicity we will work in xpaths
        # this for loop seems contrived; don't bother sorting
        to_remove = []
        xpaths = [convert_tag_to_xpath(tag).split("/") for tag in found]
        for xpath in xpaths:
            parents_xpath = [xpath[:i] for i in range(len(xpath))]
            for parent_xpath in parents_xpath:
                if parent_xpath in xpaths: to_remove.append(xpaths.index(parent_xpath))
        found = [f for i, f in enumerate(found) if i not in to_remove]  # most root path
        [print(convert_tag_to_xpath(tag)) for tag in found]
        return found

    @staticmethod
    def reduce_to_node(tag, get_attrs="__TEXT", expect_one=False):
        _type, _classes = tag.name, tag.get("class", [])
        return HtmlNode(_type, _classes, get_attrs=get_attrs, expect_one=expect_one)

    @staticmethod
    def reduce_from_xnode(xnode):
        return HtmlNode(xnode.name, xnode.classes, get_attrs=xnode.get_attrs, expect_one=xnode.expect_one)


# now, convert this to a rule; needs to know trunk of closest match across groupings?
# do not need to do that until there are multiple matches; and anyway, how to determine "class" etc
# without having a high-level instruction e.g. "there should be many" i.e., listify.
# so, probably only a few use cases: "list of objects", "is clickable", etc. to add later.
# for is_list, trying to think through when classes are different etc but this is straightforward

# def generate_candidate_specific_nodes(tag):
#     # generation n choose m combinations of _classes
#     # consider trunk upward.
#     # in separate class will select the most specific as long as extractions are equal.
#     # need to prompt user when extractions are not equal, and/or default to 'most'
#     return :)

