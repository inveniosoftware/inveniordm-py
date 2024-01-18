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

    accept = "application/vnd.inveniordm.v1+json"
    content_type = "application/vnd.inveniordm.v1+json"

    @property
    def endpoint_kwargs(self):
        """Return endpoint kwargs for a file, namely the filename."""
        return {"filename": self._data["filename"]}


class FilesListMetadata(ListMetadata):
    """Metadata of a list of files."""

    accept = "application/vnd.inveniordm.v1+json"

    item_class = FileMetadata


class Stream:
    """Stream metadata."""

    accept = "application/octet-stream"
