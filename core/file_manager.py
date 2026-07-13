#!/usr/bin/env python3
"""
File Manager - Handles file system operations
"""

import os
from pathlib import Path
from datetime import datetime


class FileManager:
    """Manages file system operations and metadata retrieval"""
    
    @staticmethod
    def get_files(directory):
        """
        Get list of files in directory with metadata.
        
        Args:
            directory: Path to directory
            
        Returns:
            List of file info dictionaries
        """
        files = []
        
        try:
            for entry in os.listdir(directory):
                file_path = os.path.join(directory, entry)
                
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    
                    file_info = {
                        'name': entry,
                        'path': file_path,
                        'size': stat.st_size,
                        'type': os.path.splitext(entry)[1] or 'No Extension',
                        'modified_timestamp': stat.st_mtime,
                        'modified_date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    }
                    files.append(file_info)
        except PermissionError:
            pass
        
        return files
    
    @staticmethod
    def get_directories(directory):
        """
        Get list of subdirectories.
        
        Args:
            directory: Path to directory
            
        Returns:
            List of subdirectory paths
        """
        dirs = []
        
        try:
            for entry in os.listdir(directory):
                file_path = os.path.join(directory, entry)
                if os.path.isdir(file_path):
                    dirs.append(file_path)
        except PermissionError:
            pass
        
        return sorted(dirs)
    
    @staticmethod
    def file_exists(file_path):
        """Check if file exists"""
        return os.path.exists(file_path)
    
    @staticmethod
    def is_directory(path):
        """Check if path is directory"""
        return os.path.isdir(path)
    
    @staticmethod
    def copy_file(src, dst):
        """Copy file from src to dst"""
        import shutil
        shutil.copy2(src, dst)
    
    @staticmethod
    def move_file(src, dst):
        """Move file from src to dst"""
        import shutil
        shutil.move(src, dst)
    
    @staticmethod
    def delete_file(file_path):
        """Delete file"""
        os.remove(file_path)
    
    @staticmethod
    def rename_file(file_path, new_name):
        """Rename file"""
        directory = os.path.dirname(file_path)
        new_path = os.path.join(directory, new_name)
        os.rename(file_path, new_path)
        return new_path
