from django.shortcuts import render, redirect
# 导入 HttpResponse 模块
from .models import ArticlePost
# 引入 markdown
import markdown
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.http import HttpResponse


# 视图函数

def article_list(request):
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body, 
    extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite'
    ])
    # 需要传递给模板的参数
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

# 写文章的视图
def article_create(request):
    if request.method == 'POST':
        artticle_post_form = ArticlePostForm(data=request.POST)
        if artticle_post_form.is_valid():
            new_article = artticle_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        artticle_post_form = ArticlePostForm()
        context = { 'article_post_form': artticle_post_form }
        return render(request, 'article/create.html', context)

def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")