# -*- coding: utf-8 -*-

import afwf

from .handlers import (
    google_suggest,
)

wf = afwf.Workflow()
wf.register(google_suggest.google_suggest_handler)
wf.register(google_suggest.trans_cn_handler)
wf.register(google_suggest.en_wbs_handler)
wf.register(google_suggest.en_syn_handler)
wf.register(google_suggest.aws_doc_handler)
