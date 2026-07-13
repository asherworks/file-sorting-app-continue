#!/usr/bin/env python3
"""
Favorites Manager - Handles bookmarked folders
"""

import json
import os


class FavoritesManager:
    """Manages favorite/bookmarked folders with persistent storage"""
    
    def __init__(self):
        """Initialize favorites manager with persistent storage"""
        self.favorites_file = os.path.expanduser('~/.file_sorter_favorites.json')
        self.favorites = self._load_favorites()
    
    def _load_favorites(self):
        """Load favorites from persistent storage"""
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_favorites(self):
        """Save favorites to persistent storage"""
        with open(self.favorites_file, 'w') as f:
            json.dump(self.favorites, f, indent=2)
    
    def add_favorite(self, folder_path):
        """
        Add folder to favorites.
        
        Args:
            folder_path: Path to folder to bookmark
        """
        if folder_path not in self.favorites:
            self.favorites.append(folder_path)
            self._save_favorites()
    
    def remove_favorite(self, folder_path):
        """
        Remove folder from favorites.
        
        Args:
            folder_path: Path to folder to unbookmark
        """
        if folder_path in self.favorites:
            self.favorites.remove(folder_path)
            self._save_favorites()
    
    def get_favorites(self):
        """
        Get list of favorite folders.
        
        Returns:
            List of folder paths
        """
        # Filter out folders that no longer exist
        existing = [f for f in self.favorites if os.path.exists(f)]
        
        if existing != self.favorites:
            self.favorites = existing
            self._save_favorites()
        
        return self.favorites
    
    def is_favorite(self, folder_path):
        """
        Check if folder is in favorites.
        
        Args:
            folder_path: Path to folder to check
            
        Returns:
            True if in favorites, False otherwise
        """
        return folder_path in self.favorites
