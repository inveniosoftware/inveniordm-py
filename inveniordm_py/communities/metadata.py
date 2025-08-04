# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Community metadata classes."""

import json

from inveniordm_py.metadata import ListMetadata, Metadata


class CommunityMetadata(Metadata):
    """Community metadata."""

    accept = "application/json"
    content_type = "application/json"

    @property
    def endpoint_kwargs(self):
        """Return endpoint kwargs.""" ""
        return {"id_": self._data["id"]}


class CommunityListMetadata(ListMetadata):
    """Metadata of a list of files."""

    accept = "application/json"
    content_type = "application/json"

    item_class = CommunityMetadata

    def __init__(self, data=None, **kwargs):
        """Initialize metadata object.

        The data is either explicitly passed (i.e. top-level parameters) or taken from keyword arguments.

        .. note:: this is a bit of a hack, but it works for now.
        """
        if data:
            self._data = data
        if kwargs:
            self._data = kwargs

    @property
    def endpoint_kwargs(self):
        """Return endpoint kwargs.""" ""
        return {}


class CommunityRecordMetadata(Metadata):
    """Community record metadata class."""

    accept = "application/json"
    content_type = "application/json"

    def _serialize_data(self):
        """Serialize community data to InvenioRDM format."""
        _data = self._data.get("records", [])
        if not _data:
            return {}

        req = {"records": []}
        if isinstance(_data, list):
            req["records"] = [{"id": id_} for id_ in _data]
        elif isinstance(_data, str):
            req["records"] = [{"id": _data}]
        else:
            raise ValueError(
                f"Invalid data type for community record metadata. Expected: list or str. Got: {type(_data)}"
            )
        return req

    def to_request(self):
        """Convert metadata to request body."""
        return json.dumps(self._serialize_data())


class CommunityRecordListMetadata(ListMetadata):
    """Community record list metadata class."""

    item_class = CommunityRecordMetadata

    accept = "application/json"
    content_type = "application/json"
