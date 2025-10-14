"""
Enhanced serializer with built-in validation capabilities
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from base.validators import (
    VietnamesePhoneValidator, VietnameseIDValidator, StrongPasswordValidator,
    EnhancedEmailValidator, BusinessEmailValidator, DateRangeValidator,
    DateTimeRangeValidator, StringLengthValidator, AlphanumericValidator,
    VietnameseTextValidator, TaxCodeValidator, BankAccountValidator,
    CompanyNameValidator, AddressValidator, ProvinceCodeValidator,
    CurrencyValidator, PercentageValidator
)


class ValidatedSerializer(serializers.ModelSerializer):
    """
    Enhanced serializer with built-in validation capabilities
    """
    
    # Common field validators
    phone_validator = VietnamesePhoneValidator()
    email_validator = EnhancedEmailValidator()
    business_email_validator = BusinessEmailValidator()
    password_validator = StrongPasswordValidator()
    tax_code_validator = TaxCodeValidator()
    bank_account_validator = BankAccountValidator()
    company_name_validator = CompanyNameValidator()
    address_validator = AddressValidator()
    province_code_validator = ProvinceCodeValidator()
    currency_validator = CurrencyValidator()
    percentage_validator = PercentageValidator()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_field_validators()
    
    def _setup_field_validators(self):
        """Setup field validators based on field names and types"""
        for field_name, field in self.fields.items():
            if hasattr(field, 'validators'):
                # Add common validators based on field name patterns
                if 'phone' in field_name.lower():
                    field.validators.append(self.phone_validator)
                elif 'email' in field_name.lower():
                    if 'business' in field_name.lower():
                        field.validators.append(self.business_email_validator)
                    else:
                        field.validators.append(self.email_validator)
                elif 'password' in field_name.lower():
                    field.validators.append(self.password_validator)
                elif 'tax_code' in field_name.lower() or 'ma_so_thue' in field_name.lower():
                    field.validators.append(self.tax_code_validator)
                elif 'bank_account' in field_name.lower() or 'so_tai_khoan' in field_name.lower():
                    field.validators.append(self.bank_account_validator)
                elif 'company_name' in field_name.lower() or 'ten_cong_ty' in field_name.lower():
                    field.validators.append(self.company_name_validator)
                elif 'address' in field_name.lower() or 'dia_chi' in field_name.lower():
                    field.validators.append(self.address_validator)
                elif 'province' in field_name.lower() or 'tinh' in field_name.lower():
                    field.validators.append(self.province_code_validator)
                elif 'amount' in field_name.lower() or 'so_tien' in field_name.lower():
                    field.validators.append(self.currency_validator)
                elif 'percentage' in field_name.lower() or 'phan_tram' in field_name.lower():
                    field.validators.append(self.percentage_validator)
    
    def validate(self, attrs):
        """Enhanced validation with business logic"""
        attrs = super().validate(attrs)
        
        # Add custom validation logic here
        self._validate_business_rules(attrs)
        
        return attrs
    
    def _validate_business_rules(self, attrs):
        """Validate business-specific rules"""
        # Override in subclasses for specific business logic
        pass
    
    def validate_phone(self, value):
        """Validate phone number"""
        if value:
            return self.phone_validator(value)
        return value
    
    def validate_email(self, value):
        """Validate email"""
        if value:
            return self.email_validator(value)
        return value
    
    def validate_password(self, value):
        """Validate password"""
        if value:
            return self.password_validator(value)
        return value
    
    def validate_tax_code(self, value):
        """Validate tax code"""
        if value:
            return self.tax_code_validator(value)
        return value
    
    def validate_bank_account(self, value):
        """Validate bank account"""
        if value:
            return self.bank_account_validator(value)
        return value
    
    def validate_company_name(self, value):
        """Validate company name"""
        if value:
            return self.company_name_validator(value)
        return value
    
    def validate_address(self, value):
        """Validate address"""
        if value:
            return self.address_validator(value)
        return value
    
    def validate_province_code(self, value):
        """Validate province code"""
        if value:
            return self.province_code_validator(value)
        return value
    
    def validate_amount(self, value):
        """Validate currency amount"""
        if value:
            return self.currency_validator(value)
        return value
    
    def validate_percentage(self, value):
        """Validate percentage"""
        if value:
            return self.percentage_validator(value)
        return value


class ValidatedWritableNestedSerializer(ValidatedSerializer):
    """
    Enhanced writable nested serializer with validation
    """
    
    def __init__(self, *args, **kwargs):
        # Import here to avoid circular imports
        from base.serializers.writable_nested import WritableNestedSerializer
        WritableNestedSerializer.__init__(self, *args, **kwargs)
        self._setup_field_validators()
    
    def create(self, validated_data):
        """Create with validation"""
        from base.serializers.writable_nested import WritableNestedSerializer
        return WritableNestedSerializer.create(self, validated_data)
    
    def update(self, instance, validated_data):
        """Update with validation"""
        from base.serializers.writable_nested import WritableNestedSerializer
        return WritableNestedSerializer.update(self, instance, validated_data)
    
    def to_internal_value(self, data):
        """Convert to internal value with validation"""
        from base.serializers.writable_nested import WritableNestedSerializer
        return WritableNestedSerializer.to_internal_value(self, data)


class ConditionalValidatedSerializer(ValidatedSerializer):
    """
    Serializer with conditional validation
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conditional_validators = {}
    
    def add_conditional_validator(self, field_name, condition_field, condition_value, validator):
        """Add conditional validator"""
        if field_name not in self.conditional_validators:
            self.conditional_validators[field_name] = []
        
        self.conditional_validators[field_name].append({
            'condition_field': condition_field,
            'condition_value': condition_value,
            'validator': validator
        })
    
    def validate(self, attrs):
        """Validate with conditional rules"""
        attrs = super().validate(attrs)
        
        # Apply conditional validators
        for field_name, validators in self.conditional_validators.items():
            if field_name in attrs:
                for validator_config in validators:
                    condition_field = validator_config['condition_field']
                    condition_value = validator_config['condition_value']
                    validator = validator_config['validator']
                    
                    if attrs.get(condition_field) == condition_value:
                        try:
                            attrs[field_name] = validator(attrs[field_name])
                        except DjangoValidationError as e:
                            raise ValidationError({field_name: e.message})
        
        return attrs


class BulkValidatedSerializer(ValidatedSerializer):
    """
    Serializer for bulk operations with validation
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bulk_validators = []
    
    def add_bulk_validator(self, validator):
        """Add bulk validator"""
        self.bulk_validators.append(validator)
    
    def validate_bulk_data(self, data_list):
        """Validate list of data"""
        validated_data_list = []
        errors = {}
        
        for index, data in enumerate(data_list):
            try:
                serializer = self.__class__(data=data)
                if serializer.is_valid():
                    validated_data_list.append(serializer.validated_data)
                else:
                    errors[index] = serializer.errors
            except Exception as e:
                errors[index] = {'non_field_errors': [str(e)]}
        
        if errors:
            raise ValidationError({'bulk_errors': errors})
        
        return validated_data_list


class AuditValidatedSerializer(ValidatedSerializer):
    """
    Serializer with audit trail validation
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audit_fields = ['created_by', 'updated_by', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        """Validate with audit trail"""
        attrs = super().validate(attrs)
        
        # Add audit fields if not present
        if hasattr(self, 'context') and 'request' in self.context:
            request = self.context['request']
            if hasattr(request, 'user') and request.user.is_authenticated:
                if not self.instance:  # Creating new instance
                    attrs.setdefault('created_by', request.user)
                attrs.setdefault('updated_by', request.user)
        
        return attrs

