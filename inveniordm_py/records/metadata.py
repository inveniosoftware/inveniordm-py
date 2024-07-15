# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record metadata classes."""
import json

from inveniordm_py.metadata import ListMetadata, Metadata


class RecordMetadata(Metadata):
    """Record metadata class."""

    accept = "application/json"
    content_type = "application/json"

    @property
    def endpoint_kwargs(self):
        """Return endpoint kwargs.""" ""
        return {"id_": self._data["id"]}


class DraftMetadata(Metadata):
    """Draft metadata class."""

    accept = "application/vnd.inveniordm.v1+json"
    content_type = "application/json"

    @property
    def endpoint_kwargs(self):
        """Return endpoint kwargs.""" ""
        return {"id_": self._data["id"]}


class RecordListMetadata(ListMetadata):
    """Record list metadata class."""

    accept = "application/vnd.inveniordm.v1+json"
    item_class = RecordMetadata


class RecordCommunityMetadata(Metadata):
    """Record community metadata class."""

    accept = "application/json"
    content_type = "application/json"

    def _serialize_data(self):
        """Serialize community data to InvenioRDM format."""
        _data = self._data.get("communities", [])
        if not _data:
            return {}

        req = {"communities": []}
        if isinstance(_data, list):
            req["communities"] = [{"id": id_} for id_ in _data]
        elif isinstance(_data, str):
            req["communities"] = [{"id": _data}]
        else:
            raise ValueError(
                f"Invalid data type for community metadata. Expected: list or str. Got: {type(_data)}"
            )
        return req

    def to_request(self):
        """Convert metadata to request body."""
        return json.dumps(self._serialize_data())


class RecordCommunitiesListMetadata(ListMetadata):
    """Record communities list metadata class."""

    item_class = RecordCommunityMetadata
