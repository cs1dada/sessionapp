# _*_ encoding:utf-8 _*_
from django.core.mail import EmailMessage
from django.template import RequestContext
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from mysite import models, forms

def index(request, pid=None, del_pass=None):
    if 'username' in request.session:
        username = request.session['username']
        useremail = request.session['useremail']

    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)

def login(request):
    if request.method == 'POST':
        #post method (write)
        #check login_form is valid 
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            #grab account info from client
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            try:
                # grab user data from database
                user = models.User.objects.get(name=login_name)
                # password verify
                if user.password == login_password:
                    # write session [username, useremail]
                    request.session['username'] = user.name
                    request.session['useremail'] = user.email
                    messages.add_message(request, messages.SUCCESS, ' success login ')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, ' incorrect password ')
            except:
                messages.add_message(request, messages.WARNING, ' no such member, cannot login ')
        else:
            messages.add_message(request, messages.INFO, ' plz check input content ')
    else:
        #empty instance for read login_form
        login_form = forms.LoginForm()

        message = 'create personal account --> username and password'

    template = get_template('login.html')

    html = template.render(locals(), request)
    response = HttpResponse(html)

    return response

def userinfo(request):
    if 'username' in request.session:
        username = request.session['username']
    else:
        return redirect('/login/')

    try:
        userinfo = models.User.objects.get(name=username)
    except:
        pass

    template = get_template('userinfo.html')
    html = template.render(locals())
    return HttpResponse(html)

def listing(request):
    template = get_template('listing.html')
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()

    html = template.render(locals())

    return HttpResponse(html)

def post2db(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            message = "您的訊息已儲存，要等管理者啟用後才看得到喔。"
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message = '如要張貼訊息，則每一個欄位都要填...'
    else:
        post_form = forms.PostForm()
        message = '如要張貼訊息，則每一個欄位都要填...'          

    template = get_template('post2db.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)

def posting(request):

    template = get_template('posting.html')
    moods = models.Mood.objects.all()
    message = '如要張貼訊息，則每一個欄位都要填...'
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)

def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感謝您的來信，我們會儘速處理您的寶貴意見。"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email  = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']

            mail_body = u'''
網友姓名：{}
居住城市：{}
是否在學：{}
反應意見：如下
{}'''.format(user_name, user_city, user_school, user_message)

            email = EmailMessage(   '來自【不吐不快】網站的網友意見', 
                                    mail_body, 
                                    user_email,
                                    ['skynet.tw@gmail.com'])
            email.send()
        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.ContactForm()

    template = get_template('contact.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)

