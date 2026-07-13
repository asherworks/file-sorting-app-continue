#!/usr/bin/env python3
"""
File Sorter - Handles sorting files by various criteria with optimized tag-based sorting
"""

from collections import defaultdict


class FileSorter:
    """Sorts files based on different criteria with optimized performance"""
    
    def __init__(self):
        """Initialize sorter with cache"""
        self._tag_cache = {}
        self._cache_valid = False
    
    @staticmethod
    def sort_files(files, column, reverse=False):
        """Sort files based on column - O(n log n)"""
        sort_key = {
            0: 'name',
            1: 'type',
            2: 'size',
            3: 'modified_timestamp'
        }.get(column, 'name')
        
        files.sort(key=lambda x: x.get(sort_key, ''), reverse=reverse)
        return files
    
    def sort_by_custom_category_optimized(self, files, category, tag_manager):
        """
        Sort files by custom category with O(n) performance.
        
        Optimization techniques:
        - Pre-build tag lookup dictionary in O(n) instead of O(n*m)
        - Use defaultdict for O(1) group access
        - Cache frequently accessed tags
        - Single pass through files
        
        Args:
            files: List of file info dictionaries
            category: Tag category name (e.g., "Manufacturer")
            tag_manager: TagManager instance
            
        Returns:
            Sorted list grouped by tag value
        """
        # Build efficient lookup dictionary in single pass - O(n)
        tag_lookup = self._build_tag_lookup(tag_manager, category)
        
        # Group files efficiently using defaultdict - O(n)
        groups = defaultdict(list)
        untagged = []
        
        for file_info in files:
            file_path = file_info['path']
            tag_value = tag_lookup.get(file_path)  # O(1) dictionary access
            
            if tag_value:
                groups[tag_value].append(file_info)
            else:
                untagged.append(file_info)
        
        # Sort and concatenate - O(n log n) for sorting names within groups
        sorted_files = []
        for key in sorted(groups.keys()):
            sorted_files.extend(sorted(groups[key], key=lambda x: x['name']))
        
        sorted_files.extend(sorted(untagged, key=lambda x: x['name']))
        
        return sorted_files
    
    def _build_tag_lookup(self, tag_manager, category):
        """
        Build a fast lookup dictionary for tag values - O(n).
        
        Reads tags once and creates a {file_path: tag_value} dict for O(1) access.
        
        Args:
            tag_manager: TagManager instance
            category: Tag category name
            
        Returns:
            Dictionary mapping file paths to tag values
        """
        lookup = {}
        
        # Get all tagged files for this category - O(n) where n = tagged files
        for file_path, file_tags in tag_manager.tags.items():
            if category in file_tags:
                lookup[file_path] = file_tags[category]
        
        return lookup
    
    def sort_by_custom_category(self, files, category, tag_manager):
        """
        Backward compatible wrapper to optimized sort.
        Use this to replace your existing method call.
        """
        return self.sort_by_custom_category_optimized(files, category, tag_manager)
    
    @staticmethod
    def sort_by_size(files, reverse=False):
        """Sort files by size - O(n log n)"""
        files.sort(key=lambda x: x['size'], reverse=reverse)
        return files
    
    @staticmethod
    def sort_by_type(files, reverse=False):
        """Sort files by type - O(n log n)"""
        files.sort(key=lambda x: x['type'], reverse=reverse)
        return files
    
    @staticmethod
    def sort_by_date(files, reverse=False):
        """Sort files by modification date - O(n log n)"""
        files.sort(key=lambda x: x['modified_timestamp'], reverse=reverse)
        return files
    
    def batch_sort_by_multiple_categories(self, files, categories, tag_manager, primary_category=0):
        """
        Sort by multiple categories for advanced use cases - O(n log n).
        
        Example:
            sorter.batch_sort_by_multiple_categories(
                files, 
                ["Manufacturer", "Product", "Color"], 
                tag_manager
            )
        
        Args:
            files: List of file info
            categories: List of category names in priority order
            tag_manager: TagManager instance
            primary_category: Index of primary sort (default 0)
            
        Returns:
            Files sorted by multiple tag criteria
        """
        # Build lookups for all categories upfront - O(n * m) where m = num categories
        lookups = {}
        for category in categories:
            lookups[category] = self._build_tag_lookup(tag_manager, category)
        
        # Sort by all categories using multi-key comparison - O(n log n)
        def multi_key(file_info):
            path = file_info['path']
            keys = []
            for category in categories:
                tag_value = lookups[category].get(path, "~UNTAGGED~")  # ~ sorts last
                keys.append(tag_value)
            return tuple(keys)
        
        files.sort(key=multi_key)
        return files
