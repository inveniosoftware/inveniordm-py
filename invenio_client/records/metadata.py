# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record metadata classes."""

from ..metadata import ListMetadata, Metadata


class RecordMetadata(Metadata):
    accept = "application/vnd.inveniordm.v1+json"
    content_type = "application/vnd.inveniordm.v1+json"

    @property
    def endpoint_kwargs(self):
        return {'id_': self._data['id']}


class DraftMetadata(Metadata):
    accept = "application/vnd.inveniordm.v1+json"
    content_type = "application/vnd.inveniordm.v1+json"

    @property
    def endpoint_kwargs(self):
        return {'id_': self._data['id']}


class RecordListMetadata(ListMetadata):
    accept = "application/vnd.inveniordm.v1+json"
    item_class = RecordMetadata
