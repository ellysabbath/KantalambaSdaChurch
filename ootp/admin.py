from django.contrib import admin
from .forms import RegisterForm
from .models import (
    SpecialNeeds,
    SpecialNeedsDisabledMembers,
    specialNeedsEvents,
    specialNeedsMainGoals,
    educationLeader,
    educationsLeadersGoals,
    educationLeaderAllMembers,
    EducationLeaderPosts,
    EducationEvents,
    EducationFeesDeficitMembers,
    EducationOwenedAssets
)

from .models import CustomUser, UserProfile,UserRegistration,Treasurer, TreasurerGoal, TreasurerAmountCollected, TreasurerAmountUsed

from .models import Treasurer, AllMembers,TreasurerRecords, Events, ZoneHistory,CommunicationLeaderCredentials, CommunicationMainGoals, CommunicationAssets,UserRegistration,Ventures, VenturesMainPlans, VenturesMonthlyAccount, VenturesLeaderCredentials,MedicalMissionary, MedicalMissionaryEventDetails, MedicalMissionaryHealthStatusOfMembers


# Register CustomUser with the CustomUserAdmin class


# ***********************************bonus options************************
@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'middle_name', 'last_name', 'email','phone_number','date_of_birth','city','church','baptism_status','gender','terms_agreement')
    search_fields = ('username', 'phone_number')  # Search by username or firstname
    list_filter = ('email', 'church')  # Filter by contribution type or month
    ordering = ('-church',)  # Order by month in descending order



    # ***********************user registration****************************

class TreasurerAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    ordering = ('-start_date',)


class TreasurerGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_amount', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


class TreasurerAmountCollectedAdmin(admin.ModelAdmin):
    list_display = ('amountCollected', 'source', 'dateOfCollection')
    list_filter = ('source', 'dateOfCollection')
    ordering = ('-dateOfCollection',)


class TreasurerAmountUsedAdmin(admin.ModelAdmin):
    list_display = ('amountUsed', 'aimOfUse', 'dateOfUse')
    list_filter = ('aimOfUse', 'dateOfUse')
    ordering = ('-dateOfUse',)


# Register each model to admin panel
admin.site.register(Treasurer, TreasurerAdmin)
admin.site.register(TreasurerGoal, TreasurerGoalAdmin)
admin.site.register(TreasurerAmountCollected, TreasurerAmountCollectedAdmin)
admin.site.register(TreasurerAmountUsed, TreasurerAmountUsedAdmin)

# *********************************end treasurer***************************************


@admin.register(AllMembers)
class AllMembersAdminWithInlines(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'email', 'MobNumber', 'collage', 'yearOfStudy', 'churchName')
    search_fields = ('username', 'firstname', 'email')
    list_filter = ('collage', 'yearOfStudy')
    ordering = ('username',)
   

@admin.register(ZoneHistory)
class ZoneHistoryAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'position', 'yearOfStudy', 'certificateStatus')
    search_fields = ('username', 'firstname', 'position')  # Search by username, firstname, or position
    list_filter = ('yearOfStudy', 'certificateStatus')  # Filter by year of study or certificate status
    ordering = ('yearOfStudy',)  # Order by year of study


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('nameOfAnEvent', 'date', 'costUsed')
    search_fields = ('nameOfAnEvent',)  # Search by event name
    ordering = ('-date',)  # Order by event date in descending order
    list_filter = ('date',)  # Filter by event date
# ***************************************bonus options*******************************


# class CustomUserAdmin(admin.ModelAdmin):
#     form = RegisterForm  # Optional: You can link your custom form for user creation
#     list_display = ('email', 'username', 'mobile_number', 'is_staff', 'is_active')  # Fields you want to display in the list view
#     search_fields = ('email', 'username')  # Enable search by email and username
#     ordering = ('email',)  # Optional: Order users by email


# **************************************for ventures*******************************



class VenturesAdmin(admin.ModelAdmin):
    list_display = ('name', 'established_date', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')
    ordering = ('established_date',)


class MainPlansAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'cost')
    list_filter = ('plan_type',)
    search_fields = ('name', 'description')
    ordering = ('plan_type',)


class MonthlyAccountAdmin(admin.ModelAdmin):
    list_display = ('name','account_balance', 'last_payment_date', 'is_active', 'monthlyGain', 'monthlyCost', 'monthlyProfit')
    list_filter = ('is_active',)
    ordering = ('-last_payment_date',)


class LeaderCredentialsAdmin(admin.ModelAdmin):
    list_display = ('leader_name', 'role', 'leader_email', 'leaderMobile')
    list_filter = ('role',)
    search_fields = ('leader_name', 'leader_email')
    ordering = ('leader_name',)


# Register all models
admin.site.register(Ventures, VenturesAdmin)
admin.site.register(VenturesMainPlans, MainPlansAdmin)
admin.site.register(VenturesMonthlyAccount, MonthlyAccountAdmin)
admin.site.register(VenturesLeaderCredentials, LeaderCredentialsAdmin)

admin.site.register(UserProfile)

# Optionally, if you have a custom user, register it too
admin.site.register(CustomUser)

# **********************************medical missionary****************************

@admin.register(MedicalMissionary)
class MedicalMissionaryAdmin(admin.ModelAdmin):
    list_display = ('goal_name', 'mission_date', 'cost', 'active')
    search_fields = ('goal_name',)
    list_filter = ('active', 'mission_date')
    ordering = ('-mission_date',)


@admin.register(EducationEvents)
class EducationEventsAdmin(admin.ModelAdmin):
    list_display = ('event_name','date_of_event','cost_used')
    search_fields=('event_name','date_of_event','cost_used')
    list_filter=('event_name','date_of_event','cost_used')
    ordering=('event_name','date_of_event','cost_used')


@admin.register(EducationOwenedAssets)
class educationOwnedAssetsAdmin(admin.ModelAdmin):
    list_display=('AssetName', 'value')
    search_fields=('AssetName', 'value')
    ordering=('AssetName', 'value')
    list_filter=('AssetName', 'value')

@admin.register(EducationFeesDeficitMembers)
class educationFeesDeficitMembersAdmin(admin.ModelAdmin):
    list_display=('firstName', 'collage', 'feesStatus')
    search_fields=('firstName', 'collage', 'feesStatus')
    ordering=('firstName', '-collage', 'feesStatus')
    list_filter=('firstName', 'collage', 'feesStatus')
    




@admin.register(MedicalMissionaryEventDetails)
class MedicalMissionaryEventDetailsAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'event_location', 'missionary_name', 'cost', 'output_raised')
    search_fields = ('event_name', 'event_location', 'missionary_name')
    list_filter = ('event_date',)
    ordering = ('-event_date',)


@admin.register(MedicalMissionaryHealthStatusOfMembers)
class MedicalMissionaryHealthStatusOfMembersAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'health_condition', 'member_collage', 'follow_up_date', 'missionary_name')
    search_fields = ('member_name', 'health_condition', 'username')
    list_filter = ('member_collage', 'follow_up_date')
    ordering = ('-follow_up_date',)
# *****************************************communication party********************
# --- Admin for Communication ---
@admin.register(CommunicationLeaderCredentials)
class LeaderCredentialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'mobile', 'established_date', 'is_active')
    list_filter = ('is_active', 'role')
    search_fields = ('name', 'role', 'email', 'mobile')
    ordering = ('-established_date',)



# --- Admin for MainGoals ---
@admin.register(CommunicationMainGoals)
class MainGoalsAdmin(admin.ModelAdmin):
    list_display = ('goal_title', 'achieved', 'cost')
    list_filter = ('achieved',)
    search_fields = ('goal_title', 'goal_description')
    ordering = ('-cost',)


# --- Admin for Assets ---
@admin.register(CommunicationAssets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'asset_type', 'quantity', 'value', 'acquired_date')
    list_filter = ('asset_type',)
    search_fields = ('asset_name', 'asset_type')
    ordering = ('-acquired_date',)


# ******************************Treasurer records of the zone**********************
class TreasurerRecordsAdmin(admin.ModelAdmin):
    # List the fields to display in the table
    list_display = ('username', 'firstname', 'contributionType', 'month', 'AmountPaid', 'collage')
    
    # Make these fields searchable
    search_fields = ('username', 'firstname', 'collage')
    
    # Add filters for the admin list view
    list_filter = ('contributionType', 'collage', 'month')
    
    # Allow the user to filter by month and contributionType
    date_hierarchy = 'month'
    
    # Optionally, add an "extra" empty form for new data
    # Allow admins to add a new record while viewing the list of existing ones
    # The `extra` number adds that number of extra empty forms
    # In this case, it allows them to add up to one extra record.
    extra = 1
    
    # Ordering of records by month (descending, most recent first)
    ordering = ('-month',)
    
    # Display a custom field as part of the list display
    def amount_status(self, obj):
        return "Paid" if obj.AmountPaid > 0 else "Not Paid"
    
    amount_status.short_description = "Payment Status"
    
    # Add custom field to display in the list view
    list_display = ('username', 'firstname', 'contributionType', 'month', 'AmountPaid', 'collage', 'amount_status')

# Register the model with the admin site
admin.site.register(TreasurerRecords, TreasurerRecordsAdmin)

# ***************************************88special needs*************************
@admin.register(SpecialNeeds)
class SpecialNeedsAdmin(admin.ModelAdmin):
    list_display = ('username', 'fullname', 'bodyAbility')
    search_fields = ('username', 'fullname', 'bodyAbility')
    list_filter = ('bodyAbility',)
    ordering = ('fullname',)


@admin.register(SpecialNeedsDisabledMembers)
class SpecialNeedsDisabledMembersAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'email',
        'collage',
        'mobile_number',
        'problem',
        'body_ability_status',
        
    )
    search_fields = (
        'username',
        'first_name',
        'email',
        'collage',
        'mobile_number',
        'problem',
    )
    list_filter = (
        'collage',
        'body_ability_status',
        'problem',
    )
    ordering = ('username',)



@admin.register(specialNeedsEvents)
class SpecialNeedsEventsAdmin(admin.ModelAdmin):
    list_display = ('eventName', 'date', 'location', 'cost')
    search_fields = ('eventName', 'location')
    list_filter = ('location', 'date')
    ordering = ('-date',)


@admin.register(specialNeedsMainGoals)
class SpecialNeedsMainGoalsAdmin(admin.ModelAdmin):
    list_display = ('goal_name', 'location', 'date')
    search_fields = ('goal_name', 'location')
    list_filter = ('location', 'date')
    ordering = ('-goal_name',)


# **************************education leader**************************
@admin.register(educationLeader)
class educationLeaderAdmin(admin.ModelAdmin):
    list_display=('fullname','username','email','mobileNumber','image','dateJoined','collage','program','yearOfStudy')
    search_fields=('fullname','username','email','mobileNumber','image','dateJoined','collage','program','yearOfStudy')
    list_filter=('fullname','username','email','mobileNumber','image','dateJoined','collage','program','yearOfStudy')
    ordering=('-username',)
    

@admin.register(educationLeaderAllMembers)
class educationLeaderAllMembersAdmin(admin.ModelAdmin):
    list_display=('fullname','username','email','mobileNumber','image','dateJoined','collage','program','yearOfStudy')
    search_fields=('fullname','username','email','mobileNumber','image','dateJoined','collage','program','yearOfStudy')
    list_filter=('fullname','username','email','mobileNumber','image','dateJoined','collage','program','yearOfStudy')
    ordering=('-username',)


@admin.register(educationsLeadersGoals)
class educationsLeadersGoalsAdmin(admin.ModelAdmin):
    list_display=('goalName','cost','expression','status')
    search_fields=('goalName','cost','expression','status')
    list_filter=('goalName','cost','expression','status')
    ordering=('goalName','cost','expression','status')



# *****************posts******************
admin.site.register(EducationLeaderPosts)

admin.site.site_header = "TUCASA UDOM ZONE   ADMIN DASHBOARD"
admin.site.site_title = "TUCASA UDOM ZONE  ADMIN PORTAL"
admin.site.index_title = "welcome to TUCASA udom zone"