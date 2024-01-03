# -*- coding: utf-8 -*-

from afwf_google_suggest.workflow import wf
from afwf_google_suggest.handlers import (
    google_suggest,
    memorize_cache,
    open_file,
    open_url,
    read_file,
    set_settings,
    view_settings,
    write_file,
)
from rich import print as rprint


def test():
    sf = wf._run(arg=f"{memorize_cache.handler.id} my_key")


if __name__ == "__main__":
    from afwf_google_suggest.tests import run_cov_test

    run_cov_test(__file__, "afwf_google_suggest.workflow", preview=False)
