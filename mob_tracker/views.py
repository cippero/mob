from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Entry, Tip, Profile
from .forms import LoginForm, UserForm, SearchForm, EntryForm
from django.conf import settings
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions, SemanticRolesOptions
import json
import requests

def index(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			q = form.cleaned_data['query']
			response = settings.NATURAL_LANGUAGE_PROCESSING.analyze(
				text=q,
				features=Features(
				# entities=EntitiesOptions(
				#   emotion=True,
				#   sentiment=True,
				#   limit=5),
				keywords=KeywordsOptions(
					# emotion=True,
					sentiment=True,
					limit=5),
				# concepts=ConceptsOptions(
				# 	limit=5),
				categories=CategoriesOptions(),
				semantic_roles=SemanticRolesOptions(
					entities=True,
					keywords=True,
					limit=1)))
			print(json.dumps(response, indent=2))
			query = {}
			query['semantic_roles'] = {
										'subject': response['semantic_roles'][0]['subject']['text'].title(), 
										'action': response['semantic_roles'][0]['action']['verb']['text'], 
										'object': response['semantic_roles'][0]['object']['text'].title()}
			query['keywords'] = []
			for keyword in response['keywords']:
				query['keywords'].append({
										'text': keyword['text'].title(), 
										'relevance': int(keyword['relevance']*100.0)})
			query['keywords_length'] = len(query['keywords'])
			query['categories'] = []
			for category in response['categories']: 
				query['categories'].append({'score': int(category['score']*100.0), 'label': str(category['label'])[1:].title()})
			
			# accesscode = request.GET.get('code')
			# redirect_uri = 'http://www.example.com'
			# url = 'https://www.linkedin.com/uas/oauth2/accessToken'

			# postdata = {
			# 	'grant_type': 'authorization_code',
			# 	'code': accesscode,
			# 	'redirect_uri': redirect_uri,
			# 	'client_id': consumer_key,
			# 	'client_secret': consumer_secret,
			# }

			# r = requests.post('http://localhost:8000/api/', data=query)
			# print(r.status_code)
			# print(r.text)

			return render(request, 'index.html', {'query': query, 'search': q})
		else: 
			print(form)
			print('form errors', form.errors)
			return render(request, 'index.html', {'form': form, 'search': ''})
	else:
		return render(request, 'index.html')

def signup_view(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			# ln = form.cleaned_data['last_name']
			# fn = form.cleaned_data['first_name']
			u = form.cleaned_data['username']
			e = form.cleaned_data['email']
			p = form.cleaned_data['password']
			user = User.objects.create_user(u, e, p)
			login(request, user)
			return HttpResponseRedirect('/')
	else:
		form = UserForm()
		return render(request, 'signup.html', {'form': form})

def entry_view(request, entry_title):
	if request.method == 'POST':
		form = UserForm(request.POST)
	# 	if form.is_valid():
	# 		# ln = form.cleaned_data['last_name']
	# 		# fn = form.cleaned_data['first_name']
	# 		u = form.cleaned_data['username']
	# 		e = form.cleaned_data['email']
	# 		p = form.cleaned_data['password']
	# 		user = User.objects.create_user(u, e, p)
	# 		login(request, user)
	# 		return HttpResponseRedirect('/')
	# else:
		# form = UserForm()
		# return render(request, 'signup.html', {'form': form})
	entry = Entry.objects.get(title_clean=entry_title)
	contributors = Profile.objects.filter(entries=entry.id)
	# print(Profile.objects.filter(entries=entry['id']))
	print(entry.id)
	return render(request, 'entry.html', {'entry': entry, 'contributors': contributors})

def profile_view(request, username):
	user = Profile.objects.get(user=request.user)
	# user = Profile.objects.get(user=request.user.username)
	# print('&&&&&&&&&&', request.user.username)
	# user = Profile.objects.get(user=username)
	entries = user.entries.all().values()
	for i in range(len(entries)):
		users = Profile.objects.filter(entries=entries[i]['id'])
		entries[i]['contributors'] = users
	return render(request, 'profile.html', {'profile': user, 'entries': entries})

def login_view(request):
	if request.method == 'POST':
		# if post, then authenticate (user submitted username and password)
		form = LoginForm(request.POST)
		if form.is_valid():
			u = form.cleaned_data['username']
			p = form.cleaned_data['password']
			user = authenticate(username = u, password = p)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/')
				else:
					print("The account has been disabled.")
					return HttpResponseRedirect('/login/')
			else:
				print("The username and/or password is incorrect.")
				return render(request, 'login.html', {'error': "The username and/or password is incorrect.", 'form': form})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')







# def party_list(request):
# 	parties = Party.objects.all()
# 	form = PartyForm()
# 	return render(request, 'party_list.html', {'parties': parties, 'form': form})


# class PartyList(ListView):
# 	context_object_name = 'parties'
# 	template_name = 'party_list.html'

# 	def get_queryset(self):
# 		return Party.objects.all()

# def party_detail(request, pk):
# 	# parties = Party.objects.all()
# 	# form_party = PartyForm()
# 	form_clown = ClownForm()
# 	party = None
# 	try: party = Party.objects.get(id=pk)
# 	except: pass
# 	return render(request, 'party_detail.html', {'party': party, 'form': form_clown})


# class PartyDetail(DetailView):
# 	template_name = 'party_detail.html'
# 	model = Party

# class PartyPost(CreateView):
# 	# template_name = 'party_list.html'
# 	model = Party
# 	success_url = reverse_lazy("party_list")
# 	fields = ['title', 'location', 'description']

# class ClownPost(CreateView):
# 	pk = ''
# 	def dispatch(self, request, *args, **kwargs):
# 		# self.party = get_object_or_404(Party, pk=kwargs['pk'])
# 		# print('%%%%% party number:', kwargs['pk'])
# 		pk = kwargs['pk']
# 		return super().dispatch(request, *args, **kwargs)

# 	# def form_valid(self, form):
# 	# 	form.instance.party = self.party
# 	# 	return super().form_valid(form)
# 	if pk != '': print('%%%%% party number:', pk)
# 	model = Clown
# 	success_url = reverse_lazy("party_detail", kwargs={'pk': pk})
# 	fields = ['name', 'description']

# class PartyDelete(DeleteView):
#     pass

# class PartyUpdate(UpdateView):
#     pass


