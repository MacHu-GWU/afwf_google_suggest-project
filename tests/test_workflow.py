# -*- coding: utf-8 -*-

from afwf_google_suggest.workflow import wf
from afwf_google_suggest.handlers import (
    google_suggest,
)
from rich import print as rprint


def test():
    sf = wf._run(arg=f"{google_suggest.google_suggest_handler.id} tesla")


if __name__ == "__main__":
    from afwf_google_suggest.tests import run_cov_test

    run_cov_test(__file__, "afwf_google_suggest.workflow", preview=False)
