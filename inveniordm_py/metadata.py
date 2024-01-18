# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base metadata class."""

import json


class Metadata:
    """Base metadata class."""

    accept = ""
    content_type = ""

    @classmethod
    def from_response(cls, response):
        """Create metadata object from response."""
        data = response.json()
        return cls(**data)

    @property
    def endpoint_kwargs(self):
        """Endpoint kwargs, delegated to the implementation."""
        raise NotImplementedError

    def to_request(self):
        """Convert metadata to request body (JSON)."""
        return json.dumps(self._data)

    def __init__(self, **data):
        """Initialize metadata object."""
        self._data = data

    def __getitem__(self, key):
        """Get item from metadata."""
        return self._data[key]

    def __setitem__(self, key, value):
        """Set item in metadata."""
        self._data[key] = value

    def __eq__(self, value) -> bool:
        """Compare two metadata objects.

        Two metadata objects are equal if their data is equal.
        """
        return value == self._data


class ListMetadata(Metadata):
    """List metadata class."""

    item_class = None

    @property
    def hits(self):
        """List of hits."""
        return [self.item_class(**h) for h in self._data["hits"]["hits"]]

    @property
    def total(self):
        """Total number of hits."""
        return self._data["hits"]["total"]

    @property
    def aggregations(self):
        """Search aggregations."""
        return self._data["aggregations"]
