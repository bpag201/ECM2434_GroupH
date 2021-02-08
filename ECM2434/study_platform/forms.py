from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

def register(request):
    submitted = False
15     if request.method == 'POST':
16         form = RegisterForm(request.POST)
17         if form.is_valid():
18             cd = form.cleaned_data
19             # assert False
20             return HttpResponseRedirect('/register?submitted=True')
21     else:
22         form = RegisterForm()
23         if 'submitted' in request.GET:
24             submitted = True
25 
26     return render(request, 
27         'template/profile.html', 
28         {'form': form, 'submitted': submitted}
29         )