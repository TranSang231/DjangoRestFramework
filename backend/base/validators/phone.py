"""
Phone number validation utilities
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PhoneValidator:
    """Base phone validator class"""
    
    @staticmethod
    def clean_phone_number(phone):
        """Clean phone number by removing spaces, dashes, etc."""
        return re.sub(r'[^\d+]', '', phone)
    
    @staticmethod
    def validate_phone_format(phone, pattern, message):
        """Generic phone format validation"""
        if not re.match(pattern, phone):
            raise ValidationError(message)
        return phone


class VietnamesePhoneValidator(PhoneValidator):
    """Vietnamese phone number validator"""
    
    # Vietnamese phone patterns
    PATTERNS = {
        'mobile': r'^(\+84|84|0)[1-9][0-9]{8,9}$',
        'landline': r'^(\+84|84|0)[2-8][0-9]{8,9}$'
    }
    
    def __init__(self, phone_type='mobile'):
        self.phone_type = phone_type
        self.pattern = self.PATTERNS.get(phone_type, self.PATTERNS['mobile'])
        self.message = _(f'Enter a valid Vietnamese {phone_type} number.')
    
    def __call__(self, value):
        if not value:
            return value
        
        cleaned_phone = self.clean_phone_number(value)
        return self.validate_phone_format(cleaned_phone, self.pattern, self.message)


class InternationalPhoneValidator(PhoneValidator):
    """International phone number validator"""
    
    def __init__(self, country_code=None):
        self.country_code = country_code
    
    def __call__(self, value):
        if not value:
            return value
        
        cleaned_phone = self.clean_phone_number(value)
        
        # Basic international format validation
        if not re.match(r'^\+[1-9]\d{1,14}$', cleaned_phone):
            raise ValidationError(_('Enter a valid international phone number (e.g., +1234567890).'))
        
        # Check country code if specified
        if self.country_code:
            if not cleaned_phone.startswith(f'+{self.country_code}'):
                raise ValidationError(_(f'Phone number must start with +{self.country_code}.'))
        
        return cleaned_phone


def validate_phone_length(phone, min_length=10, max_length=15):
    """Validate phone number length"""
    if not phone:
        return phone
    
    cleaned_phone = PhoneValidator.clean_phone_number(phone)
    
    if len(cleaned_phone) < min_length:
        raise ValidationError(_(f'Phone number must be at least {min_length} digits long.'))
    
    if len(cleaned_phone) > max_length:
        raise ValidationError(_(f'Phone number must be no more than {max_length} digits long.'))
    
    return cleaned_phone


def validate_phone_prefix(phone, allowed_prefixes):
    """Validate phone number prefix"""
    if not phone:
        return phone
    
    cleaned_phone = PhoneValidator.clean_phone_number(phone)
    
    for prefix in allowed_prefixes:
        if cleaned_phone.startswith(prefix):
            return cleaned_phone
    
    raise ValidationError(_(f'Phone number must start with one of: {", ".join(allowed_prefixes)}'))


class PhoneFormatValidator:
    """Flexible phone format validator"""
    
    def __init__(self, formats=None):
        self.formats = formats or [
            r'^\+[1-9]\d{1,14}$',  # International
            r'^[1-9]\d{9,14}$',   # National without +
            r'^0[1-9]\d{8,9}$'    # Vietnamese format
        ]
    
    def __call__(self, value):
        if not value:
            return value
        
        cleaned_phone = PhoneValidator.clean_phone_number(value)
        
        for pattern in self.formats:
            if re.match(pattern, cleaned_phone):
                return cleaned_phone
        
        raise ValidationError(_('Enter a valid phone number format.'))

