import pytest
import os
import json
from datetime import datetime
from src.storage.handler import StorageHandler

@pytest.fixture
def storage_handler(tmp_path):
    """Create a storage handler with temporary directory"""
    return StorageHandler(storage_dir=str(tmp_path))

@pytest.fixture
def sample_data():
    """Create sample data for storage"""
    return {
        "id": "test123",
        "title": "Test Item",
        "url": "https://test.com/123",
        "content": {"test_key": "test_value"}
    }

def test_store_latest(storage_handler, sample_data):
    """Test storing latest item"""
    # Store data
    result = storage_handler.store_latest("test_key", sample_data)
    assert result is True
    
    # Verify file exists
    storage_path = storage_handler._get_storage_path("test_key")
    assert os.path.exists(storage_path)
    
    # Verify content
    with open(storage_path, 'r') as f:
        stored_data = json.load(f)
        assert stored_data["id"] == sample_data["id"]
        assert "timestamp" in stored_data  # Should auto-add timestamp

def test_get_latest_existing(storage_handler, sample_data):
    """Test retrieving existing item"""
    # Store first
    storage_handler.store_latest("test_key", sample_data)
    
    # Retrieve
    result = storage_handler.get_latest("test_key")
    
    assert result is not None
    assert result["id"] == sample_data["id"]
    assert result["title"] == sample_data["title"]

def test_get_latest_nonexistent(storage_handler):
    """Test retrieving non-existent item"""
    result = storage_handler.get_latest("nonexistent_key")
    assert result is None

def test_storage_directory_creation(tmp_path):
    """Test storage directory is created if it doesn't exist"""
    storage_dir = os.path.join(str(tmp_path), "new_storage")
    StorageHandler(storage_dir=storage_dir)
    assert os.path.exists(storage_dir)

def test_store_latest_invalid_path(storage_handler, sample_data):
    """Test storing with invalid path"""
    # Make storage directory read-only
    os.chmod(storage_handler.storage_dir, 0o444)
    
    try:
        result = storage_handler.store_latest("test_key", sample_data)
        assert result is False
    finally:
        # Restore permissions for cleanup
        os.chmod(storage_handler.storage_dir, 0o777)