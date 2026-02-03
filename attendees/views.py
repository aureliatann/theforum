# Create your views here.
from django.shortcuts import render, redirect
from .forms import AttendeeForm

# view -> python function that runs when someone opens a webpage (when use visits this URL, what should website do?)

# this view / function runs whenever someone visits registration page
def register(request):
    # if POST (user just submitted the form), need to process and save form
    if request.method == "POST":
        form = AttendeeForm(request.POST)   # loads the dat athe user typed into django form
        # django checks that name isn't empty and email is in valid format
        if form.is_valid():
            form.save()  # saves name and email to the database
            return redirect('success')  # goes to success page
    else:
        # user's first time visiting (GET request) -> show empty form
        form = AttendeeForm()

    # render -> show the register HTML
    return render(request, 'register.html', {'form': form})

# when form is saved, show the success HTML
def success(request):
    return render(request, 'success.html')