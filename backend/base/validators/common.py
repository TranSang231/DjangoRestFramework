"""
Common validators for the application
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models


class BaseValidator:
    """Base validator class with common functionality"""
    
    @staticmethod
    def validate_required(value, field_name="Field"):
        """Validate that a field is not empty"""
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(_(f"{field_name} is required."))
        return value
    
    @staticmethod
    def validate_min_length(value, min_length, field_name="Field"):
        """Validate minimum length"""
        if isinstance(value, str) and len(value) < min_length:
            raise ValidationError(_(f"{field_name} must be at least {min_length} characters long."))
        return value
    
    @staticmethod
    def validate_max_length(value, max_length, field_name="Field"):
        """Validate maximum length"""
        if isinstance(value, str) and len(value) > max_length:
            raise ValidationError(_(f"{field_name} must be no more than {max_length} characters long."))
        return value
    
    @staticmethod
    def validate_range(value, min_val, max_val, field_name="Field"):
        """Validate numeric range"""
        if isinstance(value, (int, float)):
            if value < min_val or value > max_val:
                raise ValidationError(_(f"{field_name} must be between {min_val} and {max_val}."))
        return value


class VietnamesePhoneValidator(RegexValidator):
    """Validator for Vietnamese phone numbers"""
    regex = r'^(\+84|84|0)[1-9][0-9]{8,9}$'
    message = _('Enter a valid Vietnamese phone number.')
    code = 'invalid_phone'


class VietnameseIDValidator(RegexValidator):
    """Validator for Vietnamese ID numbers (CCCD/CMND)"""
    regex = r'^[0-9]{9,12}$'
    message = _('Enter a valid Vietnamese ID number (9-12 digits).')
    code = 'invalid_id'


class StrongPasswordValidator:
    """Validator for strong passwords"""
    
    def __init__(self, min_length=8, require_uppercase=True, require_lowercase=True, 
                 require_numbers=True, require_special_chars=True):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_numbers = require_numbers
        self.require_special_chars = require_special_chars
    
    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(_(f'Password must be at least {self.min_length} characters long.'))
        
        if self.require_uppercase and not re.search(r'[A-Z]', value):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        
        if self.require_lowercase and not re.search(r'[a-z]', value):
            raise ValidationError(_('Password must contain at least one lowercase letter.'))
        
        if self.require_numbers and not re.search(r'[0-9]', value):
            raise ValidationError(_('Password must contain at least one number.'))
        
        if self.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError(_('Password must contain at least one special character.'))


class UniqueTogetherValidator:
    """Validator for unique together constraints"""
    
    def __init__(self, fields, model_class, exclude_field=None):
        self.fields = fields
        self.model_class = model_class
        self.exclude_field = exclude_field
    
    def __call__(self, value, instance=None):
        if not instance:  # Creating new instance
            filter_kwargs = {field: value.get(field) for field in self.fields if field in value}
            if self.model_class.objects.filter(**filter_kwargs).exists():
                raise ValidationError(_(f'Combination of {", ".join(self.fields)} must be unique.'))
        else:  # Updating existing instance
            filter_kwargs = {field: value.get(field) for field in self.fields if field in value}
            queryset = self.model_class.objects.filter(**filter_kwargs)
            if self.exclude_field:
                queryset = queryset.exclude(**{self.exclude_field: getattr(instance, self.exclude_field)})
            if queryset.exists():
                raise ValidationError(_(f'Combination of {", ".join(self.fields)} must be unique.'))


class ConditionalValidator:
    """Validator that applies validation based on conditions"""
    
    def __init__(self, condition_field, condition_value, validator, error_message=None):
        self.condition_field = condition_field
        self.condition_value = condition_value
        self.validator = validator
        self.error_message = error_message
    
    def __call__(self, value, instance=None):
        # This would be used in serializer validation
        pass


def validate_vietnamese_name(value):
    """Validate Vietnamese names (allow Vietnamese characters)"""
    if not re.match(r'^[a-zA-ZÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐđ\s]+$', value):
        raise ValidationError(_('Name can only contain letters and spaces.'))
    return value


def validate_no_special_chars(value):
    """Validate that string contains no special characters"""
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(_('Field cannot contain special characters.'))
    return value

