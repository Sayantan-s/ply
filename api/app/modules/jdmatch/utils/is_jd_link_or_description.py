import re


def is_jd_link_or_description(text: str) -> bool:
    url_regex = r"^(https?://)?([\w-]+\.)+[\w-]+(/[\w\-._~:/?#\[\]@!$&'()*+,;=]*)?$"
    return bool(re.match(url_regex, text.strip(), re.IGNORECASE))
