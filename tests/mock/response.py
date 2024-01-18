# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Mock module of HTTP responses for inveniordm-py tests."""

import json
from unittest.mock import MagicMock


class MockResponse(MagicMock):
    """Mocked HTTP response.""" ""

    request = None

    @property
    def data(self):
        """Return the data passed to the request.

        Since we can't mock the API response exactly with all the transformations, the request data is just copied over to the response.
        """
        return self.request.data

    def __init__(self, request, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        self.request = request

    def json(self):
        """Return the data as a dict."""
        if isinstance(self.data, dict):
            dict_data = self.data
        else:
            dict_data = json.loads(self.data)

        # Fake the draft/record id
        dict_data.update({"id": 1})
        return dict_data

    def raise_for_status(self):
        """Mock function."""
        pass
