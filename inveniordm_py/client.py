# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio REST API client.."""

import atexit

from requests import Session

from .records.resources import RecordList


class InvenioAPI:
    """InvenioRDM REST API client."""

    def __init__(self, base_url, access_token, session=None):
        """Initialize client."""
        from inveniordm_py import __version__

        self._base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self._access_token = access_token
        self.session = session or Session()
        atexit.register(self.session.close)
        self.session.headers["User-Agent"] = f"Invenio API Client/{__version__}"
        self.session.headers["Authorization"] = f"Bearer {self._access_token}"

    @property
    def records(self):
        """Get a record list resource."""
        return RecordList(client=self)
