# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resource base class."""

from copy import copy
from functools import partial

from .metadata import *
from .pagination import SimplePagination


class Resource:
    """Resource base class."""

    endpoint = ""

    def __init__(self, client, **kwargs):
        """Initialize a resource.

        Any keyword arguments are used as endpoint arguments.
        """
        self._client = client
        self._endpoint_args = kwargs
        self._data = None

    @property
    def session(self):
        """Get the client bound session."""
        return self._client.session

    @property
    def data(self):
        """Get the resource data object."""
        return self._data

    @property
    def endpoint_args(self) -> dict:
        """Get endpoint arguments.

        Arguments are computed from the data and the resource.
        Precedence is given to the resource endpoint kwargs.
        """
        if isinstance(self.data, Metadata):
            return {**self.data.endpoint_kwargs, **self._endpoint_args}
        return self._endpoint_args

    @data.setter
    def data(self, value):
        """Set the resource data object."""
        self._data = value

    def _resource_or_self(self, resource):
        """Return the resource or self if resource is None."""
        return resource if resource is not None else self

    def _partial(self, method, params, **updates):
        """Create a partial method with updated parameters."""
        newparams = copy(params)
        newparams.update(updates)
        return partial(method, **newparams)

    def _make_factory(self, resource_cls):
        """Factory for creating a resource from a metadata object."""

        def inner(data):
            r = resource_cls(self._client, **data.endpoint_kwargs)
            r.data = data
            return r

        return inner

    #
    # Request helper methods
    #
    def url(self, suffix=""):
        """Construct the URL for an REST API endpoint."""
        endpoint = self.endpoint.format(**self.endpoint_args)
        return f"{self._client._base_url}{endpoint}{suffix}"

    def headers(self, accept=None, data=None, extra=None):
        """Construct request headers."""
        defaults = {}
        if accept is not None:
            defaults["accept"] = accept.accept
        if data is not None:
            defaults["content-type"] = data.content_type
        if extra is not None:
            defaults.update(extra)
        return defaults

    def raise_on_error(self, response):
        """Check response for errors."""
        response.raise_for_status()

    #
    # HTTP request methods
    #
    def _get(
        self, metadata_class, url_suffix="", params=None, headers=None, resource=None
    ):
        """Make a GET request."""
        resource = self._resource_or_self(resource)
        headers = self.headers(accept=metadata_class, extra=headers)
        resp = self.session.get(
            self.url(suffix=url_suffix),
            headers=headers,
            params=params,
        )
        self.raise_on_error(resp)
        resource.data = metadata_class.from_response(resp)
        return resource

    def _post(
        self, metadata_class, data=None, url_suffix="", headers=None, resource=None
    ):
        """Make a POST request."""
        resource = self._resource_or_self(resource)
        headers = self.headers(accept=metadata_class, data=data, extra=headers)
        request_data = data.to_request() if data is not None else None
        resp = self.session.post(
            self.url(suffix=url_suffix),
            data=request_data,
            headers=headers,
        )
        self.raise_on_error(resp)
        resource.data = metadata_class.from_response(resp)
        return resource

    def _put(
        self, metadata_class, data=None, url_suffix="", headers=None, resource=None
    ):
        """Make a PUT request."""
        resource = self._resource_or_self(resource)
        headers = self.headers(accept=metadata_class, data=data, extra=headers)
        request_data = data.to_request() if data is not None else None
        resp = self.session.put(
            self.url(suffix=url_suffix),
            data=request_data,
            headers=headers,
        )
        self.raise_on_error(resp)
        resource.data = metadata_class.from_response(resp)
        return resource

    def _get_raw(self, metadata_class, url_suffix="", params=None, headers=None):
        headers = self.headers(accept=metadata_class, extra=headers)
        resp = self.session.get(
            self.url(suffix=url_suffix), headers=headers, params=params
        )
        self.raise_on_error(resp)
        return resp

    def _delete(self, url_suffix="", headers=None):
        """Make a DELETE request."""
        headers = self.headers(extra=headers)
        resp = self.session.delete(self.url(suffix=url_suffix), headers=headers)
        self.raise_on_error(resp)
        return True

    def _search(
        self,
        params,
        metadata_class,
        hit_factory,
        prev_page,
        next_page,
        url_suffix="",
        headers=None,
    ):
        """Make a GET request with pagination."""
        headers = self.headers(accept=metadata_class, extra=headers)
        response = self.session.get(
            self.url(suffix=url_suffix), params=params, headers=headers
        )
        self.raise_on_error(response)
        data_list = metadata_class.from_response(response)
        return SimplePagination(
            data_list,
            hit_factory,
            prev_page=prev_page,
            next_page=next_page,
        )
