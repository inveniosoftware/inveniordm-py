# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio REST API client.."""

from .client import InvenioAPI

__version__ = "0.1.0"

__all__ = ("__version__", "InvenioAPI")
