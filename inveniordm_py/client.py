# SPDX-FileCopyrightText: 2024 CERN.
# SPDX-License-Identifier: MIT

"""Invenio REST API client.."""

import atexit

from requests import Session

from .communities.community import CommunityList
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

    @property
    def communities(self):
        """Get a community list resource."""
        return CommunityList(client=self)
