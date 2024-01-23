# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Mock request handlers."""


import json
from abc import ABC, abstractmethod


class Handler(ABC):
    """Base handler class.

    This class creates an interfact to handle requests from the mock server.
    """

    def handle(self, request):
        """Handle a request."""
        if request.method == "GET":
            return self._handle_get(request)
        elif request.method == "POST":
            return self._handle_post(request)
        elif request.method == "DELETE":
            return self._handle_delete(request)
        elif request.method == "PUT":
            return self._handle_put(request)
        else:
            raise ValueError(f"Unsupported method {request.method}")

    @abstractmethod
    def _handle_get(self, request):
        """Handle GET requests."""

    @abstractmethod
    def _handle_post(self, request):
        """Handle POST requests."""

    @abstractmethod
    def _handle_delete(self, request):
        """Handle DELETE requests."""

    @abstractmethod
    def _handle_put(self, request):
        """Handle PUT requests."""


class DraftFilesHandler(Handler):
    """Handler for draft files (resource endpoint)."""

    def _handle_get(self, request):
        """Handle GET requests (i.e. list all the files of a draft)."""
        id_ = 1
        return {
            "default_preview": None,
            "enabled": True,
            "entries": [],
            "links": {"self": f"/api/records/{id_}/draft/files"},
            "order": [],
        }

    def _handle_post(self, request):
        """Handle POST requests (i.e. start draft file(s) upload)."""
        id_ = 1
        entries = [
            {
                "key": entry["key"],
                "updated": "2020-11-27 11:17:11.002624",
                "created": "2020-11-27 11:17:10.998919",
                "metadata": None,
                "status": "pending",
                "links": {
                    "content": f"/api/records/{id_}/draft/files/figure.png/content",
                    "self": f"/api/records/{id_}/draft/files/figure.png",
                    "commit": f"/api/records/{id_}/draft/files/figure.png/commit",
                },
            }
            for entry in json.loads(request.data)
        ]
        return {
            "enabled": True,
            "default_preview": None,
            "order": [],
            "entries": entries,
            "links": {"self": f"/api/records/{id_}/draft/files"},
        }

    def _handle_delete(self, request):
        """Handle DELETE requests, the API does not implement this endpoint."""
        raise NotImplementedError

    def _handle_put(self, request):
        """Handle PUT requests, the API does not implement this endpoint."""
        raise NotImplementedError


class DraftFileHandler(Handler):
    """Handler for draft file (single file endpoint)."""

    def _handle_get(self, request):
        """Handle GET requests (i.e. get a draft's file metadata)."""
        id_ = 1
        filename = request.params["filename"]
        return {
            "key": f"{filename}",
            "updated": "2020-11-27 11:26:04.607831",
            "created": "2020-11-27 11:17:10.998919",
            "checksum": "md5:6ef4267f0e710357c895627e931f16cd",
            "mimetype": "image/png",
            "size": 89364.0,
            "status": "completed",
            "metadata": {"width": 960, "height": 640},
            "file_id": "2151fa94-6dc3-4965-8df9-ec73ceb9175c",
            "version_id": "57ad8c66-b934-49c9-a46f-38bf5aa0374f",
            "bucket_id": "90b5b318-114a-4b87-bc9d-0d018b9363d3",
            "storage_class": "S",
            "links": {
                "content": f"/api/records/{id_}/draft/files/{filename}/content",
                "self": f"/api/records/{id_}/draft/files/{filename}",
                "commit": f"/api/records/{id_}/draft/files/{filename}/commit",
            },
        }

    def _handle_post(self, request):
        """Handle POST requests (i.e. complete the upload of a file)."""
        id_ = request.params["_id"]
        filename = request.params["filename"]
        return {
            "key": f"{filename}",
            "updated": "2020-11-27 11:26:04.607831",
            "created": "2020-11-27 11:17:10.998919",
            "checksum": "md5:6ef4267f0e710357c895627e931f16cd",
            "mimetype": "image/png",
            "size": 89364.0,
            "status": "completed",
            "metadata": None,
            "file_id": "2151fa94-6dc3-4965-8df9-ec73ceb9175c",
            "version_id": "57ad8c66-b934-49c9-a46f-38bf5aa0374f",
            "bucket_id": "90b5b318-114a-4b87-bc9d-0d018b9363d3",
            "storage_class": "S",
            "links": {
                "content": f"/api/records/{id_}/draft/files/{filename}/content",
                "self": f"/api/records/{id_}/draft/files/{filename}",
                "commit": f"/api/records/{id_}/draft/files/{filename}/commit",
            },
        }

    def _handle_delete(self, request):
        """Handle DELETE requests."""
        return {}

    def _handle_put(self, request):
        """Handle PUT requests, the API does not implement this endpoint."""
        raise NotImplementedError


class RecordsListHandler(Handler):
    """Handler for records list."""

    def _handle_get(self, request):
        """Handle GET requests (i.e. list all records)."""
        return {
            "aggregations": {...},
            "hits": {...},
            "links": {...},
            "sortBy": ...,
        }

    @property
    def base(self):
        """Base response, does not contain metadata."""
        return {
            "access": {
                "record": "public",
                "files": "public",
                "embargo": {"reason": None, "active": False},
            },
            "created": "2020-11-27 10:52:23.945755",
            "expires_at": "2020-11-27 10:52:23.945868",
            "files": {"enabled": True},
            "id": 1,
            "is_published": False,
            "links": {
                "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
                "versions": "{scheme+hostname}/api/records/{id}/versions",
                "self_html": "{scheme+hostname}/uploads/{id}",
                "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
                "latest_html": "{scheme+hostname}/records/{id}/latest",
                "self": "{scheme+hostname}/api/records/{id}/draft",
                "files": "{scheme+hostname}/api/records/{id}/draft/files",
                "access_links": "{scheme+hostname}/api/records/{id}/access/links",
            },
            "parent": {
                "id": 0,
                "access": {"owned_by": [{"user": 1}], "links": []},
            },
            "pids": {},
            "revision_id": 3,
            "updated": "2020-11-27 10:52:23.969244",
            "versions": {"index": 1, "is_latest": False, "is_latest_draft": True},
        }

    @property
    def meta(self):
        """Metadata response for the record."""
        return (
            {
                "resource_type": {"id": "image-photo", "title": {"en": "Photo"}},
                "title": "A Romans story",
                "publication_date": "2020-06-01",
                "creators": [
                    {
                        "person_or_org": {
                            "family_name": "Brown",
                            "given_name": "Troy",
                            "type": "personal",
                        }
                    },
                    {
                        "person_or_org": {
                            "family_name": "Collins",
                            "given_name": "Thomas",
                            "identifiers": [
                                {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
                            ],
                            "name": "Collins, Thomas",
                            "type": "personal",
                        },
                        "affiliations": [
                            {
                                "id": "01ggx4157",
                                "name": "European Organization for Nuclear Research",
                            }
                        ],
                    },
                ],
            },
        )

    def _handle_post(self, request):
        """Handle POST requests (i.e. create new draft).

        If the request is empty, return the base response (e.g. a new empty draft).
        Otherwise, return the base response with the metadata (e.g. a new draft with metadata).
        """
        if request.data == {}:
            return self.base

        return {**self.base, "metadata": self.meta}

    def _handle_delete(self, request):
        """Handle DELETE requests."""
        return {}

    def _handle_put(self, request):
        """Handle PUT requests (i.e. update a draft).

        Returns the base response with the metadata.
        """
        return {**self.base, "metadata": self.meta}


class DraftHandler(Handler):
    """Handler for draft (single draft endpoint)."""

    def _handle_get(self, request):
        """Get a draft metadata."""
        return {}

    def _handle_post(self, request):
        """Publish a draft."""
        return {}

    def _handle_delete(self, request):
        """Delete a draft."""
        return {}

    def _handle_put(self, request):
        """Update a draft."""
        id_ = 1
        return {
            "access": {
                "record": "public",
                "files": "public",
                "embargo": {"reason": None, "active": False},
            },
            "created": "2020-11-27 10:52:23.945755",
            "expires_at": "2020-11-27 10:52:23.945868",
            "files": {"enabled": False},
            "id": f"{id_}",
            "is_published": False,
            "links": {
                "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
                "versions": "{scheme+hostname}/api/records/{id}/versions",
                "self_html": "{scheme+hostname}/uploads/{id}",
                "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
                "latest_html": "{scheme+hostname}/records/{id}/latest",
                "self": "{scheme+hostname}/api/records/{id}/draft",
                "files": "{scheme+hostname}/api/records/{id}/draft/files",
                "access_links": "{scheme+hostname}/api/records/{id}/access/links",
            },
            "metadata": {
                "resource_type": {"id": "image-photo", "title": {"en": "Photo"}},
                "title": "An Updated Romans story",
                "publication_date": "2020-06-01",
                "creators": [
                    {
                        "person_or_org": {
                            "family_name": "Collins",
                            "given_name": "Thomas",
                            "identifiers": [
                                {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
                            ],
                            "name": "Collins, Thomas",
                            "type": "personal",
                        },
                        "affiliations": [
                            {
                                "id": "01ggx4157",
                                "name": "European Organization for Nuclear Research",
                            }
                        ],
                    }
                ],
            },
            "parent": {
                "id": "{parent-id}",
                "access": {"owned_by": [{"user": 1}], "links": []},
            },
            "pids": {},
            "revision_id": 3,
            "updated": "2020-11-27 10:52:23.969244",
            "versions": {"index": 1, "is_latest": False, "is_latest_draft": True},
        }
