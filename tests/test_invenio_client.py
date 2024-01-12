# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

token = "85dTFUIcoomyTWy9jGNnz5yZ0vPCMmvNDw0M2G8nslGtTwAKJG7TNkxlkRiP"

from inveniordm_py import InvenioAPI

client = InvenioAPI('https://sandbox.zenodo.org/api', token)

res = client.records.search()

for r in res:
    r.versions


client.records.create()
client.records('1234').files.download()


r = client.records('1234').get()

r.data
r.versions.latest()
