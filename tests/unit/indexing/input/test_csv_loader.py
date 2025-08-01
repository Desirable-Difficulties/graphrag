# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from graphrag.config.enums import InputFileType
from graphrag.config.models.input_config import InputConfig
from graphrag.config.models.storage_config import StorageConfig
from graphrag.index.input.factory import create_input
from graphrag.utils.api import create_storage_from_config


async def test_csv_loader_one_file():
    config = InputConfig(
        storage=StorageConfig(
            base_dir="tests/unit/indexing/input/data/one-csv",
        ),
        file_type=InputFileType.csv,
        file_pattern=".*\\.csv$",
    )
    storage = create_storage_from_config(config.storage)
    documents = await create_input(config=config, storage=storage)
    assert documents.shape == (2, 4)
    assert documents["title"].iloc[0] == "input.csv"


async def test_csv_loader_one_file_with_title():
    config = InputConfig(
        storage=StorageConfig(
            base_dir="tests/unit/indexing/input/data/one-csv",
        ),
        file_type=InputFileType.csv,
        file_pattern=".*\\.csv$",
        title_column="title",
    )
    storage = create_storage_from_config(config.storage)
    documents = await create_input(config=config, storage=storage)
    assert documents.shape == (2, 4)
    assert documents["title"].iloc[0] == "Hello"


async def test_csv_loader_one_file_with_metadata():
    config = InputConfig(
        storage=StorageConfig(
            base_dir="tests/unit/indexing/input/data/one-csv",
        ),
        file_type=InputFileType.csv,
        file_pattern=".*\\.csv$",
        title_column="title",
        metadata=["title"],
    )
    storage = create_storage_from_config(config.storage)
    documents = await create_input(config=config, storage=storage)
    assert documents.shape == (2, 5)
    assert documents["metadata"][0] == {"title": "Hello"}


async def test_csv_loader_multiple_files():
    config = InputConfig(
        storage=StorageConfig(
            base_dir="tests/unit/indexing/input/data/multiple-csvs",
        ),
        file_type=InputFileType.csv,
        file_pattern=".*\\.csv$",
    )
    storage = create_storage_from_config(config.storage)
    documents = await create_input(config=config, storage=storage)
    assert documents.shape == (4, 4)
