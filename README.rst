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
    client = InvenioAPI('https://your-invenio-instance.com/api', 'your-token')

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
    draft = client.records.create(data=DraftMetadata(**data))
    
    # Update metadata and draft
    data["metadata"]["title"] = "Test 2"
    draft.update(data=DraftMetadata(**data))

Individual files can be added to the draft:

.. code-block:: python

    from inveniordm_py.files.metadata import OutgoingStream, FilesListMetadata
    from pathlib import Path
    
    # Create a single file metadata and add it to the draft using a stream
    demo_file = Path("inveniordm_py_demo_file.txt")
    demo_file.write_text(f"This is demo file content.")
    file_data = FilesListMetadata([{"key": demo_file.name}])
    draft.files.create(file_data)
    draft_file = list(draft.files)[0]
    with demo_file.open() as stream:
        draft_file.set_contents(OutgoingStream(data=stream))
        draft_file.commit()
    
    # cleanup draft by deleting single demo file
    list(draft.files)[0].delete()

Alternatively, multiple files can be added to the draft:

.. code-block:: python

    # Create local set of demo files to be uploaded
    demo_dir = Path("inveniordm_py_demo_directory")
    demo_dir.mkdir(parents=True, exist_ok=True)
    for i in range(3):
        file_path = demo_dir / f"dataset_{i}.txt"
        file_path.write_text(f"Content of demo file #{i}.")
    
    # Create a multi-file metadata and add it to the draft using a stream
    file_data = FilesListMetadata([{"key": fpath.name} for fpath in sorted(demo_dir.glob("*"))])
    draft.files.create(file_data)
    for f in draft.files:
        with (demo_dir / f.data["key"]).open() as stream:
            f.set_contents(OutgoingStream(data=stream))
            f.commit()

Finally, the draft can be published:

.. code-block:: python

    # Publish the draft and check the status
    record = draft.publish()
    print(f"Record status: {record.data['status']}")
