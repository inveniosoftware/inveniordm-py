# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Inveniordm-py is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Test client for drafts."""

from inveniordm_py.records.metadata import DraftMetadata
from inveniordm_py.records.resources import Draft, Record


def test_create_empty(client):
    """Test case for creating an empty draft."""
    draft = client.records.create()
    assert draft
    assert isinstance(draft, Draft)
    assert draft.data is not None
    assert draft.data["id"] is not None


def test_create_with_data(client):
    """Test case for creating a draft with data."""
    data = {"title": "Test", "creators": [{"name": "Test"}]}
    draft = client.records.create(data=DraftMetadata(**data))
    assert draft
    assert isinstance(draft, Draft)
    assert draft.data is not None
    assert draft.data["id"] is not None


def test_update(client):
    """Test case for updating a draft.

    First creates an empty draft and updates its metadata afterwards.
    """
    draft = client.records.create()
    assert draft
    data = {"title": "Test", "creators": [{"name": "Test"}]}
    draft.update(data=DraftMetadata(**data))
    assert draft.data is not None
    assert draft.data["id"] is not None


def test_publish(client):
    """Test case for publishing a draft."""
    draft = client.records.create()
    assert draft
    data = {"title": "Test", "creators": [{"name": "Test"}]}
    draft.update(data=DraftMetadata(**data))
    assert draft.data is not None
    assert draft.data["id"] is not None
    record = draft.publish()
    assert isinstance(record, Record)
    assert record.data is not None
    assert record.data["id"] is not None


def test_delete(client):
    pass
