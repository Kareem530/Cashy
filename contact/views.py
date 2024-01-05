from django.shortcuts import render, redirect
from contact.models import Contact
from django.contrib import messages
from django.core.mail import send_mail



def contact(request):
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        user_id = request.POST['user_id']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(user=user_id)
            if has_contacted:
                messages.error(request, 'You Have Already Messaged Us')
                return redirect('Contact')

        contact = Contact(name=name,email=email, message=message, subject=subject,user=user_id)
        contact.save()
        messages.success(request, 'Your Message Has Been Submitted, We Will Get Back To You Soon')
        return render(request,'pages/Contact.html')

        # Send email (disabled for now)
        # send_mail(
        #   'Property Listing Inquiry',
        #   'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
        #   'example@gmail.com',
        #   [realtor_email, 'example2@gmail.com'],
        #   fail_silently=False
        # )
        
    else:
     return render(request,'pages/Contact.html')
    
    
    
