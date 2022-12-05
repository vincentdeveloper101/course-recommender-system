from django.contrib.auth.models import User

# ALGORITHMN
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .forms import AddRatingForm
from .models import Course, Rating
from django.contrib import messages
import pandas as pd
from math import sqrt
import numpy as np
from math import ceil
# Create your views here.


def filterCourseBySchool():

    # filtering by schools
    allCourses = []
    schoolsCourse = Course.objects.values('schools', 'id')
    schools = {item["schools"] for item in schoolsCourse}
    for s in schools:
        course = Course.objects.filter(schools=s)
        print(course)
        n = len(course)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allCourses.append([course, range(1, nSlides), nSlides])
    params = {'allCourses': allCourses}
    return params


def generateRecommendation(request):
    course = Course.objects.all()
    rating = Rating.objects.all()
    x = []
    y = []
    A = []
    B = []
    C = []
    D = []

    # course Data Frames
    for item in course:
        x = [item.id, item.title, item.academic_year,item.entry_year,
             item.image.url, item.schools, item.tution_fees, item.lectures, item.intake_in, item.faculty, item.school_email, item.school_phone, item.location, item.description]
        y += [x]
    courses_df = pd.DataFrame(
        y, columns=['courseId', 'title', 'academic_year','entry_year' ,'image', 'schools', 'tution_fees', 'lectures', 'intake_in', 'faculty', 'school_email', 'school_phone', 'location', 'description'])
    print("courses DataFrame")
    print(courses_df)
    print(courses_df.dtypes)
    # Rating Data Frames
    print(rating)
    for item in rating:
        A = [item.user.id, item.course, item.rating]
        B += [A]
    rating_df = pd.DataFrame(B, columns=['userId', 'courseId', 'rating'])
    print("Rating data Frame")
    rating_df['userId'] = rating_df['userId'].astype(str).astype(np.int64)
    rating_df['courseId'] = rating_df['courseId'].astype(str).astype(np.int64)
    rating_df['rating'] = rating_df['rating'].astype(str).astype(np.float)
    print(rating_df)
    print(rating_df.dtypes)
    if request.user.is_authenticated:
        userid = request.user.id
        # select related is join statement in django.It looks for foreign key and join the table
        userInput = Rating.objects.select_related('course').filter(user=userid)
        if userInput.count() == 0:
            recommenderQuery = None
            userInput = None
        else:
            for item in userInput:
                C = [item.course.title, item.rating]
                D += [C]
            inputCourses = pd.DataFrame(D, columns=['title', 'rating'])
            print("Rated  Courses by user dataframe")
            inputCourses['rating'] = inputCourses['rating'].astype(
                str).astype(np.float)
            print(inputCourses.dtypes)

            # Filtering out the courses by title
            inputId = courses_df[courses_df['title'].isin(
                inputCourses['title'].tolist())]
            # Then merging it so we can get the courseId. It's implicitly merging it by title.
            inputCourses = pd.merge(inputId, inputCourses)
            # #Dropping information we won't use from the input dataframe
            # inputCourses = inputCourses.drop('tution_fees', 1)
            # Final input dataframe
            # If a course you added in above isn't here, then it might not be in the original
            # dataframe or it might spelled differently, please check capitalisation.
            print(inputCourses)

            # Filtering out users that have watched Courses that the input has watched and storing it
            userSubset = rating_df[rating_df['courseId'].isin(
                inputCourses['courseId'].tolist())]
            print(userSubset.head())

            # Groupby creates several sub dataframes where they all have the same value in the column specified as the parameter
            userSubsetGroup = userSubset.groupby(['userId'])

            # print(userSubsetGroup.get_group(7))

            # Sorting it so users with course most in common with the input will have priority
            userSubsetGroup = sorted(
                userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

            print(userSubsetGroup[0:])

            userSubsetGroup = userSubsetGroup[0:]

            # Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
            pearsonCorrelationDict = {}

        # For every user group in our subset
            for name, group in userSubsetGroup:
                # Let's start by sorting the input and current user group so the values aren't mixed up later on
                group = group.sort_values(by='courseId')
                inputCourses = inputCourses.sort_values(by='courseId')
                # Get the N for the formula
                nRatings = len(group)
                # Get the review scores for the courses that they both have in common
                temp_df = inputCourses[inputCourses['courseId'].isin(
                    group['courseId'].tolist())]
                # And then store them in a temporary buffer variable in a list format to facilitate future calculations
                tempRatingList = temp_df['rating'].tolist()
                # Let's also put the current user group reviews in a list format
                tempGroupList = group['rating'].tolist()
                # Now let's calculate the pearson correlation between two users, so called, x and y
                Sxx = sum([i**2 for i in tempRatingList]) - \
                    pow(sum(tempRatingList), 2)/float(nRatings)
                Syy = sum([i**2 for i in tempGroupList]) - \
                    pow(sum(tempGroupList), 2)/float(nRatings)
                Sxy = sum(i*j for i, j in zip(tempRatingList, tempGroupList)) - \
                    sum(tempRatingList)*sum(tempGroupList)/float(nRatings)

                # If the denominator is different than zero, then divide, else, 0 correlation.
                if Sxx != 0 and Syy != 0:
                    pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
                else:
                    pearsonCorrelationDict[name] = 0

            print("pearsonCorrelationDict.items()")
            print(pearsonCorrelationDict.items())

            pearsonDF = pd.DataFrame.from_dict(
                pearsonCorrelationDict, orient='index')
            pearsonDF.columns = ['similarityIndex']
            pearsonDF['userId'] = pearsonDF.index
            pearsonDF.index = range(len(pearsonDF))
            print(pearsonDF.head())

            topUsers = pearsonDF.sort_values(
                by='similarityIndex', ascending=False)[0:]
            print("topUsers.head()")
            print(topUsers.head())

            topUsersRating = topUsers.merge(
                rating_df, left_on='userId', right_on='userId', how='inner')
            topUsersRating.head()

            # Multiplies the similarity by the user's ratings
            topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * \
                topUsersRating['rating']
            topUsersRating.head()

            # Applies a sum to the topUsers after grouping it up by userId
            tempTopUsersRating = topUsersRating.groupby(
                'courseId').sum()[['similarityIndex', 'weightedRating']]
            tempTopUsersRating.columns = [
                'sum_similarityIndex', 'sum_weightedRating']
            tempTopUsersRating.head()

            # Creates an empty dataframe
            recommendation_df = pd.DataFrame()
            # Now we take the weighted average
            recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating'] / \
                tempTopUsersRating['sum_similarityIndex']
            recommendation_df['courseId'] = tempTopUsersRating.index
            recommendation_df.head()

            recommendation_df = recommendation_df.sort_values(
                by='weighted average recommendation score', ascending=False)
            recommender = courses_df.loc[courses_df['courseId'].isin(
                recommendation_df.head(5)['courseId'].tolist())]
            print("recommender")
            print(recommender)
            return recommender.to_dict('records')


def homepage(request):

    params = filterCourseBySchool()
    params['recommended'] = generateRecommendation(request)
    return render(request, 'account/homepage.html', params)


def dashboard(request):
    if request.user.is_authenticated:
        params = filterCourseBySchool()
        params['user'] = request.user
        if request.method == 'POST':
            userid = request.POST.get('userid')
            courseid = request.POST.get('courseid')
            course = Course.objects.all()
            u = User.objects.get(pk=userid)
            m = Course.objects.get(pk=courseid)
            rfm = AddRatingForm(request.POST)
            params['rform'] = rfm
            if rfm.is_valid():
                rat = rfm.cleaned_data['rating']
                count = Rating.objects.filter(user=u, course=m).count()

                # prevent motiple review to one course
                if (count > 0):
                    messages.warning(
                        request, 'You have already submitted your review!!')
                    return render(request, 'account/dashboard.html', params)
                action = Rating(user=u, course=m, rating=rat)
                action.save()
                messages.success(
                    request, 'You have submitted'+' '+rat+' '+"star")
            return render(request, 'account/dashboard.html', params)
        else:

            # print(request.user.id)
            rfm = AddRatingForm()
            params['rform'] = rfm
            course = Course.objects.all()
            return render(request, 'account/dashboard.html', params)
    else:
        return HttpResponseRedirect('/login/')
