from django.shortcuts import render
# 导入 HttpResponse 模块
from .models import ArticlePost

# 视图函数


def article_list(request):
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)
