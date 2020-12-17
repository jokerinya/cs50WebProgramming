from django.contrib import admin
# from .models import User
from .models import *
# Register your models here.


class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "price")


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watching)
admin.site.register(Comment)
