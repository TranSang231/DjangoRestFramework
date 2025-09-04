from django.shortcuts import render
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, "index.html", {"message": "Chào mừng bạn đến với Django!"})

class AboutView(View):
    def get(self, request):
        return render(request, "about.html", {"description": "Đây là trang giới thiệu Django."})

class ContactView(View):
    def get(self, request):
        return render(request, "contact.html", {"email": "support@example.com"})

class ServicesView(View):
    def get(self, request):
        return render(request, "services.html", {"services": ["Tư vấn", "Thiết kế", "Phát triển"]})

class ProductsView(View):
    def get(self, request):
        return render(request, "products.html", {"products": ["Sản phẩm A", "Sản phẩm B", "Sản phẩm C"]})

class BlogView(View):
    def get(self, request):
        posts = [
            {"title": "Học Django cơ bản", "author": "Sam"},
            {"title": "Class-based View là gì?", "author": "Lan"},
            {"title": "Template Inheritance trong Django", "author": "Minh"},
        ]
        return render(request, "blog.html", {"posts": posts})

class FAQView(View):
    def get(self, request):
        faqs = [
            {"question": "Django là gì?", "answer": "Một web framework mạnh mẽ của Python."},
            {"question": "Django có dễ học không?", "answer": "Khá dễ nếu đã biết Python."},
        ]
        return render(request, "faq.html", {"faqs": faqs})

class CareersView(View):
    def get(self, request):
        return render(request, "careers.html", {"jobs": ["Backend Developer", "Frontend Developer", "Tester"]})

class PrivacyView(View):
    def get(self, request):
        return render(request, "privacy.html", {"policy": "Chúng tôi cam kết bảo mật thông tin người dùng."})
