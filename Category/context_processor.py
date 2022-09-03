from .models import Categories,SubCategories

def menu_links(request):
    category_links = Categories.objects.all()
    return {'category_links':category_links}