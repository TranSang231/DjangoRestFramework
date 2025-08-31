from django.http import HttpResponse
from django.http import HttpResponse
from django.views import View

class IndexView(View):
    def get(self, request):
        return HttpResponse("Đây là trang chủ (Class-based View)")

class AboutView(View):
    def get(self, request):
        return HttpResponse("Đây là trang giới thiệu (Class-based View)")

class ContactView(View):
    def get(self, request):
        return HttpResponse("Đây là trang liên hệ (Class-based View)")

class ServicesView(View):
    def get(self, request):
        return HttpResponse("Đây là trang dịch vụ (Class-based View)")

class ProductsView(View):
    def get(self, request):
        return HttpResponse("Đây là trang sản phẩm (Class-based View)")

class BlogView(View):
    def get(self, request):
        return HttpResponse("Đây là trang blog (Class-based View)")

class FAQView(View):
    def get(self, request):
        return HttpResponse("Đây là trang câu hỏi thường gặp (FAQ) - Class-based View")
