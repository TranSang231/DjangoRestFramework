"""
String validation utilities
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class StringLengthValidator:
    """Validator for string length"""
    
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length
    
    def __call__(self, value):
        if not value:
            return value
        
        if self.min_length and len(value) < self.min_length:
            raise ValidationError(_(f'String must be at least {self.min_length} characters long.'))
        
        if self.max_length and len(value) > self.max_length:
            raise ValidationError(_(f'String must be no more than {self.max_length} characters long.'))
        
        return value


class AlphanumericValidator:
    """Validator for alphanumeric strings"""
    
    def __init__(self, allow_spaces=False, allow_underscores=False, allow_hyphens=False):
        self.allow_spaces = allow_spaces
        self.allow_underscores = allow_underscores
        self.allow_hyphens = allow_hyphens
    
    def __call__(self, value):
        if not value:
            return value
        
        pattern = r'^[a-zA-Z0-9'
        if self.allow_spaces:
            pattern += r'\s'
        if self.allow_underscores:
            pattern += r'_'
        if self.allow_hyphens:
            pattern += r'-'
        pattern += r']+$'
        
        if not re.match(pattern, value):
            allowed_chars = 'letters, numbers'
            if self.allow_spaces:
                allowed_chars += ', spaces'
            if self.allow_underscores:
                allowed_chars += ', underscores'
            if self.allow_hyphens:
                allowed_chars += ', hyphens'
            
            raise ValidationError(_(f'String can only contain {allowed_chars}.'))
        
        return value


class VietnameseTextValidator:
    """Validator for Vietnamese text"""
    
    def __call__(self, value):
        if not value:
            return value
        
        # Vietnamese character pattern
        vietnamese_pattern = r'^[a-zA-ZÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐĐđ\s\.,!?\-\(\)\[\]{}:;"\']+$'
        
        if not re.match(vietnamese_pattern, value):
            raise ValidationError(_('Text can only contain Vietnamese characters, letters, numbers, and common punctuation.'))
        
        return value


class NoSpecialCharsValidator:
    """Validator that prevents special characters"""
    
    def __init__(self, allowed_chars=None):
        self.allowed_chars = allowed_chars or r'[a-zA-Z0-9\s]'
    
    def __call__(self, value):
        if not value:
            return value
        
        if not re.match(f'^{self.allowed_chars}+$', value):
            raise ValidationError(_('String contains invalid characters.'))
        
        return value


class URLValidator:
    """Validator for URLs"""
    
    def __init__(self, allowed_schemes=None):
        self.allowed_schemes = allowed_schemes or ['http', 'https']
    
    def __call__(self, value):
        if not value:
            return value
        
        url_pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        
        if not re.match(url_pattern, value):
            raise ValidationError(_('Enter a valid URL.'))
        
        # Check scheme
        scheme = value.split('://')[0]
        if scheme not in self.allowed_schemes:
            raise ValidationError(_(f'URL scheme must be one of: {", ".join(self.allowed_schemes)}'))
        
        return value


class SlugValidator:
    """Validator for URL slugs"""
    
    def __call__(self, value):
        if not value:
            return value
        
        slug_pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
        
        if not re.match(slug_pattern, value):
            raise ValidationError(_('Slug can only contain lowercase letters, numbers, and hyphens. It cannot start or end with a hyphen.'))
        
        return value


class UsernameValidator:
    """Validator for usernames"""
    
    def __init__(self, min_length=3, max_length=30):
        self.min_length = min_length
        self.max_length = max_length
    
    def __call__(self, value):
        if not value:
            return value
        
        # Check length
        if len(value) < self.min_length:
            raise ValidationError(_(f'Username must be at least {self.min_length} characters long.'))
        
        if len(value) > self.max_length:
            raise ValidationError(_(f'Username must be no more than {self.max_length} characters long.'))
        
        # Check format (alphanumeric and underscores only)
        username_pattern = r'^[a-zA-Z0-9_]+$'
        if not re.match(username_pattern, value):
            raise ValidationError(_('Username can only contain letters, numbers, and underscores.'))
        
        # Cannot start with number
        if value[0].isdigit():
            raise ValidationError(_('Username cannot start with a number.'))
        
        return value


class HTMLValidator:
    """Validator for HTML content"""
    
    def __init__(self, allowed_tags=None, max_length=None):
        self.allowed_tags = allowed_tags or ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li']
        self.max_length = max_length
    
    def __call__(self, value):
        if not value:
            return value
        
        # Check length
        if self.max_length and len(value) > self.max_length:
            raise ValidationError(_(f'HTML content must be no more than {self.max_length} characters long.'))
        
        # Check for allowed tags only
        tag_pattern = r'<([a-zA-Z][a-zA-Z0-9]*)[^>]*>'
        tags = re.findall(tag_pattern, value)
        
        for tag in tags:
            if tag not in self.allowed_tags:
                raise ValidationError(_(f'HTML tag "{tag}" is not allowed. Allowed tags: {", ".join(self.allowed_tags)}'))
        
        return value


class JSONValidator:
    """Validator for JSON strings"""
    
    def __call__(self, value):
        if not value:
            return value
        
        try:
            import json
            json.loads(value)
        except (ValueError, TypeError):
            raise ValidationError(_('Invalid JSON format.'))
        
        return value


def validate_no_html(value):
    """Validator that prevents HTML content"""
    if not value:
        return value
    
    html_pattern = r'<[^>]+>'
    if re.search(html_pattern, value):
        raise ValidationError(_('HTML content is not allowed.'))
    
    return value


def validate_no_script(value):
    """Validator that prevents script tags"""
    if not value:
        return value
    
    script_pattern = r'<script[^>]*>.*?</script>'
    if re.search(script_pattern, value, re.IGNORECASE | re.DOTALL):
        raise ValidationError(_('Script tags are not allowed.'))
    
    return value

