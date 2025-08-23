import os
import django

# Trỏ tới file settings.py của project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab2.settings")

# Khởi tạo Django
django.setup()

# Import model sau khi setup Django
from blog.models import Post

# Tạo dữ liệu
post = Post.objects.create(title="Bài test", content="Nội dung cho bài test nộp thầy")

# Lấy toàn bộ dữ liệu
all_posts = Post.objects.all()

print("Danh sách bài viết trong database:")
for p in all_posts:
    print(f"- {p.id}: {p.title} ({p.created_at})")
