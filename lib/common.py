import re


def get_link_from_query(query):
    m = re.findall("(https?://\S+)", query)
    if len(m) > 0:
        return m[0]
    return None


def validate_query(query):
    return get_link_from_query(query) or re.search("aliexpress", query) or is_digits(query)


def is_digits(query):
    return re.search("^\d+$", query)
