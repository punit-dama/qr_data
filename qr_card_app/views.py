import qrcode
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django_ical.views import ICalFeed
import vobject

from .forms import EntryForm
from .models import Entry


def form_view(request):
    
    form = EntryForm(request.POST, request.FILES)
    if form.is_valid():
        form_value = form.save()
        url = reverse('details', args=[form_value.id])
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(request.build_absolute_uri(url))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    else:
        form = EntryForm()
    return render(request, 'form.html', {'form': form})

def landing_view(request, data_id):
    form_data = Entry.objects.get(id=data_id)
    context = {

        'form_data' : form_data
    }
    return render(request, 'landing_page.html', context)

def delete_emp(request, id):
    emp = Entry.objects.get(id=id)
    emp.delete()
    print("Successfully Deleted!")
    # return HttpResponse()


def download_vcf(request, id):
    # retrieve the form data using the pk parameter
    form_data = Entry.objects.get(id=id)
    
    # Create a new vCard object
    card = vobject.vCard()

    # Set the first name field
    fullname = form_data.first_name +" "+form_data.last_name
    card.add('fn')
    card.fn.value = fullname
    # Set the email field
    card.add('email')
    card.email.value = form_data.email

    # Set the company field
    card.add('org')
    card.org.value = ['Atrina Technologies']

    # Set the phone field
    card.add('tel')
    card.tel.value = form_data.phone

    #Set the image field
   
    # photo_data = form_data.photo.read()
    # card.add('photo')
    # card.photo.value = photo_data

    # generate the VCF file as a string
    vcf_file = card.serialize()

    # create an HTTP response with the VCF file as content
    response = HttpResponse(vcf_file, content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{fullname}.vcf"'
    return response
