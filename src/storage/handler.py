import json
import os
from typing import Optional, Dict, Any
from datetime import datetime

class StorageHandler:
    """Handles persistent storage of latest items"""
    
    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
    def _get_storage_path(self, key: str) -> str:
        return os.path.join(self.storage_dir, f"{key}.json")
        
    def get_latest(self, key: str) -> Optional[Dict[str, Any]]:
        """Get the latest stored item for a given key"""
        try:
            path = self._get_storage_path(key)
            if not os.path.exists(path):
                return None
                
            with open(path, 'r') as f:
                data = json.load(f)
                return data
                
        except Exception as e:
            print(f"Error reading storage for {key}: {e}")
            return None
            
    def store_latest(self, key: str, data: Dict[str, Any]) -> bool:
        """Store the latest item for a given key"""
        try:
            path = self._get_storage_path(key)
            
            # Add timestamp if not present
            if "timestamp" not in data:
                data["timestamp"] = datetime.now().isoformat()
                
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
            
        except Exception as e:
            print(f"Error storing data for {key}: {e}")
            return False