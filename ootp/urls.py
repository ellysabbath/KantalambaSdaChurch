from django.urls import path
from . import views  
from .views import (
    VenturesMainPlansViewSet,
    VenturesMonthlyAccountViewSet,
    VenturesLeaderCredentialsViewSet,
    CommunicationLeaderCredentialsView,
    CommunicationMainGoalsView,
    CommunicationAssetsView,
    EducationEventsListView,
    educationLeaderListView,
    educationLeaderAllMembersListCreateView,
    educationLeaderGoalsListCreateView,
    SpecialNeedsListCreateView,
    SpecialNeedsDisabledMembersListCreateView,
    SpecialNeedsEventsListCreateView,
    SpecialNeedsMainGoalsListCreateView,
    EducationLeaderPostsListsCreateView,
    EducationFeesDeficitMembersListCreateView,
    EducationOwnedAssetsListCreateView
  
)
from .views import get_profile_image,landing,VenturesMainPlansViewSet,MedicalMissionaryEventDetailsListView,MedicalMissionaryListCreateView,MedicalMissionaryHealthStatusOfMembersListCreateView, VenturesMonthlyAccountViewSet, VenturesLeaderCredentialsViewSet,UserProfileView,VentureListCreateView,EventsListCreateView,ZoneHistoryListCreateView,AllMembersList,TreasurerRecordsList,TreasurerList, TreasurerGoalList, TreasurerAmountCollectedList, TreasurerAmountUsedList

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.landing, name='landing'),
    path('signup/', views.SignUp, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('verify-email/<str:username>/', views.Verify_email, name='verify-email'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path('tucasa/', views.index, name='index'),
    path('request-reset-password/', views.request_reset_password, name='request-reset-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset-password'),
    path('logout/', views.logout_view, name='logout'),  # Add the logout URL
    path('send-otp/', views.send_sms, name='send_sms'),
    path('status-callback/', views.message_status_callback, name='message_status_callback'),

    # ######################## internal ###################
    path('tucasa/User-Dashboard/', views.Dashboard, name="user-dashboard"),
    path('User-mhazini/', views.mhazini_view, name='mhazini'), 

    # ***********************************aptec and udom Tucasa zone**********************************
    path('aptec-admin/', views.aptecAdmin, name="aptec_admin"),
    path('aptec-all-members/', views.aptecAllMembers, name="aptec_all_members"),
    path('aptec-cive-branch/', views.aptecCive, name="aptec_cive"),
    path('aptec-coed-branch/', views.aptecCoed, name="aptec_coed"),
    path('aptec-Humanities-branch/', views.aptecHumanities, name="aptec_humanities"),
    path('aptec-medicalMissionary/', views.aptecMedicalMissionary, name="aptec_medicalMissionary"),
    path('aptec-spiritual/', views.aptecSpiritual, name="aptec_spiritual"),
    path('aptec-Tiba-branch/', views.aptecTiba, name="aptec_Tiba"),
    path('aptec-social-branch/', views.aptecSocial, name="aptec_social"),
    path('aptec-treasurer/', views.aptecTreasure, name="aptec_Treasurer"),
    path('zone-auditor/', views.auditor, name="auditor"),
    path('zone-chair/', views.chair, name="chair"),
    path('zone-chaplain/', views.chaplain, name="chaplain"),
    path('zone-communication/', views.communication, name="communication"),
    path('zone-medicalMissionary/', views.medicalMissionary, name="medicalMissionary"),
    path('zone-pastor/', views.pastor, name="pastor"),
    path('zone-all-members/', views.udomZoneAllMembers, name="udomzoneallmembers"),
    path('zone-history/', views.ZoneHistorical, name="History"),
    path('zone-education/', views.education, name="education"),
    path('zone-special-needs/', views.special, name="special"),
    path('zone-venture-api/', views.ventures, name="ventures"),
    path('user-profile-api/', views.profile, name="profile"),
    path('user-data-settings-api/', views.appsettings, name="settings"),
    path('page-to/update-your/profile/', views.updateProfile, name="updateProfile"),
    path('create-profile-API/',views.createProfile, name="createProfile"),
    # ***********************profile APIs*********************************
    path('api/registrations/', views.register.as_view(), name='user-registration'),
    path('users/', views.UserRegistrationListView.as_view(), name='user_registration_list'),
    path('update_user/', views.UpdateUserRegistrationView.as_view(), name='update_user_registration'),



    # **************************image profile**************************
    path('upload/', views.upload_image, name='upload_image'),
    path('imag/', get_profile_image, name='get_profile_image'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/userprofile/', UserProfileView.as_view(), name='userprofile-api'), 


    # *****************************************getting APIs for the data***************************
    path('api/treasurer-records/', TreasurerRecordsList.as_view(), name='treasurer-records-list'),
    path('api/treasurers/', TreasurerList.as_view(), name='treasurer-list'),
    path('api/treasurer-goals/', TreasurerGoalList.as_view(), name='treasurer-goal-list'),
    path('api/treasurer-amount-collected/', TreasurerAmountCollectedList.as_view(), name='treasurer-amount-collected-list'),
    path('api/treasurer-amount-used/', TreasurerAmountUsedList.as_view(), name='treasurer-amount-used-list'),
    path('api/all-members/', AllMembersList.as_view(), name='all-members-list'),
    path('api/zone-history/', ZoneHistoryListCreateView.as_view(), name='zone-history-list'),
    path('api/events/', EventsListCreateView.as_view(), name='events-list-create'),
    path('api/ventures/', VentureListCreateView.as_view(), name='vents'),
    path('api/ventures-main-plans/', VenturesMainPlansViewSet.as_view(), name='ventures_main_plans'),
    path('api/ventures-monthly-account/', VenturesMonthlyAccountViewSet.as_view(), name='ventures_monthly_account'),
    path('api/ventures-leader-credentials/', VenturesLeaderCredentialsViewSet.as_view(), name='ventures_leader_credentials'),
    path('api/medical-missionary/details-events/',MedicalMissionaryEventDetailsListView.as_view(), name='medical_missionary_events'),
    path('api/medical-missionary/', MedicalMissionaryListCreateView.as_view(),name='medica-missionary-leader'),
    path('api/members/health-status/fetch/',MedicalMissionaryHealthStatusOfMembersListCreateView.as_view(),name='health_status_ofMembers'),
    path('api/communication-leaders/', CommunicationLeaderCredentialsView.as_view(), name='communication_leaders'),
    path('api/communication-goals/', CommunicationMainGoalsView.as_view(), name='communication_goals'),
    path('api/communication-assets/', CommunicationAssetsView.as_view(), name='communication_assets'),
    path('api/education/Leader-View/api/',educationLeaderListView.as_view(),name='leader_fetch'),
    path('api/education/leader/goals/', educationLeaderGoalsListCreateView.as_view(),name='edu_goals'),
    path('api/edu-all/members/',educationLeaderAllMembersListCreateView.as_view(),name='edu_all_members'),
    path('api/special-needs/', SpecialNeedsListCreateView.as_view(), name='special-needs'),
    path('api/special-needs/disabled-members/', SpecialNeedsDisabledMembersListCreateView.as_view(), name='special-needs-disabled'),
    path('api/special-needs/events/', SpecialNeedsEventsListCreateView.as_view(), name='special-needs-events'),
    path('api/special-needs/goals/', SpecialNeedsMainGoalsListCreateView.as_view(), name='special-needs-goals'),
    path('api/posts/',EducationLeaderPostsListsCreateView.as_view(),name='edu_posts'),
    path('api/education/events/', EducationEventsListView.as_view(), name="edu_events"),
    path('api/feesdeficit/members/education/', EducationFeesDeficitMembersListCreateView.as_view(), name='fees_deficit'),
    path('api/edu-assets/', EducationOwnedAssetsListCreateView.as_view(), name='edu_assets'),

    # ******************************************admin password reset********************************


    

]
