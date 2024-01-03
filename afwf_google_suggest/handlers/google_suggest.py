# -*- coding: utf-8 -*-

import typing as T
from urllib import request
import xml.etree.ElementTree as ET

import attrs
import afwf.api as afwf

from ..cache import cache


def http_get(url: str) -> str:
    """
    Get html content from url.
    """
    with request.urlopen(url) as response:
        return response.read().decode("utf-8")


CACHE_EXPIRE = 3600


def url_encode(query: str) -> str:
    return "+".join([word.strip() for word in query.split(" ") if word.strip()])


google_suggest_endpoint = (
    "https://www.google.com/complete/search?output=toolbar&q={query}"
)


def _get_suggestion_list(query: str) -> T.List[str]:
    """
    Get google suggest list from google suggest endpoint.
    """
    url = google_suggest_endpoint.format(query=query)
    html = http_get(url)
    root = ET.fromstring(html)
    suggestion_list = list()
    for suggestion in root.iter("suggestion"):
        suggestion_list.append(suggestion.attrib["data"])
    return suggestion_list


def get_suggestion_list(query: str) -> T.List[str]:
    """
    wrapper of :func:`_get_suggestion_list`, with cache.
    """
    url_safe_query = url_encode(query)
    if url_safe_query in cache:
        return cache[url_safe_query]
    else:
        suggestion_list = _get_suggestion_list(url_safe_query)
        cache.set(url_safe_query, suggestion_list, expire=CACHE_EXPIRE)
        return suggestion_list


@attrs.define
class Handler(afwf.Handler):
    search_url_template: str = attrs.field()
    subtitle_template: str = attrs.field()

    def main(self, query: str) -> afwf.ScriptFilter:
        suggestion_list = get_suggestion_list(query)
        sf = afwf.ScriptFilter()
        for suggestion in suggestion_list:
            url_safe_query = suggestion.replace(" ", "+")
            google_search_url = self.search_url_template.format(query=url_safe_query)
            item = afwf.Item(
                uid=suggestion,
                title=suggestion,
                subtitle=self.subtitle_template.format(suggestion=suggestion),
                arg=suggestion,
                autocomplete=suggestion,
            ).open_url(google_search_url)
            sf.items.append(item)
        return sf

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        new_query = "+".join([s for s in query.split(" ") if s.strip()])
        return dict(query=new_query)


google_suggest_handler = Handler(
    id="google_suggest",
    search_url_template="https://www.google.com/search?q={query}",
    subtitle_template="Search Google For {suggestion}",
)
trans_cn_handler = Handler(
    id="trans_cn",
    search_url_template="https://translate.google.com/?sl=en&tl=zh-CN&text={query}&op=translate",
    subtitle_template="Translate '{suggestion}' to zh-CN",
)
en_wbs_handler = Handler(
    id="en_wbs",
    search_url_template="https://www.merriam-webster.com/dictionary/{query}",
    subtitle_template="Search '{suggestion}' in merriam-webster.com",
)
en_syn_handler = Handler(
    id="en_syn",
    search_url_template="https://www.thesaurus.com/browse/{query}",
    subtitle_template="Find Synonyms or Antonyms for '{suggestion}'",
)
aws_doc_handler = Handler(
    id="aws_doc",
    search_url_template="https://docs.aws.amazon.com/search/doc-search.html?searchPath=documentation&searchQuery={query}",
    subtitle_template="Search AWS Doc for '{suggestion}'",
)
