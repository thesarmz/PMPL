from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item, List

def home_page(request):
#    if request.method == 'POST':      
#        Item.objects.create(text=request.POST['item_text'])  #2
#        return redirect('/lists/the-only-list-in-the-world/')

    if Item.objects.count() == 0:
	    comment = 'yey, waktunya berlibur'
    elif Item.objects.count() < 5:
	    comment = 'sibuk tapi santai'
    else:
        comment = 'oh tidak'
	
    return render(request, 'home.html', {'comment': comment})

	
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})
	
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))
	
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))