# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Community resources."""

from inveniordm_py.communities.metadata import (
    CommunityListMetadata,
    CommunityMetadata,
    CommunityRecordListMetadata,
    CommunityRecordMetadata,
)
from inveniordm_py.records.resources import Record, RecordMetadata
from inveniordm_py.resources import Resource


class Community(Resource):
    """Implements a Community as a Resource.

    This is the resource that is used to interact with the /api/communities/{id_} endpoint.
    """

    endpoint = "/communities/{id_}"

    def create(self, data=None):
        """Create new community."""
        return self._post(CommunityMetadata, data=data, resource=self)

    def update(self, data=None):
        """Update a community"""
        return self._put(CommunityMetadata, data=data, resource=self)

    def delete(self):
        """Delete community."""
        return self._delete()

    def get(self):
        """Get community metadata."""
        self._get(CommunityMetadata)

    @property
    def records(self):
        """Create and returns list of associated records."""
        return CommunityRecordList(self._client, **self.endpoint_args)


class CommunityList(Resource):
    """Implements a CommunityList as a Resource.

    This is the resource that is used to interact with the /api/communities endpoint.
    """ ""

    endpoint = "/communities"

    def get(self) -> CommunityListMetadata:
        """Get all data of the community list."""
        return self._get(CommunityListMetadata)

    def __call__(self, id_) -> Community:
        """Instantiate a community item resource."""
        return Community(self._client, id_=id_)

    def _new(self) -> Community:
        """Creates and returns a community API object."""
        return Community(self._client, **self.endpoint_args)

    def create(self, data=None) -> CommunityMetadata:
        """Create new community."""
        return self._post(CommunityMetadata, data=data, resource=self._new())

    def search(self, q, page=1, size=10, sort="newest"):
        """Search for a community."""
        params = dict(q=q, page=page, size=size, sort=sort)
        return self._search(
            params,
            CommunityListMetadata,
            self._make_factory(Community),
            self._partial(self.search, params, page=params["page"] - 1),
            self._partial(self.search, params, page=params["page"] + 1),
        )

    def __iter__(self):
        """Iterate over communities."""
        self._it = iter(self.get().data["entries"])
        return self

    def __next__(self):
        """Returns the next file in the record list, instantiated as a `Record`."""
        obj = next(self._it)
        if not obj:
            raise StopIteration
        metadata = CommunityListMetadata(**obj)
        community = Community(
            self._client, filename=metadata["key"], **self._endpoint_args
        )
        community.data = metadata
        return community


class CommunityRecordList(Resource):
    """Implements a CommunityRecordList as a Resource.

    This is the resource that is used to interact with the /api/communities/{id_}/records endpoint.s
    """

    endpoint = "/communities/{id_}/records"

    def _normalize_data(self, data):
        """Normalize data to a CommunityRecordMetadata object."""
        if isinstance(data, CommunityRecordMetadata):
            _data = data
        elif isinstance(data, list):
            _data = CommunityRecordMetadata(communities=data)
        elif isinstance(data, str):
            _data = CommunityRecordMetadata(communities=[data])
        else:
            raise ValueError(
                "Data must be a list of records, a single record id, or a CommunityRecordMetadata object."
            )
        return _data

    def get(self):
        """Get all the community record data."""
        return self._get(CommunityRecordListMetadata)

    def add(self, data):
        """Add record to a community.

        The data is first normalized, allowing to pass a list of record, a single record id, or aCommunityRecordMetadata object.

        Usage:

        .. code-block:: python

            records.add(["<record_id_0>", "<record_id_1>"])
            records.add("<record_id>")
            records.add(CommunityRecordMetadata(records=["<record_id_0>", "<record_id_1>"]))
        """
        _data = self._normalize_data(data)

        return self._post(CommunityRecordMetadata, data=_data)

    def search(self):
        """Get record communities."""
        return self._get(CommunityRecordListMetadata)

    def __iter__(self):
        """Iterate over community records."""
        self._it = iter(self.get().data["hits"]["hits"])
        return self

    def __next__(self):
        """Returns the next file in the community record list, instantiated as a `Record`."""
        obj = next(self._it)
        if not obj:
            raise StopIteration
        metadata = RecordMetadata(**obj)
        record = Record(self._client, data={"id_": metadata["id"]})
        record.data = metadata
        record.data["id_"] = metadata["id"]
        return record
