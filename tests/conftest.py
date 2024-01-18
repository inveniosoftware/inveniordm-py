# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

import pytest

from inveniordm_py import InvenioAPI

from .mock.session import MockSession


@pytest.fixture()
def base_url():
    """Base URL of the REST API."""
    return "https://127.0.0.1"


@pytest.fixture()
def token():
    """Mocked authentication token."""
    return "test"


@pytest.fixture()
def mocked_session():
    """Mock HTTP session used by the client."""
    yield MockSession()


@pytest.fixture()
def client(base_url, token, mocked_session):
    """Inveniordm REST API client."""
    return InvenioAPI(base_url, token, session=mocked_session)
