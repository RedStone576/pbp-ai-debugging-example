from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Item
from .forms import ItemForm

def item_list(request):
    items = Item.objects.all().order_by('-created_at')
    form = ItemForm()
    return render(request, 'inventory/item_list.html', {'items': items, 'form': form})

@require_POST
def add_item_ajax(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        item = form.save()
        return JsonResponse({
            'status': 'success',
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'description': item.description,
        }, status=201)
    
    # Bug demonstration: Returns HTTP 400 Bad Request when form validation fails.
    # Students must handle this status in JavaScript and display field error messages to users.
    return JsonResponse({
        'status': 'error',
        'errors': form.errors
    }, status=400)
