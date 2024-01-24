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
        """Initialize metadata object.

        The data is either explicitely passed (i.e. top-level parameters) or taken from keyword arguments.

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
    """Outgoing stream metadata.

    This is used to upload a file.
    """

    content_type = "application/octet-stream"
    accept = "application/json"


class IncomingStream(Stream):
    """Incoming stream metadata.

    This is used to download a file.
    """

    content_type = None
    accept = None
