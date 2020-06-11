import xadmin

from .models import User, UserRelationship, CheckCode


class UserAdmin(object):
    list_display = ['nickname', 'username', 'email', 'gender', 'address', 'description', 'image', ]
    search_fields = ['nickname', ]
    list_filter = ["nickname", "email", "gender", "address", "description", ]


class CheckCodeAdmin(object):
    list_display = ['user', 'check_code', 'add_time', ]
    search_fields = ['user', 'check_code', ]
    list_filter = ["user", "check_code", "add_time", ]


class UserRelationshipAdmin(object):
    list_display = ['from_user', 'to_user', 'add_time', ]
    search_fields = ['from_user', 'to_user', 'add_time', ]
    # list_editable = ["is_hot", ]
    list_filter = ['from_user', 'to_user', 'add_time', ]


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
xadmin.site.register(CheckCode, CheckCodeAdmin)
xadmin.site.register(UserRelationship, UserRelationshipAdmin)
