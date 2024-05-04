from django.shortcuts import render, redirect
from .models import ResponseForm

# Create your views here.
def home_view(request):

    return render(request,'home.html')

def response_view(request):

    if request.method == 'POST':
        form = ResponseForm(request.POST)
         
        if form.is_valid():
            form.save()
            return redirect('..')
    else:
        form = ResponseForm()
    
    return render(request,'response.html',{'form':form})
