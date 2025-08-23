import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab2.settings")
django.setup()

from blog.models import Author, Post, Category, Comment

def run():
    # Xoá dữ liệu cũ cho sạch
    Author.objects.all().delete()
    Post.objects.all().delete()
    Category.objects.all().delete()
    Comment.objects.all().delete()

    # Tạo Author
    author = Author.objects.create(name="Sang Tran", email="sang@example.com")

    # Tạo Post
    post1 = Post.objects.create(title="Bài viết Django", content="Học Django cơ bản", author=author)
    post2 = Post.objects.create(title="REST API", content="Xây dựng API với DRF", author=author)

    # Tạo Category
    cat1 = Category.objects.create(name="Python")
    cat2 = Category.objects.create(name="Web Development")
    post1.categories.add(cat1, cat2)
    post2.categories.add(cat1)

    # Tạo Comment
    Comment.objects.create(post=post1, author_name="User A", text="Hay quá!")
    Comment.objects.create(post=post1, author_name="User B", text="Cảm ơn tác giả!")
    Comment.objects.create(post=post2, author_name="User C", text="Rất hữu ích!")

    print("✅ Dữ liệu mẫu đã được tạo thành công!")

if __name__ == "__main__":
    run()
