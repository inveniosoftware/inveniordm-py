# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record resources."""

from functools import partial

from ..resources import Resource
from .metadata import *

class Record(Resource):
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
        return self._search(RecordMetadata, **params)

    @property
    def draft(self):
        return Draft(self._client, **self._endpoint_args)

    @property
    def versions(self):
        return RecordVersions(self._client, **self._endpoint_args)

    @property
    def files(self):
        pass

    @property
    def access(self):
        pass


class RecordVersions(Resource):
    endpoint = "/records/{id_}/versions"

    def create(self):
        """Create a new draft version of a published record."""
        return self._post(DraftMetadata, resource=Draft(self._client, **self._endpoint_args))

    def latest(self):
        """Get the latest version of a record."""
        return self._get(RecordMetadata, url_suffix='/latest', resource=Record(self._client, **self._endpoint_args))

    def search(self, q="", page=1, size=10, sort='newest', allversions=True):
        params = dict(q=q, page=page, size=size, sort=sort)
        if allversions:
            params['allversions'] = '1'

        return self._search(
            params,
            RecordListMetadata,
            self._make_factory(Record),
            self._partial(self.search, params, page=params['page'] - 1),
            self._partial(self.search, params, page=params['page'] + 1),
        )


class Draft(Resource):
    endpoint = "/records/{id_}/draft"

    def get(self):
        """Get a draft"""
        return self._get(DraftMetadata)

    def create(self):
        """Edit a record"""
        return self._post(DraftMetadata)

    def delete(self):
        """Delete/discard a draft"""
        return self._delete()

    def update(self, data=None):
        """Update a draft"""
        return self._put(DraftMetadata, data=data or self.data)

    @property
    def files(self):
        pass

    def import_files(self):
        """Run import files action."""
        # TODO
        self._post(None,)
        resp = self.session.post(self.url('/actions/files-import'), headers=self.headers({}))
        self.raise_on_error(resp)
        self.data = self.item_class(resp)
        return self

    def publish(self):
        """Publish draft."""
        return self._post(
            RecordMetadata,
            url_suffix='/actions/publish',
            resource=Record(self._client, **self._endpoint_args),
        )


class RecordList(Resource):
    endpoint = "/records"

    def __call__(self, id_):
        """Instantiate a record item resource."""
        return Record(self._client, id_=id_)

    def search(self, q="", page=1, size=10, sort='newest', allversions=False):
        params = dict(q=q, page=page, size=size, sort=sort)
        if allversions:
            params['allversions'] = '1'
        return self._search(
            params,
            RecordListMetadata,
            self._make_factory(Record),
            self._partial(self.search, params, page=params['page'] - 1),
            self._partial(self.search, params, page=params['page'] + 1),
        )


class FilesList(Resource):
    endpoint = "/records/{id_}/files"

    def get(self):
        """Get a files lsit"""
        return self._get(FilesListMetadata)

    def __call__(self, key):
        """Instantiate a record item resource."""
        return File(self._client, id_=id_, key=key)


class File(Resource):
    endpoint = "/records/{id_}/files/{key}"

    def get(self):
        """Get a files lsit"""
        return self._get(FileMetadata)

    def download(self):
        """Download a file"""
        return self._get(Stream, url_suffix='/content')
