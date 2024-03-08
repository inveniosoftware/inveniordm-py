..
    Copyright (C) 2024 CERN.

    inveniordm-py is free software; you can redistribute it and/or modify
    it under the terms of the MIT License; see LICENSE file for more details.

================
 inveniordm-py
================

.. image:: https://github.com/inveniosoftware/inveniordm-py/workflows/CI/badge.svg
        :target: https://github.com/inveniosoftware/inveniordm-py/actions?query=workflow%3ACI

.. image:: https://img.shields.io/github/tag/inveniosoftware/inveniordm-py.svg
        :target: https://github.com/inveniosoftware/inveniordm-py/releases

.. image:: https://img.shields.io/pypi/dm/inveniordm-py.svg
        :target: https://pypi.python.org/pypi/inveniordm-py

.. image:: https://img.shields.io/github/license/inveniosoftware/inveniordm-py.svg
        :target: https://github.com/inveniosoftware/inveniordm-py/blob/master/LICENSE

`inveniordm-py` is a Python client designed to interact with the InvenioRDM API.


================
Usage
================

Here's a basic example of how to use `inveniordm-py`:

.. code-block:: python

    from inveniordm_py.client import InvenioAPI

    # Initialize client
    client = InvenioAPI('https://your-invenio-instance.com', 'your-token')

    # Get a list of all records
    records = client.records.search()

The client supports creating and updating drafts:

.. code-block:: python

    from inveniordm_py.records.metadata import DraftMetadata

    # Create a draft with metadata
    data = {
        "metadata": {
            "title": "Test",
            "resource_type": {
                "id": "publication-article",
            },
            "publication_date": "2024",
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Brown",
                        "given_name": "Troy",
                        "type": "personal",
                    }
                },
            ],
            "publisher": "Zenodo"
        }
    }
    draft = client.records.create(data=DraftMetadata(data))

    # Update metadata and draft
    data.update({
        "metadata": {
            "title": "Test 2",
        }
    })
    draft.update(data=DraftMetadata(data))

Files can be added to the draft:

.. code-block:: python

    from inveniordm_py.files.metadata import FileMetadata, OutgoingStream, FileMetadata

    # Define files metadata
    fname = "test.txt"
    fpath = "/path/to/test.txt"
    file_data = FileMetadata({"key": fname})

    # Create the file and add it to the draft using a stream
    draft.files.create(file_data)
    stream = open(fpath, "rb")
    f.set_contents(OutgoingStream(data=stream))
    f.commit()

    # It also supports the addition of multiple files from disk
    _dir = "/path/to/dir"
    file_data = FilesListMetadata([{"key": fname} for fname in os.listdir(_dir)])
    draft.files.create(file_data)
    for f in draft.files:
        file_path = os.path.join(_dir, f.data['key'])
        stream = open(file_path, "rb")
        f.set_contents(OutgoingStream(data=stream))
        f.commit()


Finally, the draft can be published:

.. code-block:: python

    # Publish the draft and check the status
    record = draft.publish()
    print(record.data["status"])
