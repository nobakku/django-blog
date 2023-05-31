from .models import Category

# すべてのカテゴリデータをどのテンプレートでも使えるようにする設定
def common(request):
    category_data = Category.objects.all()
    context = {
        'category_data': category_data,
    }
    return context
