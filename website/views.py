from django.shortcuts import render, redirect


def website(request):
    #
    return render(request, 'website/index.html')


def redirect_to_welcome(request):
    return redirect('welcome')