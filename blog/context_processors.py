from . models import Category

def extrect(request):
    items = Category.objects.all()
    return {'items':items}