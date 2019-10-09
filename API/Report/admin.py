from django.contrib import admin

# Register your models here.
from API.Report.models import GroupModel, PersonModel, DevelopmentDataModel, ReturnDataModel, PerformanceDataModel, HighSeasDataModel, TransferPerformanceDataModel


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'date_joined']
    search_fields = ['id']


class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'actual_name', 'group_id', 'status', 'date_joined']
    search_fields = ['id']


class DevelopmentDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_id', 'new_volume', 'success_opening_volume', 'business_introduction_volume', 'answer_question_volume', 'contract_pay_volume', 'quality_error_volume', 'data_time', 'date_joined']
    search_fields = ['id']


class ReturnDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_id', 'return_visit_volume', 'success_opening_volume', 'business_introduction_volume', 'answer_question_volume', 'contract_pay_volume', 'quality_error_volume', 'data_time', 'date_joined']
    search_fields = ['id']


class HighSeasDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_id', 'high_seas_volume', 'success_opening_volume', 'business_introduction_volume', 'answer_question_volume', 'contract_pay_volume', 'quality_error_volume', 'data_time', 'date_joined']
    search_fields = ['id']


class PerformanceDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_id', 'new_addition_volume', 'talkable_volume', 'work_customer_volume', 'transaction_volume', 'source', 'data_time', 'date_joined']
    search_fields = ['id']


class TransferPerformanceDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'person_id', 'development_volume', 'transfer_volume', 'data_time', 'date_joined']
    search_fields = ['id']


admin.site.register(GroupModel, GroupAdmin)
admin.site.register(PersonModel, PersonAdmin)
admin.site.register(DevelopmentDataModel, DevelopmentDataAdmin)
admin.site.register(ReturnDataModel, ReturnDataAdmin)
admin.site.register(PerformanceDataModel, PerformanceDataAdmin)
admin.site.register(HighSeasDataModel, HighSeasDataAdmin)
admin.site.register(TransferPerformanceDataModel, TransferPerformanceDataAdmin)
