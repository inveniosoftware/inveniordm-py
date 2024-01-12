# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base metadata class."""

import json

class Metadata:
    accept = ""
    content_type = ""

    @classmethod
    def from_response(cls, response):
        data = response.json()
        return cls(**data)

    @property
    def endpoint_kwargs(self):
        raise NotImplementedError

    def to_request(self):
        return json.dumps(self._data)

    def __init__(self, **data):
        self._data = data

    def __getitem__(self, key):
        self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value


class ListMetadata(Metadata):
    item_class = None

    @property
    def hits(self):
        return [self.item_class(**h) for h in self._data['hits']['hits']]

    @property
    def total(self):
        return self._data['hits']['total']

    @property
    def aggregations(self):
        return self._data['aggregations']
