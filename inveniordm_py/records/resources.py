# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record resources."""

from functools import partial

from inveniordm_py.files.metadata import (
    FileMetadata,
    FilesListMetadata,
    IncomingStream,
    OutgoingStream,
)
from inveniordm_py.records.metadata import (
    DraftMetadata,
    RecordListMetadata,
    RecordMetadata,
)
from inveniordm_py.resources import Resource


class Record(Resource):
    """Implements a Record as a Resource.

    This is the resource that is used to interact with the /api/records/{id_} endpoint.
    """

    endpoint = "/records/{id_}"

    def get(self):
        """Get a record."""
        return self._get(RecordMetadata)

    def create(self, data=None):
        """Create new draft."""
        return self._post(DraftMetadata, data=data, resource=self.draft)

    def edit(self):
        """Create a draft from a published record (shortcut)."""
        return self.draft.create()

    def new_version(self):
        """Create a new version of a published record (shortcut)."""
        return self.versions.create()

    def search(self, **params):
        """Search for a record."""
        # TODO isn't this more suited to use with the RecordList (/api/records) resource?
        return self._search(RecordMetadata, **params)

    @property
    def draft(self):
        """Creates and returns a record draft API object."""
        return Draft(self._client, **self.endpoint_args)

    @property
    def versions(self):
        """Creates and rerturns record versions API object."""
        return RecordVersions(self._client, **self.endpoint_args)

    @property
    def files(self):
        """Record files."""
        return RecordFilesList(self._client, **self.endpoint_args)

    @property
    def access(self):
        """Record access."""
        pass


class RecordVersions(Resource):
    """Implements a RecordVersions as a Resource.

    This is the resource that is used to interact with the /api/records/{id_}/versions endpoint.
    """

    endpoint = "/records/{id_}/versions"

    def create(self):
        """Create a new draft version of a published record."""
        return self._post(
            DraftMetadata, resource=Draft(self._client, **self.endpoint_args)
        )

    def latest(self):
        """Get the latest version of a record."""
        return self._get(
            RecordMetadata,
            url_suffix="/latest",
            resource=Record(self._client, **self.endpoint_args),
        )

    def search(self, q="", page=1, size=10, sort="newest", allversions=True):
        """Search for record versions."""
        params = dict(q=q, page=page, size=size, sort=sort)
        if allversions:
            params["allversions"] = "1"

        return self._search(
            params,
            RecordListMetadata,
            self._make_factory(Record),
            self._partial(self.search, params, page=params["page"] - 1),
            self._partial(self.search, params, page=params["page"] + 1),
        )


class Draft(Resource):
    """Implements a Draft as a Resource.

    This is the resource that is used to interact with the /api/records/{id_}/draft endpoint.
    """

    endpoint = "/records/{id_}/draft"

    def get(self):
        """Get a draft."""
        return self._get(DraftMetadata)

    def create(self):
        """Edit a record."""
        return self._post(DraftMetadata)

    def delete(self):
        """Delete/discard a draft."""
        return self._delete()

    def update(self, data=None):
        """Update a draft."""
        return self._put(DraftMetadata, data=data or self.data)

    @property
    def files(self):
        """Draft files."""
        return DraftFilesList(self._client, **self.endpoint_args)

    def import_files(self):
        """Run import files action."""
        # TODO
        self._post(
            None,
        )
        resp = self.session.post(
            self.url("/actions/files-import"), headers=self.headers({})
        )
        self.raise_on_error(resp)
        self.data = self.item_class(resp)
        return self

    def publish(self):
        """Publish draft."""
        return self._post(
            RecordMetadata,
            url_suffix="/actions/publish",
            resource=Record(self._client, **self.endpoint_args),
        )


class RecordList(Resource):
    """Implements a RecordList as a Resource.

    This is the resource that is used to interact with the /api/records endpoint.
    """ ""

    endpoint = "/records"

    def __call__(self, id_):
        """Instantiate a record item resource."""
        return Record(self._client, id_=id_)

    @property
    def draft(self):
        """Creates and returns a record draft API object."""
        return Draft(self._client, **self.endpoint_args)

    def create(self, data=None):
        """Create new draft."""
        return self._post(DraftMetadata, data=data, resource=self.draft)

    def search(self, q="", page=1, size=10, sort="newest", allversions=False):
        """Search for records."""
        params = dict(q=q, page=page, size=size, sort=sort)
        if allversions:
            params["allversions"] = "1"
        return self._search(
            params,
            RecordListMetadata,
            self._make_factory(Record),
            self._partial(self.search, params, page=params["page"] - 1),
            self._partial(self.search, params, page=params["page"] + 1),
        )


class RecordFilesList(Resource):
    """Implements a RecordFilesList as a Resource.

    This is the resource that is used to interact with the /api/records/{id_}/files endpoint.
    """

    endpoint = "/records/{id_}/files"

    def get(self):
        """Get a files list."""
        return self._get(FilesListMetadata)

    def __call__(self, key):
        """Instantiate a record item resource."""
        return RecordFile(self._client, filename=key, **self._endpoint_args)


class RecordFile(Resource):
    """Implements a RecordFile as a Resource.

    This is the resource that is used to interact with the /api/records/{id_}/files/{filename} endpoint.
    """

    endpoint = "/records/{id_}/files/{filename}"

    def get(self):
        """Get file metadata."""
        return self._get(FileMetadata)

    def download(self):
        """Download a file."""
        return self._get_raw(
            IncomingStream, url_suffix="/content", params={"stream": True}
        )


class DraftFilesList(Resource):
    """Implements a DraftFilesList as a Resource.

    This is the resource that is used to interact with the /api/records/{id_}/draft/files endpoint.
    """

    endpoint = "/records/{id_}/draft/files"

    def get(self):
        """Get all the files of the draft."""
        return self._get(FilesListMetadata)

    def create(self, data):
        """Create a list of files in the draft."""
        return self._post(FilesListMetadata, data=data)

    def __call__(self, key):
        """Instantiate a record item resource."""
        return DraftFile(self._client, filename=key, **self._endpoint_args)

    def __iter__(self):
        """Iterate over files of the draft."""
        self._it = iter(self.get().data["entries"])
        return self

    def __next__(self):
        """Returns the next file in the draft, instantiated as a `DraftFile`."""
        obj = next(self._it)
        if not obj:
            raise StopIteration
        metadata = FileMetadata(**obj)
        file = DraftFile(self._client, filename=metadata["key"], **self._endpoint_args)
        file.data = metadata
        return file


class DraftFile(Resource):
    """Implements a DraftFile as a Resource.

    This is the resource that is used to interact with the /api/records/{id_}/draft/files/{filename} endpoint.
    """

    endpoint = "/records/{id_}/draft/files/{filename}"

    def set_contents(self, stream):
        """Set file contents."""
        return self._put(OutgoingStream, data=stream, url_suffix="/content")

    def commit(self):
        """Commit one file."""
        return self._post(FileMetadata, url_suffix="/commit")

    def download(self):
        """Download a file."""
        return self._get_raw(
            IncomingStream, url_suffix="/content", params={"stream": True}
        )

    def delete(self):
        """Delete a file."""
        return self._delete()

    def get(self):
        """Get file information."""
        return self._get(FileMetadata)
