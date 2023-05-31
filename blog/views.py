from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post, Category
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

# or 検索用にDjangoのクエリセットAPIであるQ()関数を使用
from django.db.models import Q
# 畳み込み演算用
from functools import reduce
# 条件式を結合するため
from operator import and_


# トップページ
class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        return render(request, 'blog/index.html', {
            'post_data': post_data,
        })

# 詳細ページ
class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_detail.html', {
            'post_data': post_data
        })

# 新規投稿
class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'blog/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            # フォームからカテゴリのデータを取得して、post_data.categoryにデータを登録
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data

            post_data.content = form.cleaned_data['content']
            # 画像がアップロードされたとき､formで取得した画像データをpost_dataに格納
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'blog/post_form.html', {
            'form': form
        })

# 投稿を編集
class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'category': post_data.category,
                'content': post_data.content,
                'image': post_data.image,
            }
        )

        return render(request, 'blog/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            # フォームからカテゴリのデータを取得して、post_data.categoryにデータを登録
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data

            post_data.content = form.cleaned_data['content']
            # 画像がアップロードされたとき､formで取得した画像データをpost_dataに格納
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'blog/post_form.html', {
            'form': form
        })

# 投稿削除
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')


# カテゴリ機能
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'blog/index.html', {
            'post_data': post_data
        })


# 検索機能
class SearchView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        # 検索フォームからキーワードを取得
        keyword = request.GET.get('keyword')

        if keyword:
            # 半角と全角の空文字列を除外してquery_listに一文字ずつ格納
            exclusion_list = set([' ', '　'])
            query_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            # キーワードをQオブジェクトでor検索
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list])
            # 投稿データにキーワードでフィルターをかける
            post_data = post_data.filter(query)

        return render(request, 'blog/index.html', {
            'keyword': keyword,
            'post_data': post_data
        })
