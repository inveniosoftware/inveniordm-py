# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-RDM is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Mock session."""

from unittest.mock import MagicMock

from .request import MockRequest
from .response import MockResponse


class MockSession(MagicMock):
    """Mock session."""

    def post(self, *args, **kwargs):
        """Mock post method."""
        req = MockRequest(data=kwargs.get("data"), headers=kwargs.get("headers"))
        return MockResponse(request=req)

    def put(self, *args, **kwargs):
        """Mock put method."""
        req = MockRequest(data=kwargs.get("data"), headers=kwargs.get("headers"))
        return MockResponse(request=req)
