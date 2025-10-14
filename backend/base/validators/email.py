"""
Email validation utilities
"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class EnhancedEmailValidator(EmailValidator):
    """Enhanced email validator with additional checks"""
    
    def __init__(self, allow_disposable=False, allow_plus_sign=True):
        super().__init__()
        self.allow_disposable = allow_disposable
        self.allow_plus_sign = allow_plus_sign
    
    def __call__(self, value):
        # Basic email validation
        super().__call__(value)
        
        # Check for disposable emails if not allowed
        if not self.allow_disposable:
            self._check_disposable_email(value)
        
        # Check for plus sign if not allowed
        if not self.allow_plus_sign and '+' in value:
            raise ValidationError(_('Email addresses with plus signs are not allowed.'))
        
        return value
    
    def _check_disposable_email(self, email):
        """Check if email is from a disposable email service"""
        disposable_domains = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'temp-mail.org', 'throwaway.email'
        ]
        
        domain = email.split('@')[1].lower()
        if domain in disposable_domains:
            raise ValidationError(_('Disposable email addresses are not allowed.'))


class BusinessEmailValidator(EnhancedEmailValidator):
    """Validator for business email addresses"""
    
    def __init__(self):
        super().__init__(allow_disposable=False, allow_plus_sign=False)
    
    def __call__(self, value):
        super().__call__(value)
        
        # Check for business domain patterns
        domain = value.split('@')[1].lower()
        
        # Common personal email providers
        personal_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'live.com', 'msn.com', 'aol.com', 'icloud.com'
        ]
        
        if domain in personal_domains:
            raise ValidationError(_('Business email address is required.'))
        
        return value


def validate_email_domain(value, allowed_domains=None, blocked_domains=None):
    """Validate email domain against allowed/blocked lists"""
    if not value or '@' not in value:
        raise ValidationError(_('Invalid email format.'))
    
    domain = value.split('@')[1].lower()
    
    if allowed_domains and domain not in allowed_domains:
        raise ValidationError(_(f'Email domain must be one of: {", ".join(allowed_domains)}'))
    
    if blocked_domains and domain in blocked_domains:
        raise ValidationError(_(f'Email domain {domain} is not allowed.'))
    
    return value


def validate_email_format(value):
    """Basic email format validation"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError(_('Enter a valid email address.'))
    return value

