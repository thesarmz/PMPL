from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        #new_item_text = request.POST['item_text']  #1        
        Item.objects.create(text=request.POST['item_text'])  #2
        return redirect('/')
    #else:
    #    new_item_text = ''  #3
	
    if Item.objects.count() == 0:
	    comment = 'yey, waktunya berlibur'
    elif Item.objects.count() < 5:
	    comment = 'sibuk tapi santai'
    else:
        comment = 'oh tidak'
	
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items, 'comment': comment})
    #return render(request, 'home.html', {
    #    'new_item_text': new_item_text,  #4
    #})