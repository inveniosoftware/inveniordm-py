# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Mock module of HTTP responses for inveniordm-py tests."""

import re
from unittest.mock import MagicMock

from .handlers import DraftFileHandler, DraftFilesHandler, RecordsListHandler


class MockResponse(MagicMock):
    """Mocked HTTP response.""" ""

    HANDLERS = {
        r"records/[0-9]+/draft/files": DraftFilesHandler,
        r"records/[0-9]+/draft/files/filename": DraftFileHandler,
        r"records": RecordsListHandler,
    }

    request = None

    def _match_handler(self, request):
        for pattern, handler in self.HANDLERS.items():
            endpoint = request.url.split("/", 3)[3]
            if re.match(pattern, endpoint):
                return handler()
        raise ValueError(f"No handler found for endpoint {request.url}")

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
        """Return the JSON response.

        The request is handled by the appropriate handler, which returns the data as a JSON.
        """
        match_handler = self._match_handler(self.request)
        return match_handler.handle(self.request)

    def raise_for_status(self):
        """Mock function."""
        pass
