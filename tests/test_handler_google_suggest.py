# -*- coding: utf-8 -*-

from afwf_google_suggest.handlers.google_suggest import google_suggest_handler


def test():
    sf = google_suggest_handler.main(query="tesla")
    for item in sf.items:
        assert "tesla" in item.title


if __name__ == "__main__":
    from afwf_google_suggest.tests import run_cov_test

    run_cov_test(__file__, "afwf_google_suggest.handlers.google_suggest", preview=False)
