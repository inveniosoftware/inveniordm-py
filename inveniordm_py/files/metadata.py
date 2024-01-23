# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record metadata classes."""

from inveniordm_py.metadata import ListMetadata, Metadata


class FileMetadata(Metadata):
    """File metadata."""

    accept = "application/json"
    content_type = "application/json"

    @property
    def endpoint_kwargs(self):
        """Return endpoint kwargs for a file, namely the filename."""
        return {"key": self._data["key"]}


class FilesListMetadata(ListMetadata):
    """Metadata of a list of files."""

    accept = "application/json"
    content_type = "application/json"

    item_class = FileMetadata

    def __init__(self, data=None, **kwargs):
        # TODO for outgoing requests, we need to pass a top-level argument which is an array.
        # TODO for incoming, we receive an object with a key "entries" which is an array.
        if data:
            self._data = data
        if kwargs:
            self._data = kwargs

    @property
    def endpoint_kwargs(self):
        """Return endpoint kwargs.""" ""
        return {}


class Stream(FileMetadata):
    """Stream metadata."""

    def to_request(self):
        """Return the stream data."""
        return self._data

    @classmethod
    def from_response(cls, response):
        """Create metadata object from response."""
        yield response.content


class OutgoingStream(Stream):
    content_type = "application/octet-stream"
    accept = "application/json"


class IncomingStream(Stream):
    content_type = None
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*"
