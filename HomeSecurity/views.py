from django.shortcuts import render
from . import yolo

# Create your views here.
def Welcome(request):
    return render(request,'Welcome.html')

def Import(request):
    return render(request,'Import.html')

def Security(request):
    if request.method == "POST":
        number = request.POST['number']
        print(number)
        yolo.camera(number)
    return render(request,'Security.html')
