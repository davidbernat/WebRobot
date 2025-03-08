from webrobot.parsing.utils import convert_tag_to_xpath

class SoupHelpers:

    @staticmethod
    def get_attr(tag, key, if_not_exists=None):
        """tag is not a dictionary; so does not have tag.get(key); so this makes retrieval easier and without throws"""
        return tag.attrs[key] if tag.has_attr(key) else if_not_exists

    @staticmethod
    def find_shared_parent(tag1, tag2):
        parents1 = list(tag1.parents) + [tag1,]  # the common node may be itself with the other tag as its child
        parents2 = list(tag2.parents) + [tag2,]
        common_parents = [p for p in parents1 if p in parents2]
        if len(common_parents) == 0: return None
        common_parents = sorted(common_parents, key=lambda c: len(list(c.parents)), reverse=True)
        return common_parents[0]

    # now, we have an absurdly N1 x N2 x N3 x N4 search to identify whether (all?) sets of four match in the same roots?
    # although we know that all of them will meet in the html/body root, so we want the longest root for any of the sets.
    # but 1. how do we know only the longest root counts (an assumption of the 'is list' constraint) and how do we minimize
    # the search space?
    @staticmethod
    def find_shared_parent_of_collections(lists_of_compare):
        # Yes, I know I could make this one recursive groups but I do not feel like that right now
        def find_shared_parent_of_tag_against_collections(tag1, _lists_of_compares):
            if isinstance(_lists_of_compares, (list, tuple)):
                if len(_lists_of_compares) == 0: return None
                if len(_lists_of_compares) != 1:
                    common = find_shared_parent_of_tag_against_collections(tag1, [_lists_of_compares[0]])
                    return find_shared_parent_of_tag_against_collections(common, _lists_of_compares[1:])  # this looks correct
            lists_of_compares = _lists_of_compares[0]
            commons = [SoupHelpers.find_shared_parent(tag1, t) for t in lists_of_compares]  # find longest comparison of the available to_compare
            if len(commons) == 0: return None
            depths = [len(list(c.parents)) for c in commons]
            idx = depths.index(max(depths))  # yes, throw away when there are equal depths, i.e,. multiple lists composite
            print(convert_tag_to_xpath(commons[idx]))
            return commons[idx]

        if len(lists_of_compare) <= 1: return None
        bests = [find_shared_parent_of_tag_against_collections(tag, lists_of_compare[1:]) for tag in lists_of_compare[0]]
        depths = [len(list(c.parents)) for c in bests]
        idx = depths.index(max(depths))  # yes, throw away when there are equal depths, i.e,. multiple lists composite
        return bests[idx]



