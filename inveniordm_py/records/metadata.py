# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record metadata classes."""

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
