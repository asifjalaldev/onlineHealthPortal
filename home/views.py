from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Doctor.models import Doctor,DoctorCatagory
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
def home(request):
    if request.method=='GET':
        doctorsCatagories=DoctorCatagory.objects.all()
        doctors=Doctor.objects.all()
        total=doctors.count()
        query=request.GET.get('query')
        catagory=request.GET.get('catagory')
        paginator = Paginator(doctors,12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if query is None and catagory is None:
            context={'page_obj': page_obj, 'docCat':doctorsCatagories, 'total': total}
            return render(request, 'home/home.html', context)
        if int(catagory)==0:
                doctors=Doctor.objects.filter(Q(DoctorName__icontains=query))
                paginator = Paginator(doctors,12)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                total=len(doctors)
                context={'page_obj':page_obj, 'docCat': doctorsCatagories, 'total':total}
                return render(request, 'home/home.html',context)
            # filter(A, B) is the AND while   filter(A).filter(B) is OR         
        else:
                doctors=Doctor.objects.filter(Q(DoctorName__icontains=query)).filter( Q(catagory_id=catagory))
                total=doctors.count()
                paginator = Paginator(doctors,12)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
        context={'page_obj':page_obj, 'docCat': doctorsCatagories, 'total':total}
        return render(request, 'home/home.html',context)