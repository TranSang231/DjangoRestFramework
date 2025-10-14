"""
Business-specific validation utilities
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TaxCodeValidator:
    """Validator for Vietnamese tax codes (Mã số thuế)"""
    
    def __call__(self, value):
        if not value:
            return value
        
        # Vietnamese tax code pattern (10-13 digits)
        tax_code_pattern = r'^[0-9]{10,13}$'
        
        if not re.match(tax_code_pattern, value):
            raise ValidationError(_('Tax code must be 10-13 digits.'))
        
        # Additional validation for tax code format
        if len(value) == 10:
            # 10-digit tax code validation
            if not self._validate_10_digit_tax_code(value):
                raise ValidationError(_('Invalid tax code format.'))
        elif len(value) == 13:
            # 13-digit tax code validation
            if not self._validate_13_digit_tax_code(value):
                raise ValidationError(_('Invalid tax code format.'))
        
        return value
    
    def _validate_10_digit_tax_code(self, code):
        """Validate 10-digit tax code"""
        # Basic format check - can be enhanced with actual algorithm
        return len(code) == 10 and code.isdigit()
    
    def _validate_13_digit_tax_code(self, code):
        """Validate 13-digit tax code"""
        # Basic format check - can be enhanced with actual algorithm
        return len(code) == 13 and code.isdigit()


class BusinessLicenseValidator:
    """Validator for business license numbers"""
    
    def __call__(self, value):
        if not value:
            return value
        
        # Business license pattern (alphanumeric with specific format)
        license_pattern = r'^[0-9]{2}[A-Z]{1,2}[0-9]{6,8}$'
        
        if not re.match(license_pattern, value):
            raise ValidationError(_('Business license must be in format: 2 digits + 1-2 letters + 6-8 digits.'))
        
        return value


class BankAccountValidator:
    """Validator for Vietnamese bank account numbers"""
    
    def __init__(self, allowed_banks=None):
        self.allowed_banks = allowed_banks or [
            '970415', '970416', '970403', '970422', '970405',  # Vietcombank
            '970436', '970437', '970438', '970439', '970440',  # BIDV
            '970422', '970423', '970424', '970425', '970426',  # Agribank
            '970427', '970428', '970429', '970430', '970431',  # Techcombank
        ]
    
    def __call__(self, value):
        if not value:
            return value
        
        # Bank account pattern (6 digits + 8-13 digits)
        account_pattern = r'^[0-9]{6}[0-9]{8,13}$'
        
        if not re.match(account_pattern, value):
            raise ValidationError(_('Bank account must be 14-19 digits (6-digit bank code + 8-13 digit account number).'))
        
        # Check bank code
        bank_code = value[:6]
        if self.allowed_banks and bank_code not in self.allowed_banks:
            raise ValidationError(_(f'Bank code {bank_code} is not supported.'))
        
        return value


class CreditCardValidator:
    """Validator for credit card numbers"""
    
    def __call__(self, value):
        if not value:
            return value
        
        # Remove spaces and dashes
        cleaned_value = re.sub(r'[-\s]', '', value)
        
        # Check if all digits
        if not cleaned_value.isdigit():
            raise ValidationError(_('Credit card number must contain only digits.'))
        
        # Check length (13-19 digits)
        if len(cleaned_value) < 13 or len(cleaned_value) > 19:
            raise ValidationError(_('Credit card number must be 13-19 digits long.'))
        
        # Luhn algorithm validation
        if not self._luhn_validate(cleaned_value):
            raise ValidationError(_('Invalid credit card number.'))
        
        return cleaned_value
    
    def _luhn_validate(self, card_number):
        """Validate credit card using Luhn algorithm"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0


class CompanyNameValidator:
    """Validator for company names"""
    
    def __init__(self, min_length=2, max_length=200):
        self.min_length = min_length
        self.max_length = max_length
    
    def __call__(self, value):
        if not value:
            return value
        
        # Check length
        if len(value) < self.min_length:
            raise ValidationError(_(f'Company name must be at least {self.min_length} characters long.'))
        
        if len(value) > self.max_length:
            raise ValidationError(_(f'Company name must be no more than {self.max_length} characters long.'))
        
        # Check for valid characters (Vietnamese + English + numbers + common symbols)
        name_pattern = r'^[a-zA-ZÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐĐđ0-9\s\.,\-\(\)&]+$'
        
        if not re.match(name_pattern, value):
            raise ValidationError(_('Company name contains invalid characters.'))
        
        return value


class AddressValidator:
    """Validator for Vietnamese addresses"""
    
    def __init__(self, max_length=500):
        self.max_length = max_length
    
    def __call__(self, value):
        if not value:
            return value
        
        # Check length
        if len(value) > self.max_length:
            raise ValidationError(_(f'Address must be no more than {self.max_length} characters long.'))
        
        # Check for valid characters
        address_pattern = r'^[a-zA-ZÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐĐđ0-9\s\.,\-\(\)\/#]+$'
        
        if not re.match(address_pattern, value):
            raise ValidationError(_('Address contains invalid characters.'))
        
        return value


class ProvinceCodeValidator:
    """Validator for Vietnamese province codes"""
    
    def __init__(self):
        self.valid_codes = [
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
            '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
            '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
            '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
            '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
            '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
            '91', '92', '93', '94', '95', '96', '97', '98', '99'
        ]
    
    def __call__(self, value):
        if not value:
            return value
        
        if value not in self.valid_codes:
            raise ValidationError(_('Invalid province code.'))
        
        return value


class CurrencyValidator:
    """Validator for currency amounts"""
    
    def __init__(self, min_amount=0, max_amount=None, allow_negative=False):
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.allow_negative = allow_negative
    
    def __call__(self, value):
        if not value:
            return value
        
        try:
            amount = float(value)
        except (ValueError, TypeError):
            raise ValidationError(_('Invalid currency amount.'))
        
        if not self.allow_negative and amount < 0:
            raise ValidationError(_('Currency amount cannot be negative.'))
        
        if amount < self.min_amount:
            raise ValidationError(_(f'Currency amount must be at least {self.min_amount}.'))
        
        if self.max_amount and amount > self.max_amount:
            raise ValidationError(_(f'Currency amount must be no more than {self.max_amount}.'))
        
        return amount


class PercentageValidator:
    """Validator for percentage values"""
    
    def __init__(self, min_percentage=0, max_percentage=100):
        self.min_percentage = min_percentage
        self.max_percentage = max_percentage
    
    def __call__(self, value):
        if not value:
            return value
        
        try:
            percentage = float(value)
        except (ValueError, TypeError):
            raise ValidationError(_('Invalid percentage value.'))
        
        if percentage < self.min_percentage:
            raise ValidationError(_(f'Percentage must be at least {self.min_percentage}%.'))
        
        if percentage > self.max_percentage:
            raise ValidationError(_(f'Percentage must be no more than {self.max_percentage}%.'))
        
        return percentage

