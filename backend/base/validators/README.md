# Hệ thống Validator cho Backend Django

## Tổng quan

Hệ thống validator này cung cấp các công cụ validation toàn diện cho backend Django, bao gồm:

- **Common Validators**: Các validator cơ bản cho string, số, email, phone
- **Business Validators**: Các validator cho nghiệp vụ Việt Nam (mã số thuế, tài khoản ngân hàng, v.v.)
- **File Validators**: Validation cho file upload
- **Date Validators**: Validation cho ngày tháng
- **Enhanced Serializers**: Serializer với validation tích hợp
- **Validated Models**: Model với validation tự động

## Cài đặt và Sử dụng

### 1. Import Validators

```python
from base.validators import (
    VietnamesePhoneValidator, EnhancedEmailValidator, TaxCodeValidator,
    BankAccountValidator, CompanyNameValidator, AddressValidator,
    ProvinceCodeValidator, CurrencyValidator, DateRangeValidator,
    StringLengthValidator, VietnameseTextValidator
)
```

### 2. Sử dụng trong Models

```python
from base.models.validated_model import (
    ValidatedModel, ValidatedEmailField, ValidatedPhoneField,
    ValidatedTaxCodeField, ValidatedBankAccountField
)

class Customer(ValidatedModel):
    email = ValidatedEmailField(max_length=255, unique=True)
    phone = ValidatedPhoneField(max_length=15)
    tax_code = ValidatedTaxCodeField(max_length=13, blank=True, null=True)
    bank_account = ValidatedBankAccountField(max_length=19, blank=True, null=True)
```

### 3. Sử dụng trong Serializers

```python
from base.serializers.validated_serializer import ValidatedSerializer

class CustomerSerializer(ValidatedSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone', 'tax_code', 'bank_account']
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Custom validation logic here
        return attrs
```

## Các Loại Validator

### 1. Common Validators

#### VietnamesePhoneValidator
```python
from base.validators import VietnamesePhoneValidator

validator = VietnamesePhoneValidator()
validator('0123456789')  # Valid
validator('+84123456789')  # Valid
validator('123456789')  # Invalid
```

#### EnhancedEmailValidator
```python
from base.validators import EnhancedEmailValidator

# Basic email validation
validator = EnhancedEmailValidator()
validator('user@example.com')  # Valid

# Business email validation (no disposable emails, no plus signs)
business_validator = EnhancedEmailValidator(allow_disposable=False, allow_plus_sign=False)
business_validator('user@company.com')  # Valid
business_validator('user+tag@gmail.com')  # Invalid
```

#### StrongPasswordValidator
```python
from base.validators import StrongPasswordValidator

validator = StrongPasswordValidator(
    min_length=8,
    require_uppercase=True,
    require_lowercase=True,
    require_numbers=True,
    require_special_chars=True
)
validator('MyPassword123!')  # Valid
validator('weak')  # Invalid
```

### 2. Business Validators

#### TaxCodeValidator
```python
from base.validators import TaxCodeValidator

validator = TaxCodeValidator()
validator('0123456789')  # Valid (10 digits)
validator('0123456789012')  # Valid (13 digits)
validator('123456789')  # Invalid (9 digits)
```

#### BankAccountValidator
```python
from base.validators import BankAccountValidator

validator = BankAccountValidator()
validator('9704151234567890')  # Valid
validator('1234567890')  # Invalid
```

#### CompanyNameValidator
```python
from base.validators import CompanyNameValidator

validator = CompanyNameValidator()
validator('Công ty TNHH ABC')  # Valid
validator('Company ABC Ltd.')  # Valid
validator('Company@#$%')  # Invalid
```

### 3. File Validators

#### ImageValidator
```python
from base.validators import ImageValidator

validator = ImageValidator(max_size_mb=5)
# Use in model field
avatar = models.ImageField(
    upload_to='avatars/',
    validators=[ImageValidator(max_size_mb=5)]
)
```

#### DocumentValidator
```python
from base.validators import DocumentValidator

validator = DocumentValidator(max_size_mb=10)
# Use in model field
document = models.FileField(
    upload_to='documents/',
    validators=[DocumentValidator(max_size_mb=10)]
)
```

### 4. Date Validators

#### DateRangeValidator
```python
from base.validators import DateRangeValidator
from datetime import date

validator = DateRangeValidator(
    min_date=date(2020, 1, 1),
    max_date=date(2030, 12, 31),
    allow_future=True,
    allow_past=True
)
validator(date(2023, 6, 15))  # Valid
validator(date(2019, 1, 1))  # Invalid (before min_date)
```

#### AgeValidator
```python
from base.validators import AgeValidator

validator = AgeValidator(min_age=18, max_age=65)
validator(date(1990, 1, 1))  # Valid
validator(date(2010, 1, 1))  # Invalid (too young)
```

### 5. String Validators

#### VietnameseTextValidator
```python
from base.validators import VietnameseTextValidator

validator = VietnameseTextValidator()
validator('Nguyễn Văn An')  # Valid
validator('John Doe')  # Valid
validator('User@123')  # Invalid
```

#### StringLengthValidator
```python
from base.validators import StringLengthValidator

validator = StringLengthValidator(min_length=3, max_length=50)
validator('Hello')  # Valid
validator('Hi')  # Invalid (too short)
```

## Sử dụng trong Serializers

### 1. ValidatedSerializer

```python
from base.serializers.validated_serializer import ValidatedSerializer

class CustomerSerializer(ValidatedSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone', 'name']
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        # Custom validation logic
        return attrs
```

### 2. ConditionalValidatedSerializer

```python
from base.serializers.validated_serializer import ConditionalValidatedSerializer

class UserSerializer(ConditionalValidatedSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_type', 'first_name', 'company_name']
    
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
```

### 3. BulkValidatedSerializer

```python
from base.serializers.validated_serializer import BulkValidatedSerializer

class BulkCustomerSerializer(BulkValidatedSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone', 'name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bulk_validator(self._validate_unique_emails)
    
    def _validate_unique_emails(self, data_list):
        # Custom bulk validation logic
        emails = [item.get('email') for item in data_list if item.get('email')]
        if len(emails) != len(set(emails)):
            raise ValidationError('Duplicate emails found in bulk data.')
        return data_list
```

## Sử dụng trong Models

### 1. ValidatedModel

```python
from base.models.validated_model import ValidatedModel

class Customer(ValidatedModel):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    
    def clean(self):
        super().clean()
        # Custom validation logic
        if self.email and self.phone:
            # Check if customer already exists
            existing = Customer.objects.filter(
                email=self.email,
                phone=self.phone
            ).exclude(id=self.id).first()
            if existing:
                raise ValidationError('Customer with this email and phone already exists.')
```

### 2. Custom Validated Fields

```python
from base.models.validated_model import (
    ValidatedEmailField, ValidatedPhoneField, ValidatedTaxCodeField
)

class Company(ValidatedModel):
    email = ValidatedEmailField(max_length=255, unique=True)
    phone = ValidatedPhoneField(max_length=15)
    tax_code = ValidatedTaxCodeField(max_length=13, unique=True)
```

## Best Practices

### 1. Validation Layers

1. **Model Level**: Basic field validation, business rules
2. **Serializer Level**: API validation, data transformation
3. **View Level**: Permission validation, business logic

### 2. Error Handling

```python
try:
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)
except ValidationError as e:
    return Response({'error': str(e)}, status=400)
```

### 3. Custom Validators

```python
def validate_unique_email(value):
    """Custom validator for unique email"""
    if Customer.objects.filter(email=value).exists():
        raise ValidationError('Email already exists.')
    return value

class Customer(ValidatedModel):
    email = models.EmailField(
        max_length=255,
        validators=[validate_unique_email]
    )
```

### 4. Testing Validators

```python
from django.test import TestCase
from base.validators import VietnamesePhoneValidator

class ValidatorTestCase(TestCase):
    def test_vietnamese_phone_validator(self):
        validator = VietnamesePhoneValidator()
        
        # Valid cases
        self.assertIsNone(validator('0123456789'))
        self.assertIsNone(validator('+84123456789'))
        
        # Invalid cases
        with self.assertRaises(ValidationError):
            validator('123456789')
        with self.assertRaises(ValidationError):
            validator('invalid')
```

## Troubleshooting

### 1. Common Issues

- **Import Errors**: Đảm bảo import đúng path
- **Validation Errors**: Kiểm tra error messages để debug
- **Performance**: Sử dụng validation một cách hợp lý, tránh validation quá nhiều

### 2. Debug Validation

```python
# Debug serializer validation
serializer = CustomerSerializer(data=request.data)
if not serializer.is_valid():
    print("Validation errors:", serializer.errors)
    for field, errors in serializer.errors.items():
        print(f"Field {field}: {errors}")
```

### 3. Custom Error Messages

```python
class CustomVietnamesePhoneValidator(VietnamesePhoneValidator):
    message = 'Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại Việt Nam.'
    code = 'invalid_vietnamese_phone'
```

## Kết luận

Hệ thống validator này cung cấp một giải pháp toàn diện cho validation trong Django backend, đặc biệt phù hợp với các ứng dụng Việt Nam. Sử dụng đúng cách sẽ giúp:

- Tăng cường bảo mật và tính toàn vẹn dữ liệu
- Cải thiện trải nghiệm người dùng với error messages rõ ràng
- Giảm thiểu lỗi trong quá trình phát triển
- Dễ dàng maintain và mở rộng

