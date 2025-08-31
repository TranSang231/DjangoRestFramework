from django.http import HttpResponse

def index(request):
    return HttpResponse("Đây là trang chủ")

def about(request):
    return HttpResponse("Đây là trang giới thiệu")

def contact(request):
    return HttpResponse("Đây là trang liên hệ")

def services(request):
    return HttpResponse("Đây là trang dịch vụ")

def products(request):
    return HttpResponse("Đây là trang sản phẩm")

def blog(request):
    return HttpResponse("Đây là trang blog")

def faq(request):
    return HttpResponse("Đây là trang câu hỏi thường gặp (FAQ)")
