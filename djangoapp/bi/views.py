from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from .models import Category
from django.contrib import messages
from .models import Category, BIReport
from .forms import *

def home_dashboard(request):
    return render(request, "meu_painel/homeDashboard.html", context={ })

def category_list(request):
    query = request.GET.get('name')  # agora está certo!
    categories = Category.objects.all()

    if query:
        categories = categories.filter(name__icontains=query)

    categories = categories.annotate(report_count=Count('bi_reports')).order_by('name')
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    fields = ["name", "description", "created_at"]
    headers = ["Nome", "Descrição", "Data de criação"]

    context = {
        "title": "Gerenciar Categorias",
        "search_placeholder": "Buscar categoria...",
        "search_name": "name",  # <- importante, mantém o campo em HTML
        "button_label": "Nova Categoria",
        "data": page_obj,
        "headers": headers,
        "fields": fields,
        "field_labels": zip(fields, headers),
        "object_id_field": "id",
        "page_obj": page_obj,
        "form": CategoryForm(),
    }

    return render(request, 'meu_painel/category/category_list.html', context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso.')
        else:
            # Junta todos os erros do formulário em uma string
            error_messages = []
            for field, errors in form.errors.items():
                field_name = form.fields[field].label or field.capitalize()
                for error in errors:
                    error_messages.append(f"{field_name}: {error}")
            full_error_message = "Erro ao criar a categoria:<br>" + "<br>".join(error_messages)
            messages.error(request, full_error_message)
    return redirect('category_list')

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    related_bis = BIReport.objects.filter(category=category)

    if related_bis.exists():
        used_titles = ', '.join([bi.title for bi in related_bis])
        messages.error(request, f'Não é possível excluir. Categoria em uso por: {used_titles}')
        return redirect('category_list')

    category.delete()
    messages.success(request, 'Categoria excluída com sucesso.')
    return redirect('category_list')
