from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_delete_product(request, product_id):
    print(product_id)
    product = request.user.products.all().get(pk=product_id)
    product.delete()

    return JsonResponse({'success': True})