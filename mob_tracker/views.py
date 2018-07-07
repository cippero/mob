from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Entry, Tip, Profile, TipVote
from .forms import LoginForm, UserForm, SearchForm, EntryForm, TipForm, TipVoteForm
from django.conf import settings
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions, SemanticRolesOptions
import json
import requests
import statistics as s
# from django.db.models import Q
import nltk
# nltk.download('punkt') #set up on heroku?
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def merge_queries(filtered_sentence, i, queryset=Entry.objects.none()): 
	if i == -1: return queryset
	else:
		query = Entry.objects.filter(title_clean__contains=filtered_sentence[i]).order_by('title_clean')
		return merge_queries(filtered_sentence, i-1, queryset | query)

def index(request):
	categories_list = Entry.objects.values('category').order_by('category')
	categories = []
	for i in range(len(categories_list)): categories.append(categories_list[i]['category'])
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query']		
			stop_words = set(stopwords.words('english'))
			word_tokens = word_tokenize(query)
			filtered_sentence = list(set([w.lower() for w in word_tokens if not w in stop_words and w.isalnum()]))
			entries = Entry.objects.none()
			if len(filtered_sentence) == 1:
				entries = Entry.objects.filter(title_clean__contains=filtered_sentence[0]).order_by('title_clean')
			elif len(filtered_sentence) > 1:
				entries = merge_queries(filtered_sentence, len(filtered_sentence)-1)
			print({'entries': entries, 'query': filtered_sentence})
			return render(request, 'index.html', {'entries': entries, 
													'form': '', 
													'query': filtered_sentence, 
													'categories': categories})
		else:
			# print('FORM:', form)
			# print('FORM.ERRORS:', form.errors)
			# add error handling to forms
			# error handling for empty search
			entries = Entry.objects.order_by('-add_date')
			return render(request, 'index.html', {'entries': entries, 
													'form': form, 
													'query': '', 
													'categories': categories})
	else:
		entries = Entry.objects.order_by('title_clean')
		# print({'entries': entries})
		return render(request, 'index.html', {'entries': entries, 
												'form': '', 
												'query': '', 
												'categories': categories})


def entry_view(request, entry_title):
	if request.method == 'POST':
		form = EntryForm(request.POST)
		if form.is_valid():
			# print('FORM HERE')
			t = form.cleaned_data['title']
			c = form.cleaned_data['category']
			sc = form.cleaned_data['subcategory']
			d = form.cleaned_data['description']

			entry = Entry.objects.create(title=t, 
										title_clean="".join(e for e in t if e.isalnum()), 
										category=c, 
										subcategory=sc, 
										description=d)
			user = Profile.objects.get(user=request.user)
			entry.contributors.add(user)
			return render(request, 'entry.html', {'entry': entry, 'contributors': [user]})
		else:
			# print('FORM:', form)
			# print('FORM.ERRORS:', form.errors)
			return render(request, 'entry.html', {'entry': '', 'contributors': ''})
	else:
		# print(entry_title, type(entry_title))
		entry = Entry.objects.get(title_clean=str(entry_title))
		user = Profile.objects.get(user=request.user)
		contributors = Profile.objects.filter(entries=entry.id)
		comments = Tip.objects.filter(topic=entry).order_by('-add_date')
		# print(Profile.objects.filter(entries=entry['id']))
		# print(entry.id)

		# if user not in tip['voters']: tip.voters.add(user)
		# voters = Tip.objects.filter()
		# comments = user.comments.all().values()
		# for i in range(len(comments)):
			# tip = Tip.objects.get(id=tip_id)
			# users = Profile.objects.filter(tips=comments[i]['id'])
			# comments[i]['voters'] = users
			# print(comments[i]['voters'])


		return render(request, 'entry.html', {'entry': entry, 'contributors': contributors, 'comments': comments, 'user': user})

def tip_view(request, entry_title):
	if request.method == 'POST':
		form = TipForm(request.POST)
		if form.is_valid():
			comment = {}
			color = '255,255,255'
			comment['body'] = form.cleaned_data['body']
			if len(comment['body']) > 10:
				response = settings.NATURAL_LANGUAGE_PROCESSING.analyze(
					text=comment['body'],
					features=Features(
						keywords=KeywordsOptions(
							emotion=True,
							sentiment=True,
							limit=5)))
				# print(json.dumps(response, indent=2))
				scores, red, green, blue = [], [], [], []
				for keyword in response['keywords']:
					scores.append((int(keyword['relevance']*10.0)+int(keyword['sentiment']['score']*10.0))//2)
					# red.append(keyword['emotion']['joy']*255)
					# green.append((keyword['emotion']['anger'] + keyword['emotion']['disgust'])*255//2)
					# blue.append((keyword['emotion']['fear'] + keyword['emotion']['sadness'])*255//2)
				comment['score'] = s.mean(scores)+1
				# print('SCORE:', comment['score'])
				# comment['color'] = hex(int(s.mean(red)))[1:] + hex(int(s.mean(green)))[1:] + hex(int(s.mean(blue)))[1:]
				# comment['color'] = {'r': int(s.mean(red)), 'g': int(s.mean(green)), 'b': int(s.mean(blue))}
				# color = '%s,%s,%s' % (comment['color']['r'], comment['color']['g'], comment['color']['b'])
				# print('RED:', int(s.mean(red)))
				# print('GREEN:', int(s.mean(green)))
				# print('BLUE:', int(s.mean(blue)))
				# print('COMMENT COLOR:', comment['color'])
				# print('COLOR:', color)
			else:
				comment['score'] = 1
				# comment['color'] = {'r': 255, 'g': 255, 'b': 255}
			
			# print('ENTRY_TITLE:', entry_title)
			user = Profile.objects.get(user=request.user)
			entry = Entry.objects.get(title_clean=entry_title)
			contributors = Profile.objects.filter(entries=entry.id)
			if user not in contributors: entry.contributors.add(user)
			tip = Tip.objects.create(author=request.user,
									topic=entry,
									body=comment['body'],
									votes=comment['score'],
									color=color)
			tip.voters.add(user)
			tip_vote = TipVote.objects.create(tip=tip,
											user=request.user,
											polarity=True)
			return render(request, 'entry.html', {'comments': comment, 'user': user})
		else: 
			print(form)
			print('form errors', form.errors)
			return render(request, 'entry.html', {'form': form, 'tip': ''})
	else:
		return render(request, 'entry.html', {'form': form, 'tip': ''})

def tip_vote_view(request, tip_id):
	if request.method == 'POST':
		form = TipVoteForm(request.POST)
		if form.is_valid():
			p = form.cleaned_data['polarity']
			tip = Tip.objects.get(id=tip_id)
			tip_vote = None
			try:
				tip_vote = TipVote.objects.get(user=user)
				tip_vote.polarity = not tip_vote.polarity
				tip_vote.save(update_fields=['polarity'])
			except:
				tip_vote = TipVote.objects.create(tip=tip, 
												user=request.user, 
												polarity=p)

			user = Profile.objects.get(user=request.user)
			voters = Tip.objects.filter()
			if user not in voters: tip.voters.add(user)
			# if user not in tip['voters']: tip.voters.add(user)
			if p: tip.votes += 1
			else: tip.votes -= 1
			tip.save(update_fields=['votes'])

			return HttpResponseRedirect('/')
		else:
			print('form errors', form.errors)
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

def profile_view(request, username):
	browsing_user = User.objects.get(username=username)
	user = Profile.objects.get(user=browsing_user.id)
	entries = user.entries.all().values()
	for i in range(len(entries)):
		users = Profile.objects.filter(entries=entries[i]['id'])
		entries[i]['contributors'] = users
	return render(request, 'profile.html', {'profile': user, 'entries': entries})

def signup_view(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			u = form.cleaned_data['username']
			e = form.cleaned_data['email']
			p = form.cleaned_data['password']
			user = User.objects.create_user(u, e, p)
			login(request, user)
			return HttpResponseRedirect('/')
	else:
		form = UserForm()
		return render(request, 'signup.html', {'form': form})

def login_view(request):
	if request.method == 'POST':
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