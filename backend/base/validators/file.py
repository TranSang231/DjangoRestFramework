"""
File validation utilities
"""
import os
import magic
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _


class FileSizeValidator:
    """Validator for file size"""
    
    def __init__(self, max_size_mb=5):
        self.max_size_bytes = max_size_mb * 1024 * 1024
    
    def __call__(self, value):
        if not value:
            return value
        
        if hasattr(value, 'size'):
            if value.size > self.max_size_bytes:
                max_size_mb = self.max_size_bytes / (1024 * 1024)
                raise ValidationError(_(f'File size must be no more than {max_size_mb:.1f} MB.'))
        
        return value


class FileTypeValidator:
    """Validator for file type based on extension and MIME type"""
    
    def __init__(self, allowed_types=None, allowed_extensions=None):
        self.allowed_types = allowed_types or []
        self.allowed_extensions = allowed_extensions or []
    
    def __call__(self, value):
        if not value:
            return value
        
        # Check file extension
        if hasattr(value, 'name'):
            file_extension = os.path.splitext(value.name)[1].lower()
            if self.allowed_extensions and file_extension not in self.allowed_extensions:
                raise ValidationError(_(f'File type {file_extension} is not allowed. Allowed types: {", ".join(self.allowed_extensions)}'))
        
        # Check MIME type
        if hasattr(value, 'content_type'):
            if self.allowed_types and value.content_type not in self.allowed_types:
                raise ValidationError(_(f'File type {value.content_type} is not allowed. Allowed types: {", ".join(self.allowed_types)}'))
        
        return value


class ImageValidator(FileTypeValidator):
    """Validator specifically for images"""
    
    def __init__(self, max_size_mb=5):
        super().__init__(
            allowed_types=[
                'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
                'image/webp', 'image/svg+xml'
            ],
            allowed_extensions=['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        )
        self.max_size_mb = max_size_mb
    
    def __call__(self, value):
        # First check file type
        super().__call__(value)
        
        # Then check file size
        size_validator = FileSizeValidator(self.max_size_mb)
        size_validator(value)
        
        return value


class DocumentValidator(FileTypeValidator):
    """Validator for documents (PDF, DOC, etc.)"""
    
    def __init__(self, max_size_mb=10):
        super().__init__(
            allowed_types=[
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/plain'
            ],
            allowed_extensions=['.pdf', '.doc', '.docx', '.txt']
        )
        self.max_size_mb = max_size_mb
    
    def __call__(self, value):
        # First check file type
        super().__call__(value)
        
        # Then check file size
        size_validator = FileSizeValidator(self.max_size_mb)
        size_validator(value)
        
        return value


class VideoValidator(FileTypeValidator):
    """Validator for video files"""
    
    def __init__(self, max_size_mb=100):
        super().__init__(
            allowed_types=[
                'video/mp4', 'video/avi', 'video/mov', 'video/wmv',
                'video/flv', 'video/webm'
            ],
            allowed_extensions=['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
        )
        self.max_size_mb = max_size_mb
    
    def __call__(self, value):
        # First check file type
        super().__call__(value)
        
        # Then check file size
        size_validator = FileSizeValidator(self.max_size_mb)
        size_validator(value)
        
        return value


class AudioValidator(FileTypeValidator):
    """Validator for audio files"""
    
    def __init__(self, max_size_mb=50):
        super().__init__(
            allowed_types=[
                'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp3',
                'audio/aac', 'audio/flac'
            ],
            allowed_extensions=['.mp3', '.wav', '.ogg', '.aac', '.flac']
        )
        self.max_size_mb = max_size_mb
    
    def __call__(self, value):
        # First check file type
        super().__call__(value)
        
        # Then check file size
        size_validator = FileSizeValidator(self.max_size_mb)
        size_validator(value)
        
        return value


def validate_file_name(value, max_length=255, allowed_chars=None):
    """Validate file name"""
    if not value:
        return value
    
    if hasattr(value, 'name'):
        filename = value.name
        
        if len(filename) > max_length:
            raise ValidationError(_(f'File name must be no more than {max_length} characters long.'))
        
        if allowed_chars:
            import re
            if not re.match(allowed_chars, filename):
                raise ValidationError(_('File name contains invalid characters.'))
        
        # Check for dangerous file names
        dangerous_names = ['..', '.', 'CON', 'PRN', 'AUX', 'NUL']
        if filename.upper() in dangerous_names:
            raise ValidationError(_('File name is not allowed.'))
    
    return value


class SecureFileValidator:
    """Validator that checks for malicious files"""
    
    def __init__(self):
        self.dangerous_extensions = ['.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js']
        self.dangerous_mime_types = [
            'application/x-executable',
            'application/x-msdownload',
            'application/x-msdos-program'
        ]
    
    def __call__(self, value):
        if not value:
            return value
        
        # Check extension
        if hasattr(value, 'name'):
            file_extension = os.path.splitext(value.name)[1].lower()
            if file_extension in self.dangerous_extensions:
                raise ValidationError(_('File type is not allowed for security reasons.'))
        
        # Check MIME type
        if hasattr(value, 'content_type'):
            if value.content_type in self.dangerous_mime_types:
                raise ValidationError(_('File type is not allowed for security reasons.'))
        
        return value

