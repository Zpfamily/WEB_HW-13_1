from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import DetailView
from .models import Author, Tag, Quote
from django.views import View


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AuthorForm, QuoteForm, TagForm


from .utils import get_mongodb
PER_PAGE = 4

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={'quotes': quotes_on_page})


def author(request, author: str):
    try:
        author = Author.objects.get(fullname=author)
    except:
        author = None
    context = {"author": author}
    return render(request, "quotes/author.html", context)


def tag(request, tag: str, page: int = 1):
    quotes = []
    tag_id = None
    try:
        tag_id = Tag.objects.get(name=tag).id
    except Tag.DoesNotExist:
        pass

    if tag_id:
        quotes = Quote.objects.filter(tags=tag_id).order_by('id')  # Assuming 'id' is the field you want to order by

    paginator = Paginator(quotes, per_page=PER_PAGE)
    context = {"quotes": paginator.page(page), "tag_query": tag}
    return render(request, "quotes/tag.html", context)

@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            fullname = form.cleaned_data["fullname"]
            messages.success(request, f"Author '{fullname}' was created...")
            return render(
                request, "quotes/add_author.html", context={"form": AuthorForm()}
            )
        else:
            messages.error(request, "Not added...")
            return render(request, "quotes/add_author.html", context={"form": form})

    context = {"form": AuthorForm()}
    return render(request, "quotes/add_author.html", context)


@login_required
def add_quote(request, id: int = 0):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        print(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.quote = form.cleaned_data['quote']
            new_quote.author = Author.objects.filter(pk=form.cleaned_data['author']).get()
            new_quote.save()

            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist("tags")
            )
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            messages.success(request, "Quote was added....")
        else:
            messages.error(request, "Not added....")
            return render(request, "quotes/add_quote.html", {"tags": tags, "authors": authors, "form": form})

    return render(request, "quotes/add_quote.html", {"tags": tags, "authors": authors, "form": QuoteForm()})


class AddAuthorView(LoginRequiredMixin, View):
    form_class = AuthorForm
    template_name = "quotes/add_author.html"

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            fullname = form.cleaned_data["fullname"]
            messages.success(request, f"Author '{fullname}' was created...")
            return render(
                request, self.template_name, context={"form": self.form_class}
            )
        else:
            messages.error(request, "Not added...")
            return render(request, self.template_name, context={"form": form})


class AddTagView(LoginRequiredMixin, View):
    form_class = TagForm
    template_name = "quotes/add_tag.html"

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            fullname = form.cleaned_data["name"]
            messages.success(request, f"Tag '{fullname}' was created...")
            return render(
                request, self.template_name, context={"form": self.form_class}
            )
        else:
            messages.error(request, "Not added...")
            return render(request, self.template_name, context={"form": form})

