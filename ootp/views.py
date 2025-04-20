from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import OtpToken,AllMembers,educationLeader,educationLeaderAllMembers,educationsLeadersGoals,MedicalMissionary,CommunicationLeaderCredentials, CommunicationMainGoals, CommunicationAssets,MedicalMissionaryEventDetails,MedicalMissionaryHealthStatusOfMembers,VenturesMainPlans, VenturesMonthlyAccount, VenturesLeaderCredentials,ZoneHistory,Ventures,Events, UserProfile, UserRegistration,Treasurer, TreasurerGoal, TreasurerAmountCollected, TreasurerAmountUsed,TreasurerRecords
from .serializers import  UserRegistrationSerializer,educationLeaderSerializers,MedicalMissionaryEventDetailsSerializers,MedicalMissionaryHealthStatusOfMembersSerializers,VenturesMainPlansSerializer, VenturesMonthlyAccountSerializer, VenturesLeaderCredentialsSerializer,MedicalMissionarySerializers,VenturesSerializers,EventsSerializer,ZoneHistorySerializer,AllMembersSerializer,UserProfileSerializer,TreasurerRecordsSerializer,TreasurerSerializer, TreasurerGoalSerializer, TreasurerAmountCollectedSerializer, TreasurerAmountUsedSerializer
from django.urls import reverse
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from django.contrib import messages
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
import secrets
import json
import logging
import string
import phonenumbers
from twilio.rest import Client  # Twilio to send SMS
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .serializers import (
    CommunicationLeaderCredentialsSerializer,
    CommunicationMainGoalsSerializer,
    CommunicationAssetsSerializer,
    educationLeaderAllMembersSerializers,
    educationsLeadersGoalsSerializers,
    SpecialNeedsSerializer,
    SpecialNeedsDisabledMembersSerializer,
    SpecialNeedsEventsSerializer,
    EducationLeaderPostsSerializer,
    EducationEventsSerializer,
    SpecialNeedsMainGoalsSerializer,
    EducationOwenedAssetsSerialzer,
    EducationFeesDeficitMembersSerializers
)


from .models import (
    SpecialNeeds,
    SpecialNeedsDisabledMembers,
    specialNeedsEvents,
    specialNeedsMainGoals,
    EducationLeaderPosts,
    EducationEvents,
    EducationFeesDeficitMembers,
    EducationOwenedAssets,
    
)


# Twilio configuration (replace with your actual credentials)
# TWILIO_PHONE_NUMBER = '+12766008030'
# TWILIO_SID = 'AC380fd733caa676f79347b1ed86b0be0f'
# TWILIO_AUTH_TOKEN = 'cbef6c8a3cce29de9593b1526ba2a377'

# Function to generate and send OTP to mobile number via Twilio
# Set up logging to capture errors and debug information
# logger = logging.getLogger(__name__)

# def send_otp_to_mobile(mobile_number, otp_code):
#     try:
#         # Ensure phone number is in E.164 format
#         parsed_number = phonenumbers.parse(mobile_number, "TZ")  # Replace "TZ" with correct region code
#         if not phonenumbers.is_valid_number(parsed_number):
#             raise ValueError(f"Invalid phone number: {mobile_number}")
        
#         formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

#         # Log the formatted phone number for debugging
#         logger.debug(f"Sending OTP to mobile number: {formatted_number}")

#         # Initialize Twilio client
#         client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

#         # Send OTP via SMS
#         message = client.messages.create(
#             body=f"Your OTP is: {otp_code}. It will expire in 5 minutes.",
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=formatted_number
#         )

#         # Log the message SID to confirm the message was sent
#         logger.debug(f"Message sent successfully. SID: {message.sid}")
#         return message.sid  # Return the message SID for tracking if needed

#     except Exception as e:
#         # Log the error
#         logger.error(f"Error sending OTP to mobile number {mobile_number}: {e}")
#         raise e

# Function to send OTP to email

def send_otp_to_email(email, otp_code):
    subject = "Email Verification"
    message = f"Hi there,\nHere is your OTP: {otp_code}\nIt expires in 5 minutes."
    sender = "iyumbusda@gmail.com"
    receiver = [email]
    send_mail(subject, message, sender, receiver, fail_silently=False)

# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")

def SignUp(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Generate OTP (6-digit random number)
            otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))

            # Create OTP record for the user
            otp = OtpToken.objects.create(
                user=user,
                otp_code=otp_code,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )

            # Send OTP to user's email
            send_otp_to_email(user.email, otp_code)

            # Send OTP to user's mobile number if available
            # Uncomment the next line if you have a mobile number for the user
            # if user.mobile_number:
            #     send_otp_to_mobile(user.mobile_number, otp_code)

            # Now send the success message
            messages.success(request, f"Account created successfully! An OTP was sent to your email and mobile number. OTP: {otp_code}")

            return redirect("verify-email", username=user.username)
        else:
            messages.error(request, "There was an error with your form. Please try again.")
    
    context = {"form": form}
    return render(request, "signup.html", context)

def Verify_email(request, username):
    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("signup")

    user_otp = OtpToken.objects.filter(user=user).last()

    if not user_otp:
        messages.error(request, "No OTP found. Please request a new one.")
        return redirect("resend-otp")

    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code')

        if user_otp.otp_code == entered_otp:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully! You can now login.")
                return redirect("signin")
            else:
                messages.warning(request, "The OTP has expired. Please request a new one.")
                return redirect("resend-otp")
        else:
            messages.warning(request, "Invalid OTP. Please try again.")
            return redirect(reverse("verify-email", kwargs={"username": user.username}))

    context = {'username': username, 'otp': user_otp}
    return render(request, "verify_token.html", context)

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST.get("otp_email")
        
        try:
            user = get_user_model().objects.get(email=user_email)

            otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))  # Generate new OTP

            otp = OtpToken.objects.create(
                user=user,
                otp_code=otp_code,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )

            # Send OTP via email
            send_otp_to_email(user.email, otp_code)

            # Send OTP via mobile if available
            # if user.mobile_number:
            #     send_otp_to_mobile(user.mobile_number, otp_code)

            messages.success(request, f"A new OTP has been sent to your email and mobile number. OTP: {otp_code}")

            return redirect("verify-email", username=user.username)

        except get_user_model().DoesNotExist:
            messages.warning(request, "This email doesn't exist in the records.")
            return redirect("resend-otp")

    return render(request, "resend_otp.html")

def signin(request):
    if request.user.is_authenticated:
        return redirect("user-dashboard")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("user-dashboard")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            print(messages.get_messages(request))  # This will print the messages to the console
            return render(request, "login.html")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('signin')

# Password reset views (step 1)
def request_reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = get_user_model().objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            subject = "Password Reset Request"
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'uid': uid,
                'token': token,
            })
            send_mail(subject, message, 'no-reply@yourdomain.com', [email], fail_silently=False)
            
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect("signin")
        
        except get_user_model().DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return redirect("request-reset-password")

    return render(request, "request_reset_password.html")

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("signin")
            
            return render(request, "reset_password.html", {'uid': uidb64, 'token': token})
        else:
            messages.error(request, "The password reset link is invalid or has expired.")
            return redirect("signin")
    
    except Exception as e:
        messages.error(request, "There was an error processing your request. Please try again.")
        return redirect("signin")

def send_password_reset_email(user):
    uid = urlsafe_base64_encode(user.pk.encode())
    token = default_token_generator.make_token(user)
    reset_url = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

    subject = "Password Reset Request"
    html_message = render_to_string('password_reset_email.html', {
        'user': user,
        'uid': uid,
        'token': token,
    })
    plain_message = f"Hi {user.username},\n\nWe received a request to reset your password. Please click the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email."

    send_mail(
        subject,
        plain_message,
        'iyumbusda@gmail.com',
        [user.email],
        html_message=html_message,
    )



# Your Twilio account SID and Auth token
account_sid = 'AC380fd733caa676f79347b1ed86b0be0f'
auth_token = 'cbef6c8a3cce29de9593b1526ba2a377'

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def send_sms(request):
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body="Your OTP code is 123456",
            from_='+12766008030',  # Your Twilio phone number
            to='+255742578691'  # The recipient's phone number
        )
        
        # After sending the message, fetch the message status
        message_sid = message.sid  # Get the SID of the sent message
        message_status = client.messages(message_sid).fetch().status  # Fetch the message and check its status

        # Log the message status for debugging purposes
        logging.debug(f"Message SID: {message_sid}, Message Status: {message_status}")

        # Respond with the message status
        return HttpResponse(f"Message sent successfully: {message.sid}. Status: {message_status}")

    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return HttpResponse(f"Failed to send message: {e}")
    

    # This view will handle the callback from Twilio
def message_status_callback(request):
    message_sid = request.GET.get('MessageSid')
    message_status = request.GET.get('MessageStatus')
    logging.info(f"Message SID: {message_sid}, Status: {message_status}")

    # You can add your logic here to update your database or notify the user
    # For now, we'll just return a response to acknowledge receipt
    return JsonResponse({'status': 'Received', 'MessageSid': message_sid, 'MessageStatus': message_status})

@login_required
def Dashboard(request):
    return render(request, "registration/dashboard.html")
@login_required
def mhazini_view(request):
    return render(request, "registration/Mhazini.html")

# *********************************************aptec udom zone****************************
@login_required
def aptecAdmin(request):
    return render(request, "registration/aptecAdmin.html")
@login_required
def aptecAllMembers(request):
    return render(request, "registration/aptecAllMembers.html")
@login_required
def aptecCive(request):
    return render(request, "registration/aptecCive.html")
@login_required
def aptecCoed(request):
    return render(request, "registration/aptecCoed.html")

def landing(request):
    return render(request, "landing.html")
@login_required
def aptecSocial(request):
    return render(request, "registration/aptecSocial.html")
@login_required
def aptecHumanities(request):
    return render(request, "registration/aptecHumanities.html")
@login_required
def aptecMedicalMissionary(request):
    return render(request, "registration/aptecMedicalMissionary.html")
@login_required
def aptecSpiritual(request):
    return render(request, "registration/aptecSpiritual.html")
@login_required
def aptecTiba(request):
    return render(request, "registration/aptecTiba.html")
@login_required
def aptecTreasure(request):
    return render(request, "registration/aptecTreasure.html")
@login_required
def auditor(request):
    return render(request, "registration/auditor.html")
@login_required
def chair(request):
    return render(request, "registration/chair.html")
@login_required
def chaplain(request):
    return render(request, "registration/chaplain.html")

@login_required
def communication(request):
    return render(request, "registration/communication.html")
@login_required
def medicalMissionary(request):
    return render(request, "registration/medicalMissionary.html")
@login_required
def pastor(request):
    return render(request, "registration/pastor.html")
@login_required
def udomZoneAllMembers(request):
    return render(request, "registration/udomZoneAllMembers.html")
@login_required
def ventures(request):
    return render(request, "registration/ventures.html")
@login_required
def ZoneHistorical(request):
    return render(request, "registration/ZoneHistory.html")
@login_required
def education(request):
    return render(request, "registration/education.html")

@login_required
def special(request):
    return render(request, "registration/special.html")
@login_required
def profile(request):
    return render(request, "registration/profile.html")
@login_required
def appsettings(request):
    return render(request, "registration/settings.html")


def createProfile(request):
    return render(request, 'registration/createProfile.html')



# class UserProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'accounts/users/user-profile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user  # Add user context here
#         return context
@login_required
def updateProfile(request):
    return render(request, "registration/update-profile.html")

# *******************************end rendering pages for zone***********************************


# ************************handling data****************************
class register(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Registration successful", "user_id": user.id}, status=status.HTTP_201_CREATED)

        # 🔍 Log the exact errors to the console
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# *******************retrieving profile data******************************

class UserRegistrationListView(generics.ListAPIView):
    queryset = UserRegistration.objects.all()  # Fetch all records from the database
    serializer_class = UserRegistrationSerializer
# *****************************updating profile data************************************

class UpdateUserRegistrationView(APIView):

    def put(self, request, *args, **kwargs):
        # Get the username from the request data
        username = request.data.get('username')
        try:
            # Find the user by username
            user = UserRegistration.objects.get(username=username)

            # Update the user fields
            user.first_name = request.data.get('first_name', user.first_name)
            user.middle_name = request.data.get('middle_name', user.middle_name)
            user.last_name = request.data.get('last_name', user.last_name)
            user.email = request.data.get('email', user.email)
            user.phone_number = request.data.get('phone_number', user.phone_number)
            user.date_of_birth = request.data.get('date_of_birth', user.date_of_birth)
            user.city = request.data.get('city', user.city)
            user.church = request.data.get('church', user.church)
            user.baptism_status = request.data.get('baptism_status', user.baptism_status)
            user.gender = request.data.get('gender', user.gender),
            user.password = request.data.get('password', user.password),
            # Password update if necessary
            
            
            # Terms agreement (If any special logic needed)
            terms_agreement = request.data.get('terms_agreement', False)
            # Process terms agreement if needed

            user.save()

            return Response({"message": "User updated successfully!"}, status=status.HTTP_200_OK)
        
        except UserRegistration.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
# ***************************image upload*************************
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)  # Update existing
    except UserProfile.DoesNotExist:
        serializer = UserProfileSerializer(data=request.data)  # Create new
        profile = None

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201 if profile is None else 200)
    
    return Response(serializer.errors, status=400)


    # ****************************image fetching****************************


@login_required
def get_profile_image(request):
    try:
        user = request.user
        
        # Check if the user has a profile image
        if user.image and user.image.image:
            image_url = user.image.image.url  # Get the URL of the user's profile image
        else:
            image_url = '\media\images\elly.jpg'  # Default image if no profile image

        return JsonResponse({'image': image_url})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



        # ***********************get profile image with login**************************
# class UserProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'registration/settings.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user  # Add user context here
#         return context
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
# ***************************GETTING LOGICS FOR  APIs DEVELOPMENT******************************
class TreasurerRecordsList(APIView):
    """
    Fetch contribution records of the authenticated user only.
    """
    def get(self, request):
        if request.user.is_authenticated:  # Ensure the user is authenticated
            # Filter the contribution records based on the authenticated user
            contributions = TreasurerRecords.objects.filter(username=request.user.username)
            
            # Serialize the filtered data
            serializer = TreasurerRecordsSerializer(contributions, many=True)
            
            # Return the response with serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If user is not authenticated, return an error response
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

class TreasurerList(APIView):
    def get(self, request):
        treasurers = TreasurerRecords.objects.all()
        serializer = TreasurerSerializer(treasurers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API View for fetching all TreasurerGoal data
class TreasurerGoalList(APIView):
    def get(self, request):
        goals = TreasurerGoal.objects.all()
        serializer = TreasurerGoalSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API View for fetching all TreasurerAmountCollected data
class TreasurerAmountCollectedList(APIView):
    def get(self, request):
        collected_amounts = TreasurerAmountCollected.objects.all()
        serializer = TreasurerAmountCollectedSerializer(collected_amounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API View for fetching all TreasurerAmountUsed data
class TreasurerAmountUsedList(APIView):
    def get(self, request):
        used_amounts = TreasurerAmountUsed.objects.all()
        serializer = TreasurerAmountUsedSerializer(used_amounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# *********************************all members**********************************
class AllMembersList(APIView):
    def get(self, request):
        members = AllMembers.objects.all()
        serializer = AllMembersSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ZoneHistoryListCreateView(APIView):
 def get(self, request):
    queryset = ZoneHistory.objects.all()
    serializer_class = ZoneHistorySerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

class EventsListCreateView(APIView):
 def get(self, request):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)

class VentureListCreateView(APIView):
    def get(self, request):
        ventures=Ventures.objects.all()
        serializer_class=VenturesSerializers(ventures, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
    
class MedicalMissionaryListCreateView(APIView):
    def get(self, request):
        query=MedicalMissionary.objects.all()
        serializers_class=MedicalMissionarySerializers(query, many=True)
        return Response(serializers_class.data, status=status.HTTP_200_OK)
    

class MedicalMissionaryEventDetailsListView(APIView):
    def get(self, request):
        query=MedicalMissionaryEventDetails.objects.all()
        serial=MedicalMissionaryEventDetailsSerializers(query,many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class MedicalMissionaryHealthStatusOfMembersListCreateView(APIView):
    def get(self, request):
        query = MedicalMissionaryHealthStatusOfMembers.objects.all()
        serial=MedicalMissionaryHealthStatusOfMembersSerializers(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class VenturesMainPlansViewSet(APIView):
 def get(self, request):
    queryset = VenturesMainPlans.objects.all()
    serializer_class = VenturesMainPlansSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)


class VenturesMonthlyAccountViewSet(APIView):
 def get(self, request):

    queryset = VenturesMonthlyAccount.objects.all()
    serializer_class = VenturesMonthlyAccountSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)


class VenturesLeaderCredentialsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example: Assuming 'role' links to the authenticated user.
        # Modify this line according to how your model associates credentials with a user.
        queryset = VenturesLeaderCredentials.objects.filter(role=request.user.username)
        
        # Serialize the data
        serializer = VenturesLeaderCredentialsSerializer(queryset, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
 

class CommunicationLeaderCredentialsView(APIView):
    def get(self, request):
        queryset = CommunicationLeaderCredentials.objects.all()
        serializer = CommunicationLeaderCredentialsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CommunicationMainGoalsView(APIView):
    def get(self, request):
        queryset = CommunicationMainGoals.objects.all()
        serializer = CommunicationMainGoalsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CommunicationAssetsView(APIView):
    def get(self, request):
        queryset = CommunicationAssets.objects.all()
        serializer = CommunicationAssetsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class educationLeaderListView(APIView):
    def get(self, request):
        query=educationLeader.objects.all()
        serial=educationLeaderSerializers(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)

class   educationLeaderAllMembersListCreateView(APIView):
 def get(self, request):
     query=educationLeaderAllMembers.objects.all()
     serial=educationLeaderAllMembersSerializers(query, many=True)
     return Response(serial.data, status=status.HTTP_200_OK)
 

class educationLeaderGoalsListCreateView(APIView):
    def get(self, request):
        query=educationsLeadersGoals.objects.all()
        serial=educationsLeadersGoalsSerializers(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
    
class EducationLeaderPostsListsCreateView(APIView):
     def get(self, request):
        query=EducationLeaderPosts.objects.all()
        serial=EducationLeaderPostsSerializer(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
     
class EducationEventsListView(APIView):
    def get(self, request):
        query=EducationEvents.objects.all()
        serial=EducationEventsSerializer(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
class EducationFeesDeficitMembersListCreateView(APIView):
    def get(self, request):
        query=EducationFeesDeficitMembers.objects.all()
        serial=EducationFeesDeficitMembersSerializers(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
    
class EducationOwnedAssetsListCreateView(APIView):
    def get(self, request):
        query=EducationOwenedAssets.objects.all()
        serial=EducationOwenedAssetsSerialzer(query, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
    
class SpecialNeedsListCreateView(APIView):
 def get(self, request):
    queryset = SpecialNeeds.objects.all()
    serial=SpecialNeedsSerializer(queryset, many=True)
    return Response(serial.data, status=status.HTTP_200_OK)
    
class SpecialNeedsDisabledMembersListCreateView(APIView):
 def get(self, request):
    queryset = SpecialNeedsDisabledMembers.objects.all()
    serializer_class = SpecialNeedsDisabledMembersSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)


class SpecialNeedsEventsListCreateView(APIView):
 def get(self, request):
    queryset = specialNeedsEvents.objects.all()
    serializer_class = SpecialNeedsEventsSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)


class SpecialNeedsMainGoalsListCreateView(APIView):
 def get(self, request):
    queryset = specialNeedsMainGoals.objects.all()
    serializer_class = SpecialNeedsMainGoalsSerializer(queryset, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
 
