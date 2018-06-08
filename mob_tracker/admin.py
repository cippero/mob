from django.contrib import admin
from .models import Entry, Tip, Profile, TipVote


admin.site.register(Entry)
admin.site.register(Tip)
admin.site.register(Profile)
admin.site.register(TipVote)