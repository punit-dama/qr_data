import qrcode, os, pdfkit, subprocess
from django.template.loader import get_template
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django_ical.views import ICalFeed
import vobject
from django.contrib.auth.decorators import login_required
from .forms import EntryForm
from .models import Entry
from django.core.files.base import ContentFile
from io import BytesIO
import base64
import imgkit
# import wkhtmltopdf
from django.template.loader import render_to_string
from django.conf import settings
from html2image import Html2Image


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
# app_name = "qr_card_app"



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    elif request.method == 'GET':
        logout(request)  # Log out the admin user when the page is accessed via GET (refresh)
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')

def index_view(request):
    return render(request,'index.html')

@login_required(login_url='login')
def form_view(request):
    
    form = EntryForm(request.POST, request.FILES)
    if form.is_valid():
        form_value = form.save()
        url = reverse('details', args=[form_value.id])
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(request.build_absolute_uri(url))
        qr.make(fit=True)
        qr_image = qr.make_image()
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        # Create a ContentFile object from the buffer
        content_file = ContentFile(buffer.getvalue())
        qr_code_image = f'qr_code_{form_value.id}.png'
        form_value.qr_code.save(qr_code_image,  content_file, save=True)
        return redirect('qr_code', id=form_value.id)
    

    else:
        form = EntryForm()
    return render(request, 'form.html', {'form': form})

def qr_code_view(request, id):
    qr = Entry.objects.get(id=id)
    
    url = reverse('details', args=[qr.id])
    return render(request, 'qrcode.html', {'qr':qr, 'url':url})



def landing_view(request, data_id):
    form_data = Entry.objects.get(id=data_id)
    context = {

        'form_data' : form_data
    }
    return render(request, 'landing_page.html', context)


def landing_view2(request, data_id):
    form_data = Entry.objects.get(id=data_id)
    context = {

        'form_data' : form_data
    }
    return render(request, 'landing2.html', context)

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

    card.add('title')
    card.title.value = form_data.designation

    # Set the email field
    card.add('email')
    card.email.value = form_data.email
    card.email.type_param = 'INTERNET'

    # Set the company field
    card.add('org')
    card.org.value = ['Atrina Technologies']

    # Set the phone field
    card.add('tel')
    card.tel.value = form_data.phone

    #Set the image field
   
    photo = card.add('photo')
    photo_data =form_data.photo.read()  # Assuming 'photo' is a FileField or ImageField
    photo.value = base64.b64encode(photo_data).decode('utf-8')  # Encode photo data as base64 and set as value
    photo.params['encoding'] = 'b'

    # Add urls
    urls = ['https://metrobrands.com', form_data.linkedin]

    for url in urls:
        url_obj = card.add('url')
        url_obj.value = url


    # Add work Address
    work_address = card.add('adr')
    work_address.value = vobject.vcard.Address(
    street='401, Kanakia Zillion, LBS Marg & CST Road, Kurla West, Junction',
    city='Mumbai 400070',
    region='Maharashtra',
    # postalcode='400070',
    country='India'
)
    work_address.type_param = 'work'


    # generate the VCF file as a string
    vcf_file = card.serialize()

    # create an HTTP response with the VCF file as content
    response = HttpResponse(vcf_file, content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{fullname}.vcf"'
    return response

def withmobile(request,id):


    data = Entry.objects.get(id=id)
    host = request.get_host()
    url = reverse('details', args=[data.id])
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(request.build_absolute_uri(url))
    qr.make(fit=True)
    qr_image = qr.make_image()
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    # Create a ContentFile object from the buffer
    content_file = ContentFile(buffer.getvalue())
    qr_code_image = f'qr_code_{data.id}.png'
    data.qr_code.save(qr_code_image,  content_file, save=True)
    
    context = {
        "data":data,
        "url":url,
        "host":host,
        }

    return render(request,'admin.html',context)

def withoutmobile(request,id):


    data = Entry.objects.get(id=id)
    host = request.get_host()
    url = reverse('details2', args=[data.id])
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(request.build_absolute_uri(url))
    qr.make(fit=True)
    qr_image = qr.make_image()
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    # Create a ContentFile object from the buffer
    content_file = ContentFile(buffer.getvalue())
    qr_code_image = f'qr_code_{data.id}.png'
    data.qr_code.save(qr_code_image,  content_file, save=True)
    
    context = {
        "data":data,
        "url":url,
        "host":host,
        }

    return render(request,'admin.html',context)

def iadmin(request):
    
    return render(request,'admin.html')

def search(request):
    if request.method == 'POST':
        searched = request.POST['search_query']
        queryset=Entry.objects.filter(phone=searched)

        for item in queryset:
            link = reverse('details', args=[item.id])        
        chost = request.get_host()
        
        return render(request, 'admin.html',{'queryset':queryset, 'chost':chost, 'link':link})
    
def visitcard(request,id):
    # hti=Html2Image(output_path='qr_card_app/media/visiting_cards')

    
    data = Entry.objects.get(id=id)
    context={
        "data":data
    }
  
    fullname = data.first_name+"-"+data.last_name
    # hti.screenshot(
    # html_file='qr_card_app/templates/qrcode.html',
    # save_as=f'{fullname}-card.png'
# )
    
        # Render the template to HTML string
    html_string = render_to_string('visitcard.html', context)

# File paths
    # output_pdf = os.path.join(settings.BASE_DIR, f'qr_card_app/media/visiting_cards/{fullname}-card.pdf')
    output_png = os.path.join(settings.BASE_DIR, f'qr_card_app/media/visiting_cards/{fullname}-card.png')

    # Generate PDF using wkhtmltopdf
    command = ['wkhtmltoimage', '-', output_png]
    subprocess.run(command, input=html_string, check=True, text=True, capture_output=True)

    # # Convert PDF to PNG using ImageMagick (requires installation of ImageMagick)
    # subprocess.run(['convert', '-density', '300', output_pdf, '-quality', '100', output_png], check=True)

    # Delete the temporary PDF file
    # os.remove(output_pdf)

    # Return the PNG file as a response
    with open(f'/home/punit/workspace/python/qr_data/qr_card_app/media/visiting_cards/{fullname}-card.png', 'r+b') as f:
        response = HttpResponse(f.read(), content_type='image/png')

    response['Content-Disposition'] = f'attachment; filename= "{fullname}-card.png" '
    return response


        
