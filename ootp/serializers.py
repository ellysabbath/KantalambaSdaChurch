from rest_framework import serializers
from .models import UserRegistration,educationLeaderAllMembers,educationsLeadersGoals,educationLeader,CommunicationLeaderCredentials, CommunicationMainGoals, CommunicationAssets,MedicalMissionaryHealthStatusOfMembers,MedicalMissionaryEventDetails,UserProfile,MedicalMissionary,VenturesMainPlans, VenturesMonthlyAccount, VenturesLeaderCredentials,ZoneHistory,Ventures,Events,TreasurerRecords,Treasurer,AllMembers, TreasurerGoal, TreasurerAmountCollected, TreasurerAmountUsed
from .models import (
    SpecialNeeds,
    SpecialNeedsDisabledMembers,
    specialNeedsEvents,
    specialNeedsMainGoals,
    EducationLeaderPosts,
    EducationFeesDeficitMembers,
    EducationOwenedAssets,
    EducationEvents
)
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserRegistration
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'phone_number',
            'username', 'date_of_birth', 'city', 'church', 'baptism_status',
            'gender', 'password', 'confirm_password', 'terms_agreement'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Password will be write-only
        }

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        
        # Ensure email and username are unique
        if UserRegistration.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        if UserRegistration.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("A user with this username already exists.")

        return data

    def create(self, validated_data):
        # Remove confirm_password field before saving the user
        validated_data.pop('confirm_password')
        
        # Create a new user entry with hashed password
        user = UserRegistration.objects.create(**validated_data)
        return user
    

# *************serializer for profile image*********************

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['image'] 

# ****************************treasurer records***********************

class TreasurerRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreasurerRecords
        fields = '__all__'  # Include all fields from the model
class TreasurerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreasurerRecords
        fields = '__all__'  # Include all fields from the model

class TreasurerGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreasurerGoal
        fields = '__all__'

class TreasurerAmountCollectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreasurerAmountCollected
        fields = '__all__'

class TreasurerAmountUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreasurerAmountUsed
        fields = '__all__'

# ************************all members*************
class AllMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllMembers
        fields = '__all__'

# **************zone history************************
class ZoneHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneHistory
        fields = '__all__'

# ***************************** events************************
class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'  # Include all fields

# ********************88VENTURES serializers************************
class VenturesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ventures
        fields='__all__'




class VenturesMainPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenturesMainPlans
        fields = '__all__'


class VenturesMonthlyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenturesMonthlyAccount
        fields = '__all__'


class VenturesLeaderCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenturesLeaderCredentials
        fields = '__all__'

# ******************medical missionary******************
class MedicalMissionarySerializers(serializers.ModelSerializer):
    class Meta:
        model=MedicalMissionary
        fields='__all__'


class MedicalMissionaryEventDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model=MedicalMissionaryEventDetails
        fields='__all__'

class MedicalMissionaryHealthStatusOfMembersSerializers(serializers.ModelSerializer):
    class Meta:
        model=MedicalMissionaryHealthStatusOfMembers
        fields='__all__'


class CommunicationLeaderCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationLeaderCredentials
        fields = '__all__'


class CommunicationMainGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationMainGoals
        fields = '__all__'


class CommunicationAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationAssets
        fields = '__all__'


class educationLeaderSerializers(serializers.ModelSerializer):
    class Meta:
        model=educationLeader
        fields='__all__'

class educationLeaderAllMembersSerializers(serializers.ModelSerializer):
    class Meta:
        model=educationLeaderAllMembers
        fields='__all__'

class educationsLeadersGoalsSerializers(serializers.ModelSerializer):
    class Meta:
        model=educationsLeadersGoals
        fields='__all__'

class EducationLeaderPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model=EducationLeaderPosts
        fields='__all__'

class SpecialNeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialNeeds
        fields = '__all__'


class SpecialNeedsDisabledMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialNeedsDisabledMembers
        fields = '__all__'


class SpecialNeedsEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = specialNeedsEvents
        fields = '__all__'


class SpecialNeedsMainGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = specialNeedsMainGoals
        fields = '__all__'


class EducationEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model=EducationEvents
        fields = '__all__'

class EducationFeesDeficitMembersSerializers(serializers.ModelSerializer):
    class Meta:
        model=EducationFeesDeficitMembers
        fields='__all__'

class EducationOwenedAssetsSerialzer(serializers.ModelSerializer):
    class Meta:
        model=EducationOwenedAssets
        fields='__all__'        