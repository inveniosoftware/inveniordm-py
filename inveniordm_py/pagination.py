# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pagination classes."""


class SimplePagination:
    """Simple pagination class."""

    def __init__(self, data_list, factory, prev_page, next_page):
        """Initialize pagination object."""
        self._factory = factory
        self._hits = data_list.hits
        self._total = data_list.total
        self._aggregations = data_list.aggregations
        self._prev_page = prev_page
        self._next_page = next_page

    def __iter__(self):
        """Iterator over search hits."""
        for h in self._hits:
            yield self._factory(h)

    def __len__(self):
        """Number of search hits."""
        return len(self._hits)

    def next_page(self):
        """Get next page of the search results."""
        return self._next_page()

    def prev_page(self):
        """Get previous page of the search results."""
        return self._prev_page()
