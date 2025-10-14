"""
Date and time validation utilities
"""
from datetime import datetime, date, time
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class DateRangeValidator:
    """Validator for date ranges"""
    
    def __init__(self, min_date=None, max_date=None, allow_future=True, allow_past=True):
        self.min_date = min_date
        self.max_date = max_date
        self.allow_future = allow_future
        self.allow_past = allow_past
    
    def __call__(self, value):
        if not value:
            return value
        
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError(_('Invalid date format. Use YYYY-MM-DD.'))
        
        today = timezone.now().date()
        
        # Check if date is in the past when not allowed
        if not self.allow_past and value < today:
            raise ValidationError(_('Date cannot be in the past.'))
        
        # Check if date is in the future when not allowed
        if not self.allow_future and value > today:
            raise ValidationError(_('Date cannot be in the future.'))
        
        # Check minimum date
        if self.min_date and value < self.min_date:
            raise ValidationError(_(f'Date must be after {self.min_date}.'))
        
        # Check maximum date
        if self.max_date and value > self.max_date:
            raise ValidationError(_(f'Date must be before {self.max_date}.'))
        
        return value


class DateTimeRangeValidator:
    """Validator for datetime ranges"""
    
    def __init__(self, min_datetime=None, max_datetime=None, allow_future=True, allow_past=True):
        self.min_datetime = min_datetime
        self.max_datetime = max_datetime
        self.allow_future = allow_future
        self.allow_past = allow_past
    
    def __call__(self, value):
        if not value:
            return value
        
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise ValidationError(_('Invalid datetime format. Use ISO format.'))
        
        now = timezone.now()
        
        # Check if datetime is in the past when not allowed
        if not self.allow_past and value < now:
            raise ValidationError(_('Datetime cannot be in the past.'))
        
        # Check if datetime is in the future when not allowed
        if not self.allow_future and value > now:
            raise ValidationError(_('Datetime cannot be in the future.'))
        
        # Check minimum datetime
        if self.min_datetime and value < self.min_datetime:
            raise ValidationError(_(f'Datetime must be after {self.min_datetime}.'))
        
        # Check maximum datetime
        if self.max_datetime and value > self.max_datetime:
            raise ValidationError(_(f'Datetime must be before {self.max_datetime}.'))
        
        return value


class TimeRangeValidator:
    """Validator for time ranges"""
    
    def __init__(self, min_time=None, max_time=None):
        self.min_time = min_time
        self.max_time = max_time
    
    def __call__(self, value):
        if not value:
            return value
        
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%H:%M:%S').time()
            except ValueError:
                try:
                    value = datetime.strptime(value, '%H:%M').time()
                except ValueError:
                    raise ValidationError(_('Invalid time format. Use HH:MM or HH:MM:SS.'))
        
        # Check minimum time
        if self.min_time and value < self.min_time:
            raise ValidationError(_(f'Time must be after {self.min_time}.'))
        
        # Check maximum time
        if self.max_time and value > self.max_time:
            raise ValidationError(_(f'Time must be before {self.max_time}.'))
        
        return value


class WorkHoursValidator:
    """Validator for work hours (e.g., 9 AM to 5 PM)"""
    
    def __init__(self, start_hour=9, end_hour=17):
        self.start_time = time(start_hour, 0)
        self.end_time = time(end_hour, 0)
    
    def __call__(self, value):
        if not value:
            return value
        
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%H:%M:%S').time()
            except ValueError:
                try:
                    value = datetime.strptime(value, '%H:%M').time()
                except ValueError:
                    raise ValidationError(_('Invalid time format.'))
        
        if value < self.start_time or value > self.end_time:
            raise ValidationError(_(f'Time must be between {self.start_time} and {self.end_time}.'))
        
        return value


class AgeValidator:
    """Validator for age restrictions"""
    
    def __init__(self, min_age=None, max_age=None):
        self.min_age = min_age
        self.max_age = max_age
    
    def __call__(self, value):
        if not value:
            return value
        
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError(_('Invalid date format. Use YYYY-MM-DD.'))
        
        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if self.min_age and age < self.min_age:
            raise ValidationError(_(f'Age must be at least {self.min_age} years old.'))
        
        if self.max_age and age > self.max_age:
            raise ValidationError(_(f'Age must be no more than {self.max_age} years old.'))
        
        return value


def validate_date_format(value, date_format='%Y-%m-%d'):
    """Validate date format"""
    if not value:
        return value
    
    if isinstance(value, str):
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValidationError(_(f'Invalid date format. Use {date_format}.'))
    
    return value


def validate_datetime_format(value, datetime_format='%Y-%m-%d %H:%M:%S'):
    """Validate datetime format"""
    if not value:
        return value
    
    if isinstance(value, str):
        try:
            datetime.strptime(value, datetime_format)
        except ValueError:
            raise ValidationError(_(f'Invalid datetime format. Use {datetime_format}.'))
    
    return value


class BusinessDayValidator:
    """Validator for business days (Monday to Friday)"""
    
    def __call__(self, value):
        if not value:
            return value
        
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError(_('Invalid date format.'))
        
        # Check if it's a weekday (Monday=0, Sunday=6)
        if value.weekday() >= 5:  # Saturday or Sunday
            raise ValidationError(_('Date must be a business day (Monday to Friday).'))
        
        return value

