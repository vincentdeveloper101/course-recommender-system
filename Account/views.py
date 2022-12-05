
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from Account.forms import CodeForm
from Account.models import Code, User_Detail
from Recommender.models import Course, Deleted_Course, Rating, Updated_Course
from django.http import HttpResponse
from django.shortcuts import render, redirect


from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


def home(request):
    return render(request, 'account/index.html')

# USER SIGNUP


def register(request):

    if request.method == 'POST':
        uname = request.POST['uname']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        county = request.POST['county']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        # pass2 = request.POST['pass2']

        # if pass1 != pass2:
        #     print('pass missmatch')
        #     messages.success(request, "Passwords Didn't match try Again")
        #     return redirect('register')
        if len(pass1) < 8:
            print('Too short')
            messages.success(
                request, "Too short Password. Use a minimum of 8 Characters")
            return render(request, 'account/register.html',
                          {'uname': uname,
                           'fname': fname,
                           'lname': lname,
                           'email': email,
                           'county': county,
                           'phone': phone,

                           })
        elif len(phone) < 10 or len(phone) > 13:
            print('Invalid phone')
            messages.success(
                request, "Invalid phone, use 07123 xx Or 011xx Or +2547xx")
            return render(request, 'account/register.html',
                          {'uname': uname,
                           'fname': fname,
                           'lname': lname,
                           'email': email,
                           'county': county,
                           'phone': phone,

                           })

        elif User.objects.filter(email=email).exists():
            print('email exists')
            messages.warning(request, "This Email Exists in our system. ")
            messages.info(request, "Kindly Use a differnt Email Address. ")
            return render(request, 'account/register.html',
                          {'uname': uname,
                           'fname': fname,
                           'lname': lname,
                           'email': email,
                           'county': county,
                           'phone': phone,

                           })
        elif User.objects.filter(username=uname).exists():
            print('username exists')
            messages.warning(request, "This username Exists in our system. ")
            messages.info(request, "Kindly Use a differnt Username. ")
            return render(request, 'account/register.html',
                          {'uname': uname,
                           'fname': fname,
                           'lname': lname,
                           'email': email,
                           'county': county,
                           'phone': phone,

                           })
        elif User_Detail.objects.filter(phone=phone).exists():
            print('phone exists')
            messages.warning(request, "This Phone Exists in our system. ")
            messages.info(request, "Kindly Use a differnt Phone Number. ")
            return render(request, 'account/register.html',
                          {'uname': uname,
                           'fname': fname,
                           'lname': lname,
                           'email': email,
                           'county': county,
                           'phone': phone,

                           })

        else:

            user = User.objects.create_user(
                username=uname, email=email, first_name=fname, last_name=lname, password=pass1)

            user.save()
            user1 = User_Detail(user=user, username=uname, first_name=fname, last_name=lname,
                                email=email, county=county, phone=phone, password=pass1)

            user1.save()
            print('user created')
          

            messages.success(
                request, f"Hi {uname}, your account was created successfully. <br> Thank you for registering To CRS, we've send you a verification code in you email. <br/> please check to complete your registration. ")
            request.session['pk'] = user.pk

            return redirect('otp')

    return render(request, 'account/register.html', )


def otp(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    user = User_Detail.objects.get(user_id=pk)

    if pk:
        user = User_Detail.objects.get(user_id=pk)
        code = user.code
        phone = user.phone
        is_verified = user.is_verified
        username = user.username
        print(is_verified)
        print(phone)
        code_user = f"{user.username}: {user.code}"
        if not request.POST:
            # send sms
            print(code_user)

            subject = 'welcome to CRS'
            message = f'Hi {user.username}, thank you for registering to CRS,  your code is: {code}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)

            # # send sms
            # from infobip_api_client.api_client import ApiClient, Configuration

            # BASE_URL = "https://qgm24r.api.infobip.com"
            # API_KEY = "c4767e0ca35fe352a792c89152ed4ba6-0b186dc5-9668-40fd-8a73-fba92b2a23d8"

            # SENDER = "InfoSMS"
            # RECIPIENT = ""
            # MESSAGE_TEXT = f"This is you code: {code}"

            # client_config = Configuration(
            #     host=BASE_URL,
            #     api_key={"APIKeyHeader": API_KEY},
            #     api_key_prefix={"APIKeyHeader": "App"},
            # )

            # api_client = ApiClient(client_config)

            # sms_request = SmsAdvancedTextualRequest(
            #     messages=[
            #         SmsTextualMessage(
            #             destinations=[
            #                 SmsDestination(
            #                     to=RECIPIENT,
            #                 ),
            #             ],
            #             _from=SENDER,
            #             text=MESSAGE_TEXT,
            #         )
            #     ])

            # api_instance = SendSmsApi(api_client)

            # try:
            #     api_response: SmsResponse = api_instance.send_sms_message(
            #         sms_advanced_textual_request=sms_request)
            #     print(api_response)
            # except ApiException as ex:
            #     print("Error occurred while trying to send SMS message.")
            #     print(ex)

        if form.is_valid():
            num = form.cleaned_data.get('code')

            if str(code) == num:
                code.save()
                User_Detail.objects.filter(
                    username=username).update(is_verified=True)

                print('code verified')
                messages.success(
                    request, "Your account is activated. ")

                return redirect('login')
            else:
                messages.success(
                    request, "Your account is not  activated. Please check your code. ")
                print('code not verified')

                return redirect('otp')
    return render(request, 'account/otp.html', {'form': form})


# USER LOGIN


def login(request):
    if request.method == 'POST':

        uname = request.POST['uname']
        pass1 = request.POST['pass1']

        user = auth.authenticate(username=uname, password=pass1)

        if User_Detail.objects.filter(username=uname).exists():

            k = User_Detail.objects.get(username=uname)
            s = k.staff
            v = k.is_verified

            if v == True:

                if s == False:

                    if User.objects.filter(username=uname).exists():
                        if user is not None:

                            auth.login(request, user)
                            print('login success')
                            messages.success(request, 'Login was successful')
                            return redirect('homepage')
                        else:
                            messages.warning(request, 'invalid Password')
                            print('invalid login')

                            return redirect('login')
                    else:
                        messages.warning(request, 'invalid username')
                        print('invalid username')
                        return redirect('login')
                else:

                    if User.objects.filter(username=uname).exists():
                        if user is not None:
                            auth.login(request, user)
                            print('login success')
                            messages.success(
                                request, 'Staff login is successful!!!')

                            return redirect('dashboard2')
                        else:
                            print('invalid password')
                            messages.warning(
                                request, 'Invalid  password!!!')

                            return redirect('login')
                    else:
                        print('invalid Username')
                        messages.warning(
                            request, 'Invalid username !!!')
                        return redirect('login')
            else:
                print('your account isnt verified, check email for the code!!')
                messages.warning(
                    request, 'your account isnt verifie, check email for the code!!')
                return redirect('otp')

        else:
            print('invalid Username')
            messages.warning(
                request, 'No username with such name in our system!!!, try to create a new account')
            return redirect('login')

    return render(request, 'account/login.html')

# STAFF LOGIN


def login2(request):

    # if request.user.is_authenticated:

    if request.method == 'POST':

        uname = request.POST['uname']
        pass1 = request.POST['pass1']

        staff = request.user.user_detail.staff
        if staff == False:
            messages.warning(request, 'Staff only')
            messages.warning(
                request, 'Contactact the system moderator for help')
            print('Staff only ')
            print('Contactact the system moderator for help')
            return redirect('login2')
        else:

            user = auth.authenticate(username=uname, password=pass1)
            if User.objects.filter(username=uname).exists():
                if user is not None:
                    auth.login(request, user)
                    print('login success')
                    messages.success(
                        request, 'Staff login is successful!!!')

                    return redirect('dashboard2')
                else:
                    print('invalid password')
                    messages.warning(
                        request, 'Invalid  password!!!')

                    return redirect('login2')
            else:
                print('invalid Username')
                messages.warning(
                    request, 'Invalid username !!!')
                return redirect('login2')
    # else:
    #     print('Sorry you must be authenticated!!')
    #     messages.warning(request, 'Sorry you must be authenticated!!')

        return redirect('login')

    return render(request, 'account/login2.html')

# STAFF DASHBOARD


def dashboard2(request):
    context = {}

    post2del = Course.objects.filter(author=request.user)
    posts = Course.objects.filter(author=request.user)
    post = Course.objects.filter(author=request.user)
    post_number = Course.objects.filter(author=request.user).count()
    total_courses = Course.objects.all().count()
    total_deleted_courses = Deleted_Course.objects.all().count()
    total_updated_courses = Updated_Course.objects.all().count()

    context['total_deleted_courses'] = total_deleted_courses
    context['total_updated_courses'] = total_updated_courses
    context['post2del'] = post2del
    context['posts'] = posts
    context['post'] = post
    context['total_courses'] = total_courses
    context['post_number'] = post_number

    return render(request, 'staff/index.html', context)

# LOGUT THE USER


def logout(request):
    auth.logout(request)

    print("you're logged out ")
    messages.warning(request, "you're logged out")

    return redirect('login')

# USER PROFILE


def profile(request):
    if request.user.is_authenticated:
        # "select sum(rating) from Rating where user=request.user.id"
        r = Rating.objects.filter(user=request.user.id)
        totalReview = 0
        for item in r:
            totalReview += int(item.rating)
        # select count(*) from Rating where user=request.user.id"
        totalratedcourse = Rating.objects.filter(user=request.user.id).count()
        return render(request, 'account/profile.html',
                      {
                          'totalReview': totalReview,
                          'totalratedcourse': totalratedcourse,
                      }
                      )
    else:
        return HttpResponseRedirect('/login/')


#   UPDATE USER PROFILE VIEWS
def update_profile(request):
    return render(request, 'account/profile-update.html')


def about(request):
    return render(request, 'account/about.html')
