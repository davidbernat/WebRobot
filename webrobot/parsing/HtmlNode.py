from webrobot.parsing.SoupHelpers import SoupHelpers


class HtmlNode:

    def __init__(self, tag, classes=None, has_attrs=None, get_attrs=None, expect_one=False):
        if classes is None: classes = []
        if not isinstance(classes, (tuple, list)): classes = [classes]
        if has_attrs is None: has_attrs = dict()
        if get_attrs is None: get_attrs = None  # implies to return the element itself
        self.tag = tag
        self.classes = classes
        self.has_attrs = has_attrs
        self.get_attr = get_attrs
        self.expect_one = expect_one  # this is a lame hack that I would not use in production; when only one result is
        # expected, i.e. "headline" I want the result returned as a string not [string].
        # it also serves weakly as a data integrity check; but better solutions exist.

    def parse(self, tree):
        results = []
        matching = tree.find_all(self.tag, class_=self.classes)
        if len(matching) == 0: return []
        if self.expect_one and len(matching) != 1:
            raise RuntimeError(f"more tags than expected found={matching}")
        for tag in matching:
            if any([SoupHelpers.get_attr(tag, key) != value for key, value in self.has_attrs]): continue
            if self.get_attr is None:
                results.append(tag)  # return the tag itself
            else:
                to_gets = self.get_attr
                is_one = isinstance(to_gets, str)  # convenience to return value rather than [value] when is str
                if is_one: to_gets = [to_gets]
                if not isinstance(to_gets, (tuple, list)): raise ValueError(f"{to_gets} is not a list, str, or None")
                result = [tag.get_text(" ") if to_get == "__TEXT" else SoupHelpers.get_attr(tag, to_get) for to_get in to_gets]
                if is_one: result = result[0]
                results.append(result)
        return results[0] if self.expect_one else results  # this is also lame
