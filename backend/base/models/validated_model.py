"""
Enhanced model with built-in validation capabilities
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from base.validators import (
    VietnamesePhoneValidator, VietnameseIDValidator, EnhancedEmailValidator,
    TaxCodeValidator, BankAccountValidator, CompanyNameValidator,
    AddressValidator, ProvinceCodeValidator, CurrencyValidator
)


class ValidatedModel(models.Model):
    """
    Enhanced model with built-in validation capabilities
    """
    
    class Meta:
        abstract = True
    
    def clean(self):
        """Enhanced clean method with validation"""
        super().clean()
        self._validate_business_rules()
    
    def _validate_business_rules(self):
        """Validate business-specific rules"""
        # Override in subclasses for specific business logic
        pass
    
    def validate_phone_field(self, field_name, value):
        """Validate phone field"""
        if value:
            validator = VietnamesePhoneValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value
    
    def validate_email_field(self, field_name, value):
        """Validate email field"""
        if value:
            validator = EnhancedEmailValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value
    
    def validate_tax_code_field(self, field_name, value):
        """Validate tax code field"""
        if value:
            validator = TaxCodeValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value
    
    def validate_bank_account_field(self, field_name, value):
        """Validate bank account field"""
        if value:
            validator = BankAccountValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value
    
    def validate_company_name_field(self, field_name, value):
        """Validate company name field"""
        if value:
            validator = CompanyNameValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value
    
    def validate_address_field(self, field_name, value):
        """Validate address field"""
        if value:
            validator = AddressValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value
    
    def validate_province_code_field(self, field_name, value):
        """Validate province code field"""
        if value:
            validator = ProvinceCodeValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value
    
    def validate_currency_field(self, field_name, value):
        """Validate currency field"""
        if value:
            validator = CurrencyValidator()
            try:
                validator(value)
            except ValidationError as e:
                raise ValidationError({field_name: e.message})
        return value


class ValidatedCharField(models.CharField):
    """CharField with built-in validation"""
    
    def __init__(self, *args, **kwargs):
        self.validators = kwargs.pop('validators', [])
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with validation"""
        value = super().clean(value, model_instance)
        
        for validator in self.validators:
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedEmailField(models.EmailField):
    """EmailField with enhanced validation"""
    
    def __init__(self, *args, **kwargs):
        self.business_email = kwargs.pop('business_email', False)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with email validation"""
        value = super().clean(value, model_instance)
        
        if value:
            if self.business_email:
                validator = EnhancedEmailValidator(allow_disposable=False, allow_plus_sign=False)
            else:
                validator = EnhancedEmailValidator()
            
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedPhoneField(models.CharField):
    """PhoneField with Vietnamese phone validation"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 15)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with phone validation"""
        value = super().clean(value, model_instance)
        
        if value:
            validator = VietnamesePhoneValidator()
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedTaxCodeField(models.CharField):
    """TaxCodeField with Vietnamese tax code validation"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 13)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with tax code validation"""
        value = super().clean(value, model_instance)
        
        if value:
            validator = TaxCodeValidator()
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedBankAccountField(models.CharField):
    """BankAccountField with Vietnamese bank account validation"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 19)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with bank account validation"""
        value = super().clean(value, model_instance)
        
        if value:
            validator = BankAccountValidator()
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedCompanyNameField(models.CharField):
    """CompanyNameField with company name validation"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 200)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with company name validation"""
        value = super().clean(value, model_instance)
        
        if value:
            validator = CompanyNameValidator()
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedAddressField(models.TextField):
    """AddressField with address validation"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 500)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with address validation"""
        value = super().clean(value, model_instance)
        
        if value:
            validator = AddressValidator()
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedProvinceCodeField(models.CharField):
    """ProvinceCodeField with province code validation"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with province code validation"""
        value = super().clean(value, model_instance)
        
        if value:
            validator = ProvinceCodeValidator()
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value


class ValidatedCurrencyField(models.DecimalField):
    """CurrencyField with currency validation"""
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 15)
        kwargs.setdefault('decimal_places', 2)
        super().__init__(*args, **kwargs)
    
    def clean(self, value, model_instance):
        """Clean with currency validation"""
        value = super().clean(value, model_instance)
        
        if value:
            validator = CurrencyValidator()
            try:
                value = validator(value)
            except ValidationError as e:
                raise ValidationError(e.message)
        
        return value

