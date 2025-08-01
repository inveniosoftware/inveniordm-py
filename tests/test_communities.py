# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Inveniordm-py is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Test client for communities."""

from inveniordm_py.communities.community import Community, CommunityRecordList
from inveniordm_py.communities.metadata import CommunityMetadata


def test_search(client):
    """Test case for searching a community"""
    communities = client.communities.search("test")
    assert communities


def test_create_empty(client):
    """Test case for creating an empty draft."""
    community = client.communities.create()
    assert community
    assert isinstance(community, Community)
    assert community.data is not None
    assert community.data["id"] is not None


def test_create_with_data(client):
    """Test case for creating a community with data."""
    data = {"title": "Test", "organizations": [{"name": "CERN"}]}
    community = client.communities.create(data=CommunityMetadata(**data))
    assert community
    assert isinstance(community, Community)
    assert community.data is not None
    assert community.data["id"] is not None


def test_update(client):
    """Test case for updating a draft.

    First creates an empty community and updates its metadata afterwards.
    """
    community = client.communities.create()
    assert community
    data = {"title": "My Community", "organizations": [{"name": "CERN"}]}
    community.update(data=CommunityMetadata(**data))
    assert community.data is not None
    assert community.data["id"] is not None
    assert community.data["metadata"] is not None


def test_community_record(client):
    """Test case for community records"""
    community = client.communities.create()
    assert community
    records = community.records
    assert records
    assert isinstance(records, CommunityRecordList)
