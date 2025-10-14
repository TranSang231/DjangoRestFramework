"""
Examples of how to use validators in different apps
"""
from django.db import models
from django.core.exceptions import ValidationError
from rest_framework import serializers
from base.models.validated_model import (
    ValidatedModel, ValidatedEmailField, ValidatedPhoneField,
    ValidatedTaxCodeField, ValidatedBankAccountField, ValidatedCompanyNameField,
    ValidatedAddressField, ValidatedProvinceCodeField, ValidatedCurrencyField
)
from base.serializers.validated_serializer import (
    ValidatedSerializer, ValidatedWritableNestedSerializer,
    ConditionalValidatedSerializer, BulkValidatedSerializer
)
from base.validators import (
    VietnamesePhoneValidator, EnhancedEmailValidator, TaxCodeValidator,
    BankAccountValidator, CompanyNameValidator, AddressValidator,
    ProvinceCodeValidator, CurrencyValidator, DateRangeValidator,
    StringLengthValidator, VietnameseTextValidator
)


# =============================================================================
# EXAMPLE 1: ECOMMERCE APP - Customer Model with Validation
# =============================================================================

class Customer(ValidatedModel):
    """Customer model with validation"""
    
    # Basic fields with validation
    email = ValidatedEmailField(
        max_length=255,
        unique=True,
        business_email=False,  # Allow personal emails
        verbose_name="Email"
    )
    
    phone = ValidatedPhoneField(
        max_length=15,
        verbose_name="Phone Number"
    )
    
    first_name = models.CharField(
        max_length=50,
        validators=[VietnameseTextValidator()],
        verbose_name="First Name"
    )
    
    last_name = models.CharField(
        max_length=150,
        validators=[VietnameseTextValidator()],
        verbose_name="Last Name"
    )
    
    # Business fields
    company_name = ValidatedCompanyNameField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Company Name"
    )
    
    tax_code = ValidatedTaxCodeField(
        max_length=13,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Tax Code"
    )
    
    # Address fields
    address = ValidatedAddressField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Address"
    )
    
    province_code = ValidatedProvinceCodeField(
        max_length=2,
        blank=True,
        null=True,
        verbose_name="Province Code"
    )
    
    # Financial fields
    credit_limit = ValidatedCurrencyField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Credit Limit"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """Custom validation for Customer"""
        super().clean()
        
        # Business rule: If company_name is provided, tax_code is required
        if self.company_name and not self.tax_code:
            raise ValidationError({
                'tax_code': 'Tax code is required when company name is provided.'
            })
        
        # Business rule: Credit limit cannot be negative
        if self.credit_limit < 0:
            raise ValidationError({
                'credit_limit': 'Credit limit cannot be negative.'
            })


class CustomerSerializer(ValidatedSerializer):
    """Customer serializer with validation"""
    
    class Meta:
        model = Customer
        fields = [
            'id', 'email', 'phone', 'first_name', 'last_name',
            'company_name', 'tax_code', 'address', 'province_code',
            'credit_limit', 'created_at', 'updated_at'
        ]
    
    def validate(self, attrs):
        """Custom validation logic"""
        attrs = super().validate(attrs)
        
        # Business rule: Email must be unique
        email = attrs.get('email')
        if email:
            existing_customer = Customer.objects.filter(email=email).exclude(
                id=self.instance.id if self.instance else None
            ).first()
            if existing_customer:
                raise ValidationError({'email': 'Customer with this email already exists.'})
        
        return attrs


# =============================================================================
# EXAMPLE 2: HR APP - Employee Model with Validation
# =============================================================================

class Employee(ValidatedModel):
    """Employee model with validation"""
    
    # Personal information
    email = ValidatedEmailField(
        max_length=255,
        unique=True,
        business_email=True,  # Only business emails
        verbose_name="Business Email"
    )
    
    phone = ValidatedPhoneField(
        max_length=15,
        verbose_name="Phone Number"
    )
    
    first_name = models.CharField(
        max_length=50,
        validators=[VietnameseTextValidator()],
        verbose_name="First Name"
    )
    
    last_name = models.CharField(
        max_length=150,
        validators=[VietnameseTextValidator()],
        verbose_name="Last Name"
    )
    
    # Employment information
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        validators=[StringLengthValidator(min_length=3, max_length=20)],
        verbose_name="Employee ID"
    )
    
    position = models.CharField(
        max_length=100,
        validators=[VietnameseTextValidator()],
        verbose_name="Position"
    )
    
    department = models.CharField(
        max_length=100,
        validators=[VietnameseTextValidator()],
        verbose_name="Department"
    )
    
    # Salary information
    salary = ValidatedCurrencyField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Salary"
    )
    
    # Personal information
    date_of_birth = models.DateField(
        validators=[DateRangeValidator(allow_future=False)],
        verbose_name="Date of Birth"
    )
    
    address = ValidatedAddressField(
        max_length=500,
        verbose_name="Address"
    )
    
    province_code = ValidatedProvinceCodeField(
        max_length=2,
        verbose_name="Province Code"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """Custom validation for Employee"""
        super().clean()
        
        # Business rule: Employee ID must be unique
        if self.employee_id:
            existing_employee = Employee.objects.filter(
                employee_id=self.employee_id
            ).exclude(id=self.id).first()
            if existing_employee:
                raise ValidationError({
                    'employee_id': 'Employee with this ID already exists.'
                })
        
        # Business rule: Salary must be positive
        if self.salary <= 0:
            raise ValidationError({
                'salary': 'Salary must be positive.'
            })


class EmployeeSerializer(ValidatedSerializer):
    """Employee serializer with validation"""
    
    class Meta:
        model = Employee
        fields = [
            'id', 'email', 'phone', 'first_name', 'last_name',
            'employee_id', 'position', 'department', 'salary',
            'date_of_birth', 'address', 'province_code',
            'created_at', 'updated_at'
        ]
    
    def validate_employee_id(self, value):
        """Validate employee ID format"""
        if value:
            # Custom validation for employee ID format
            if not value.isalnum():
                raise ValidationError('Employee ID must contain only letters and numbers.')
        return value


# =============================================================================
# EXAMPLE 3: BUSINESS APP - Company Model with Validation
# =============================================================================

class Company(ValidatedModel):
    """Company model with validation"""
    
    # Company information
    name = ValidatedCompanyNameField(
        max_length=200,
        unique=True,
        verbose_name="Company Name"
    )
    
    tax_code = ValidatedTaxCodeField(
        max_length=13,
        unique=True,
        verbose_name="Tax Code"
    )
    
    business_license = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Business License"
    )
    
    # Contact information
    email = ValidatedEmailField(
        max_length=255,
        unique=True,
        business_email=True,
        verbose_name="Business Email"
    )
    
    phone = ValidatedPhoneField(
        max_length=15,
        verbose_name="Phone Number"
    )
    
    address = ValidatedAddressField(
        max_length=500,
        verbose_name="Address"
    )
    
    province_code = ValidatedProvinceCodeField(
        max_length=2,
        verbose_name="Province Code"
    )
    
    # Financial information
    capital = ValidatedCurrencyField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Registered Capital"
    )
    
    # Bank information
    bank_name = models.CharField(
        max_length=100,
        verbose_name="Bank Name"
    )
    
    bank_account = ValidatedBankAccountField(
        max_length=19,
        verbose_name="Bank Account"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """Custom validation for Company"""
        super().clean()
        
        # Business rule: Tax code and business license must be unique
        if self.tax_code:
            existing_company = Company.objects.filter(
                tax_code=self.tax_code
            ).exclude(id=self.id).first()
            if existing_company:
                raise ValidationError({
                    'tax_code': 'Company with this tax code already exists.'
                })
        
        if self.business_license:
            existing_company = Company.objects.filter(
                business_license=self.business_license
            ).exclude(id=self.id).first()
            if existing_company:
                raise ValidationError({
                    'business_license': 'Company with this business license already exists.'
                })


class CompanySerializer(ValidatedSerializer):
    """Company serializer with validation"""
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'tax_code', 'business_license', 'email', 'phone',
            'address', 'province_code', 'capital', 'bank_name', 'bank_account',
            'created_at', 'updated_at'
        ]
    
    def validate_business_license(self, value):
        """Validate business license format"""
        if value:
            # Custom validation for business license format
            if not value.isalnum():
                raise ValidationError('Business license must contain only letters and numbers.')
        return value


# =============================================================================
# EXAMPLE 4: CONDITIONAL VALIDATION
# =============================================================================

class ConditionalValidationExample(ValidatedModel):
    """Example of conditional validation"""
    
    user_type = models.CharField(
        max_length=20,
        choices=[
            ('individual', 'Individual'),
            ('company', 'Company'),
        ],
        verbose_name="User Type"
    )
    
    # Individual fields
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="First Name"
    )
    
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Last Name"
    )
    
    # Company fields
    company_name = ValidatedCompanyNameField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Company Name"
    )
    
    tax_code = ValidatedTaxCodeField(
        max_length=13,
        blank=True,
        null=True,
        verbose_name="Tax Code"
    )
    
    def clean(self):
        """Custom validation with conditions"""
        super().clean()
        
        if self.user_type == 'individual':
            if not self.first_name or not self.last_name:
                raise ValidationError({
                    'first_name': 'First name is required for individual users.',
                    'last_name': 'Last name is required for individual users.'
                })
            
            if self.company_name or self.tax_code:
                raise ValidationError({
                    'company_name': 'Company name should not be provided for individual users.',
                    'tax_code': 'Tax code should not be provided for individual users.'
                })
        
        elif self.user_type == 'company':
            if not self.company_name:
                raise ValidationError({
                    'company_name': 'Company name is required for company users.'
                })
            
            if self.first_name or self.last_name:
                raise ValidationError({
                    'first_name': 'First name should not be provided for company users.',
                    'last_name': 'Last name should not be provided for company users.'
                })


class ConditionalValidationSerializer(ConditionalValidatedSerializer):
    """Serializer with conditional validation"""
    
    class Meta:
        model = ConditionalValidationExample
        fields = [
            'id', 'user_type', 'first_name', 'last_name',
            'company_name', 'tax_code'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add conditional validators
        self.add_conditional_validator(
            'first_name',
            'user_type',
            'individual',
            StringLengthValidator(min_length=2, max_length=50)
        )
        
        self.add_conditional_validator(
            'company_name',
            'user_type',
            'company',
            CompanyNameValidator()
        )


# =============================================================================
# EXAMPLE 5: BULK VALIDATION
# =============================================================================

class BulkValidationExample(ValidatedModel):
    """Example of bulk validation"""
    
    name = models.CharField(
        max_length=100,
        validators=[VietnameseTextValidator()],
        verbose_name="Name"
    )
    
    email = ValidatedEmailField(
        max_length=255,
        unique=True,
        verbose_name="Email"
    )
    
    phone = ValidatedPhoneField(
        max_length=15,
        verbose_name="Phone Number"
    )


class BulkValidationSerializer(BulkValidatedSerializer):
    """Serializer for bulk operations"""
    
    class Meta:
        model = BulkValidationExample
        fields = ['id', 'name', 'email', 'phone']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add bulk validators
        self.add_bulk_validator(self._validate_unique_emails)
    
    def _validate_unique_emails(self, data_list):
        """Validate unique emails in bulk data"""
        emails = [item.get('email') for item in data_list if item.get('email')]
        
        # Check for duplicates within the bulk data
        if len(emails) != len(set(emails)):
            raise ValidationError('Duplicate emails found in bulk data.')
        
        # Check against existing records
        existing_emails = BulkValidationExample.objects.filter(
            email__in=emails
        ).values_list('email', flat=True)
        
        if existing_emails:
            raise ValidationError(f'Emails already exist: {list(existing_emails)}')
        
        return data_list

