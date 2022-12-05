
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect, HttpResponse
from Recommender.models import Course, Deleted_Course, Updated_Course
from Staff.forms import AddCourseForm, UpdateCourseForm
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def addcourse(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = AddCourseForm(request.POST, request.FILES)
            if fm.is_valid():
                obj = fm.save(commit=False)
                author = User.objects.filter(email=request.user.email).first()
                obj.author = author
                obj.save()

                messages.success(request, 'Course Added Successfully!!!')
                messages.success(request, 'Check it in your Homepage!!!')

        else:
            fm = AddCourseForm()
        return render(request, 'staff/add.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


def detail_course_view(request, slug):

    context = {}

    posts = get_object_or_404(Course, slug=slug)
    context['posts'] = posts

    return render(request, 'staff/detail.html', context)


def course_delete(request, slug):

    context = {}
    user = request.user
    phone = request.user.user_detail.phone
    course_id = get_object_or_404(Course, slug=slug)
    if user.is_authenticated:

        posts = get_object_or_404(Course, slug=slug).delete()
        print('post deleted')
        messages.success(request, "you're post was delted")

        # save to db

        save_deleted_post = Deleted_Course(
            user=user,
            phone=phone,
            course_id=course_id,
        )
        save_deleted_post.save()
        messages.success(request, "status updated")

        context['posts'] = posts
        return redirect('dashboard2')

    else:
        print('not autheticated')
        messages.success(request, "you're not autheticated")
        return redirect('login')

    return render(request, 'staff/delete.html', context)


def update_course_view(request, slug):

    context = {}

    user = request.user
    phone = request.user.user_detail.phone
    course_id = get_object_or_404(Course, slug=slug)

    if not user.is_authenticated:
        return redirect("login")

    post = get_object_or_404(Course, slug=slug)

    if post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = UpdateCourseForm(request.POST or None,
                                request.FILES or None, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            post = obj

            save_updated_course = Updated_Course(

                user=user,
                phone=phone,
                course_id=course_id,

            )
            save_updated_course.save()
            messages.success(request, "status updated")

    form = UpdateCourseForm(

        initial={
            "title": post.title,
            "schools": post.schools,
            "image": post.image,
            "tution_fees": post.tution_fees,
            "academic_year": post.academic_year,
            "lectures": post.lectures,
            "intake_in": post.intake_in,
            "faculty": post.faculty,
            "location": post.location,
            "description": post.description,
        }
    )

    context['form'] = form
    return render(request, 'staff/update.html', context)
