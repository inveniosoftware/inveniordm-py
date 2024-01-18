# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

# from inveniordm_py import InvenioAPI


# def test_client(token, base_url, mocked_session):
#     client = InvenioAPI(base_url, token, session=mocked_session)

#     res = client.records.search()

#     for r in res:
#         r.versions

#     client.records.create()
#     # client.records("1234").files.download() # TODO uncomment when files are implemented

#     r = client.records("1234").get()

#     assert r.data is not None
#     assert r.versions.latest() is not None
