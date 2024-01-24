# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# inveniordm-py is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Test client for files."""

import tempfile

import pytest

from inveniordm_py.files.metadata import FilesListMetadata, OutgoingStream
from inveniordm_py.records.metadata import DraftMetadata
from inveniordm_py.records.resources import DraftFile, DraftFilesList

#
# Test draft files list (/record/_id/drafts)
#


@pytest.fixture(scope="module")
def draft(client, minimal_record):
    """Create a draft."""
    draft = client.records.create()
    assert draft
    draft.update(data=DraftMetadata(**minimal_record))
    return draft


@pytest.fixture(scope="module")
def tmp_file():
    """Create a temporary file."""
    tempfile_ = tempfile.TemporaryFile()
    return tempfile_


def test_draft_files_create(draft, tmp_file):
    file_meta = FilesListMetadata([{"key": tmp_file.name}])
    f = draft.files.create(file_meta)
    assert isinstance(f, DraftFilesList)
    assert len(f.data["entries"]) == 1
    assert f.data["entries"][0]["key"] == tmp_file.name


def test_draft_files_iter(draft):
    """Test iterating over draft files."""
    for f in draft.files:
        assert isinstance(f, DraftFile)
        assert f.data["id"] is not None
        assert f.data["entries"] is None


#
# Test individual files for drafts
#


def test_draft_files_upload_workflow(draft, tmp_file):
    """Test uploading a file to a draft."""
    file_meta = FilesListMetadata([{"key": tmp_file.name}])
    draft.files.create(file_meta)
    for f in draft.files:
        f.set_contents(OutgoingStream(data=tmp_file))
        assert f.commit() is not None


def test_draft_files_delete(draft, tmp_file):
    """Test deleting a file from a draft."""
    file_meta = FilesListMetadata([{"key": tmp_file.name}])
    draft.files.create(file_meta)
    assert draft.files(tmp_file.name).delete() is not None


#
# Test record files
#
