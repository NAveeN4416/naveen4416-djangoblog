##  ------------------------ Verifications And Activation Views ----------------------------------- ##


def send_email(request):
    Subject = 'Subject'
    Body    = loader.render_to_string('students.html')
    email   = EmailMessage(Subject, Body, to=['naveen@yopmail.com'])
    if email.send():
        return redirect('index')
    return HttpResponse('Sorry Error Occured')          



def send_verify_link(request,ref_id):
    path = 'activate'
    obj  = secure.send_email_verification(request,ref_id,path)
    
    if obj:
        return redirect('users')
    return HttpResponse('Sorry Erro Occured !')    


def activate(request, uidb64, token):
    flag = secure.verify_email(uidb64, token)

    if flag==0:
        return HttpResponse('Your Account is Blocked')
    elif flag==1:
        return HttpResponse('Activation link is invalid!')
    else:
        return render(request,'registration/verification_success.html',{'user':flag})


def forgot_password(request):
    if request.is_ajax():
        email = request.POST['email_user']
        user  = User.objects.get(Q(email=email) | Q(username=email))
        if user:
            path = 'req_chang_pass'
            obj  = secure.send_email_verification(request,user.id,path)
            data = 1
        else:
            data = 0
        return HttpResponse(data)
    return render(request,'registration/forgot_password.html')     


def req_chang_pass(request, uidb64, token):
    user = secure.verify_email(uidb64, token)
    if user:
        context = {'user':user}
        return change_password(request,context)
    return HttpResponse(result)


def change_password(request,context=""):
    if request.is_ajax():
        new_password = request.POST['new_password']
        user_id      = request.POST['uid']
        user         = User.objects.get(id=user_id)
        if user.id:
            user.set_password(new_password)
            user.save()
            result = secure.password_changed(request,user)
            data = 0
        else:
            data = 1
        return HttpResponse(data)
    return render(request,'registration/change_password.html',context)


## ------------------------- End of Verifications And Activation Views ---------------------------- ##