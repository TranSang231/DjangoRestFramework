import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab2.settings")
django.setup()

from blog.models import Author, Post, Category, Comment

# Lấy 1 author đầu tiên trong DB
author = Author.objects.first()

# Lấy 1 post đầu tiên trong DB
post1 = Post.objects.first()

# Lấy category tên "Python"
category1 = Category.objects.filter(name="Python").first()

# Lấy tất cả post của một author
posts = author.posts.all()
print("Posts của author:", [p.title for p in posts])

# Lấy tất cả comment của một post
comments = post1.comments.all()
print("Comments của post:", [c.text for c in comments])

# Lấy tất cả post trong 1 category
python_posts = category1.posts.all()
print("Posts trong category:", [p.title for p in python_posts])

# Lấy tất cả comment + tiêu đề bài viết liên quan
comments_with_post = Comment.objects.select_related("post").all()
for c in comments_with_post:
    print(c.text, "-> thuộc bài viết:", c.post.title)

# Lấy tất cả post + category (giảm số query)
posts_with_categories = Post.objects.prefetch_related("categories").all()
for p in posts_with_categories:
    print(p.title, "->", [c.name for c in p.categories.all()])