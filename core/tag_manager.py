#!/usr/bin/env python3
"""
Tag Manager - Handles custom file metadata tags
"""

import json
import os
from pathlib import Path


class TagManager:
    """Manages custom tags for files with persistent storage"""
    
    def __init__(self):
        """Initialize tag manager with persistent storage"""
        self.tags_file = os.path.expanduser('~/.file_sorter_tags.json')
        self.tags = self._load_tags()
    
    def _load_tags(self):
        """Load tags from persistent storage"""
        if os.path.exists(self.tags_file):
            try:
                with open(self.tags_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_tags(self):
        """Save tags to persistent storage"""
        with open(self.tags_file, 'w') as f:
            json.dump(self.tags, f, indent=2)
    
    def add_tag(self, file_path, tag_name, tag_value):
        """
        Add tag to file.
        
        Args:
            file_path: Path to file
            tag_name: Tag category name (e.g., "Manufacturer")
            tag_value: Tag value (e.g., "Sony")
        """
        if file_path not in self.tags:
            self.tags[file_path] = {}
        
        self.tags[file_path][tag_name] = tag_value
        self._save_tags()
    
    def remove_tag(self, file_path, tag_name):
        """
        Remove tag from file.
        
        Args:
            file_path: Path to file
            tag_name: Tag category name to remove
        """
        if file_path in self.tags and tag_name in self.tags[file_path]:
            del self.tags[file_path][tag_name]
            
            if not self.tags[file_path]:
                del self.tags[file_path]
            
            self._save_tags()
    
    def get_tags(self, file_path):
        """
        Get all tags for a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary of tags or empty dict
        """
        return self.tags.get(file_path, {})
    
    def get_files_by_tag(self, tag_name, tag_value):
        """
        Get all files with a specific tag.
        
        Args:
            tag_name: Tag category name
            tag_value: Tag value to search for
            
        Returns:
            List of file paths
        """
        files = []
        for file_path, file_tags in self.tags.items():
            if file_tags.get(tag_name) == tag_value:
                files.append(file_path)
        return files
    
    def get_all_tag_categories(self):
        """
        Get all unique tag categories across all files.
        
        Returns:
            Set of tag category names
        """
        categories = set()
        for file_tags in self.tags.values():
            categories.update(file_tags.keys())
        return sorted(categories)
