
REMOVE_TAGS = {'script', 'style', 'meta', 'noscript'}
KEEP_ATTRS = {'class', 'id', 'name', 'href', 'text', 'src'}

def convert_tag_to_xpath(element):
    components = []
    endpoint = element if element.name else element.parent   # in case of NavigableString
    for tag in reversed((endpoint, *endpoint.parents)[:-1]):  # everything back to <html>; not <DOCSTRING>
        name = f"{tag.prefix}:{tag.name}" if tag.prefix else tag.name
        siblings = tag.parent.find_all(name, recursive=False)
        if len(siblings) != 1:
            idx = next(index for index, sibling in enumerate(siblings, 1) if sibling is tag)
            name += f"[{idx}]"
        components.append(name)
        # components.append(name if len(siblings) == 1 else '%s[%d]' % (name, next(
        #     index for index, sibling in enumerate(siblings, 1)  if sibling is tag)))
        # print(components[-1])
    xpath = "/" + "/".join(components)
    return xpath

#     if len(siblings) != 1: name += f"[{siblings.index(tag)+1}]"
#     components.append(name)
#     # components.append(name if len(siblings) == 1 else '%s[%d]' % (name, next(
#     #     index for index, sibling in enumerate(siblings, 1)  if sibling is tag)))
#     # print(components[-1])
# xpath = "/" + "/".join(components)
# return xpath

def minify_soup(soup, keep_attrs=None, remove_tags=None, remove_empty_tags=False):
    if keep_attrs is None: keep_attrs = KEEP_ATTRS
    if remove_tags is None: remove_tags = REMOVE_TAGS

    # Remove unwanted tags
    for tag in remove_tags: [x.extract() for x in soup.find_all(tag)]
    # Remove unwanted attributes
    for tag in soup():
        for attribute in list(tag.attrs):  # list() because changing during iteration
            if attribute not in keep_attrs: del tag[attribute]
    # Remove empty tags
    if remove_empty_tags:
        for tag in soup.find_all():
            if tag.text.strip() == "": tag.extract()
    return soup
