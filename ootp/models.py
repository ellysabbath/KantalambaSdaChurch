from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.conf import settings
import secrets
from tinymce import models as tinymce_models
import phonenumbers
from phonenumbers import phonenumberutil


# Helper function to format the mobile number
def format_mobile_number(mobile_number, region='TZ'):
    try:
        # Parse the mobile number with the specified region (defaulting to 'TZ' for Tanzania)
        phone_number = phonenumbers.parse(mobile_number, region)
        
        if not phonenumbers.is_valid_number(phone_number):
            raise ValueError("Invalid phone number")
        
        # Return the phone number in E.164 format (e.g., +255742575555 for Tanzania)
        return phonenumbers.format_number(phone_number, phonenumberutil.PhoneNumberFormat.E164)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValueError("Invalid phone number format")

# Custom user model to include email and mobile number
class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True, default='')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True) 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def clean_mobile_number(self):
        # Format the mobile number before saving it
        if self.mobile_number:
            self.mobile_number = format_mobile_number(self.mobile_number)

# OTP Token model to store OTP information
class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))  # Modify this later
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# **********************************user profile*************************
class UserRegistration(models.Model):
    CHURCH_CHOICES = [
        ('Ntyuka', 'Ntyuka'),
        ('Social', 'Social'),
        ('ngongona', 'Ngongona'),
        ('msangalalee', 'Msangalalee'),
        ('makulu','makulu'),
    ]
    
    BAPTISM_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    username = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    city = models.CharField(max_length=100)
    church = models.CharField(max_length=50, choices=CHURCH_CHOICES)
    baptism_status = models.CharField(max_length=3, choices=BAPTISM_CHOICES)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    password = models.CharField(max_length=100)
    terms_agreement = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

# ***********************profile image******************

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference the custom user model
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Image field
    
    def __str__(self):
        return self.user.username

# ***********************************Mhazini**************************
class TreasurerRecords(models.Model):
    COLLAGE_CHOICES=[
        ('choose collage of member', 'collage of member'),
        ('choose collage', 'Choose collage'),
        ('cive', 'CIVE'),
        ('humanities', 'HUMANITIES'),
        ('tiba', 'TIBA'),
        ('coed', 'COED'),
        ('social', 'SOCIAL'),
    ]
    CONTRIBUTION_TYPE=[
        ('choose contribution type', 'Choose contribution type'),
        ('miradi', 'Miradi'),
        ('vyeti', 'Vyeti'),
        ('ada', 'Ada'),
        ('michango mingine', 'Michango mingine'),
    ]
    username=models.CharField(max_length=100, null=False)
    firstname=models.CharField(max_length=100)
    contributionType=models.CharField(max_length=100, choices=CONTRIBUTION_TYPE)
    month=models.DateField()
    AmountPaid=models.IntegerField()
    collage=models.CharField(max_length=30, blank=False, default='',choices=COLLAGE_CHOICES)


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxtreasurer recordxxxxxxxxxxxxxxxxxxxxxxxxxx
class Treasurer(models.Model):

    name = models.CharField(max_length=255, default="", blank=False)
    start_date = models.DateField(default='', blank=False)
    description = tinymce_models.HTMLField(default="No description provided")  # Set default here
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TreasurerGoal(models.Model):
    STATUS=[
        ('choose status','choose status'),
        ('pending', 'pending'),
        ('on process','on process'),
        ('completed','completed'),
    ]
    title = models.CharField(max_length=255)
    description = tinymce_models.HTMLField()
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status=models.CharField(max_length=15, default='',blank=False, choices=STATUS)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title



class TreasurerAmountCollected(models.Model):
    
    
    amountCollected = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=255)
    dateOfCollection = models.DateField()

    def __str__(self):
        return f'Collected {self.amountCollected} from {self.source} on {self.dateOfCollection}'
    
class TreasurerAmountUsed(models.Model):
    
    
    amountUsed = models.DecimalField(max_digits=12, decimal_places=2)
    aimOfUse = models.CharField(max_length=255)
    dateOfUse = models.DateField()

    def __str__(self):
        return f'Used {self.amountUsed} for {self.aimOfUse} on {self.dateOfUse}'



# *****************************All members of the Zone***************************
class AllMembers(models.Model):
    COLLAGE_CHOICES=[
        ('choose collage', 'Choose collage'),
        ('cive', 'CIVE'),
        ('humanities', 'HUMANITIES'),
        ('tiba', 'TIBA'),
        ('coed', 'COED'),
        ('social', 'SOCIAL'),
    ]

    YEAR_OF_STUDY_CHOICE=[
        ('choose year of study', 'Choose year of study'),
        ('first year', 'First  year'),
        ('second year', 'Second year'),
        ('third year', 'Third year'),
        ('fourth year', 'Fourth year'),
        ('fifth year', 'Fifth year'),
        ('masters', 'Masters'),

   ]
    
    CHURCH_CHOICE=[
        ('select church', 'Select church'),
        ('udom central CIVE', 'UDOM CENTRAL CIVE'),
        ('udom east TIBA', 'UDOM EAST TIBA'),
        ('udom east COED', 'UDOM EAST COED'),
        ('udom west SOCIAL', 'UDOM WEST SOCIAL'),
        ('udom west HUMANITIES', 'UDOM WEST HUMANITIES'),

    ]

    username=models.CharField(unique=True, max_length=100, blank=False, null=False)
    firstname=models.CharField(max_length=100, blank=False)
    email=models.EmailField(max_length=100, blank=False, unique=True)
    MobNumber=models.CharField(max_length=15, default='', blank=False)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True) 
    collage=models.CharField(max_length=50, blank=False, default='', choices=COLLAGE_CHOICES)
    yearOfStudy=models.CharField(max_length=20, blank= False, default='', choices=YEAR_OF_STUDY_CHOICE)
    churchName=models.CharField(max_length=50, blank=False, default='', choices=CHURCH_CHOICE)




    def __str__(self):
        return self.username


    # **************************ZONE HISTORY****************************
class ZoneHistory(models.Model):
        YEAR_OF_STUDY_CHOICE=[
        ('choose year of study', 'Choose year of study'),
        ('first year', 'First  year'),
        ('second year', 'Second year'),
        ('third year', 'Third year'),
        ('fourth year', 'Fourth year'),
        ('fifth year', 'Fifth year'),
        ('masters', 'Masters'),

   ]
        
        CERTIFICATE_CHOICE=[
            ('choose status', 'Choose status'),
            ('completed', 'Completed'),
            ('pending', 'Pending'),
            ('on process', 'On process'),

        ]

        firstname=models.CharField(max_length=100, blank=False, default='')
        username=models.CharField(max_length=50, blank=False, default='')
        position=models.CharField(max_length=50, blank=False, default='')
        image = models.ImageField(upload_to='user_images/%Y/%m/%d/', blank=True, null=True) 
        yearOfStudy=models.CharField(blank=False, max_length=100, default='',choices=YEAR_OF_STUDY_CHOICE )
        certificateStatus=models.CharField(blank=False, default='',max_length=20, choices=CERTIFICATE_CHOICE)

        def __str__(self):
            return self.username
        


# ***************************events done**********************************
class Events(models.Model):
    date=models.DateField(blank=False, default='', max_length=20)
    images=models.ImageField(upload_to='user_images/%Y/%m/%d/', blank=True, null=True)
    nameOfAnEvent=models.CharField(max_length=50, blank=False, default='')
    costUsed=models.CharField(max_length=30, blank=False, default='')

# ********************************Ventures*********************************
class Ventures(models.Model):
    name = models.CharField(max_length=255)
    established_date = models.DateField()
    description = tinymce_models.HTMLField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class VenturesMainPlans(models.Model):
    PLAN_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise')
    ]

    name = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = tinymce_models.HTMLField()

    def __str__(self):
        return f'{self.name} ({self.plan_type})'


class VenturesMonthlyAccount(models.Model):
    name = models.CharField(max_length=255, blank=False, default='')
    account_balance = models.DecimalField(max_digits=12, decimal_places=2)
    last_payment_date = models.DateField()
    is_active = models.BooleanField(default=True)
    monthlyGain = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthlyCost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthlyProfit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'Account as of {self.last_payment_date}'


class VenturesLeaderCredentials(models.Model):
    username=models.CharField(max_length=100, blank=False,default='')
    leader_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    leader_email = models.EmailField()
    leaderMobile = models.CharField(max_length=15, blank=False, default='')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.leader_name} - {self.role}'

    
# *****************************************medical missionary********************

class MedicalMissionary(models.Model):
    goal_name = models.CharField(max_length=255)
    mission_date = models.DateField()  # <-- Add this field
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=False)  # <-- Changed from DateField to DecimalField
    location = models.CharField(max_length=255)
    description = tinymce_models.HTMLField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.goal_name

class MedicalMissionaryEventDetails(models.Model):
    # Removed ForeignKey to MedicalMissionary
    missionary_name = models.CharField(max_length=255)  # optional reference field

    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_location = models.CharField(max_length=255)
    event_description = tinymce_models.HTMLField()
    event_Image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    output_raised = models.DecimalField(max_digits=12, decimal_places=8, default=0)

    def __str__(self):
        return f'{self.event_name} on {self.event_date}'


class MedicalMissionaryHealthStatusOfMembers(models.Model):
    COLLAGE_CHOICES = [
        ('cive', 'CIVE'),
        ('humanities', 'HUMANITIES'),
        ('social', 'SOCIAL'),
        ('coed', 'COED'),
        ('cnms', 'CNMS'),
        ('coese', 'COESE'),
        ('cobe', 'COBE'),
    ]

    # Removed ForeignKey to MedicalMissionary
    missionary_name = models.CharField(max_length=255)  # optional reference field

    member_name = models.CharField(max_length=255)
    health_condition = tinymce_models.HTMLField()
    treatment_administered = models.TextField()
    username = models.CharField(max_length=50, blank=False, default='')
    event_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    member_collage = models.CharField(max_length=50, choices=COLLAGE_CHOICES, default='', blank=False)
    follow_up_date = models.DateField()

    def __str__(self):
        return f'{self.member_name} - {self.health_condition}'

# *****************************************communication**************************************
class CommunicationLeaderCredentials(models.Model):
    ROLE=[
        ('choose role','role'),
        ('staff','STAFF'),
        ('ministry leader','MINISTRY LEADER'),
    ]
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255,choices=ROLE)
    email = models.EmailField()
    mobile = models.CharField(max_length=15, blank=False, default='')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    description = tinymce_models.HTMLField(null=False, default="No description")
    established_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.role}'



class CommunicationMainGoals(models.Model):
    goal_title = models.CharField(max_length=255)
    goal_description = tinymce_models.HTMLField()
    achieved = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.goal_title


class CommunicationAssets(models.Model):
    asset_name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField()

    def __str__(self):
        return f'{self.asset_name} ({self.asset_type})'
    
# ************************************special needs********************************
class SpecialNeeds(models.Model):
    username=models.CharField(max_length=50, blank=False,default='')
    fullname=models.CharField(max_length=100, blank=False, default='')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bodyAbility=models.CharField(max_length=100)


class SpecialNeedsDisabledMembers(models.Model):
    COLLAGE_CHOICES = [
        ('select collage', 'Select collage'),
        ('cive', 'CIVE'),
        ('social','SOCIAL'),
        ('tiba','TIBA'),
        ('coed','COED'),
        ('humanity','HUMANITIES'),
    ]

    BODY_ABILITY_CHOICES = [
        ('normal', 'Normal'),
        ('partially disabled', 'Partially Disabled'),
        ('fully disabled', 'Fully Disabled'),
    ]

    username = models.CharField(max_length=100, blank=False, default='')
    first_name = models.CharField(max_length=100, blank=False, default='')
    collage = models.CharField(max_length=100, choices=COLLAGE_CHOICES, blank=False, default='select collage')
    mobile_number = models.CharField(max_length=15, blank=False, default='')
    email = models.EmailField(max_length=100, blank=False, default='')
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    problem = models.CharField(max_length=50, blank=False, default='')
    body_ability_status = models.CharField(max_length=50, choices=BODY_ABILITY_CHOICES, blank=False, default='normal')

    def __str__(self):
        return f"{self.username} - {self.first_name}"




class specialNeedsEvents(models.Model):
    eventName=models.CharField(max_length=100, blank=False, default='special needs event')
    date=models.DateField()
    location=models.CharField(max_length=50)
    picture=models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=8, default=0)


class specialNeedsMainGoals(models.Model):
    goal_name=models.CharField(max_length=100, default='', null=False)
    location=models.CharField(max_length=50)
    date=models.DateField()
    description=tinymce_models.HTMLField()


# **************************************education leader*****************************************
class educationLeader(models.Model):
    YEAR_OF_STUDY_CHOICE=[
        ('choose year of study', 'Choose year of study'),
        ('first year', 'First  year'),
        ('second year', 'Second year'),
        ('third year', 'Third year'),
        ('fourth year', 'Fourth year'),
        ('fifth year', 'Fifth year'),
        ('masters', 'Masters'),

   ]
    COLLAGE_CHOICES = [
        ('cive', 'CIVE'),
        ('humanities', 'HUMANITIES'),
        ('social', 'SOCIAL'),
        ('coed', 'COED'),
        ('cnms', 'CNMS'),
        ('coese', 'COESE'),
        ('cobe', 'COBE'),
    ]
    username=models.CharField(max_length=100, default='', null=False)
    fullname=models.CharField(max_length=100, default='', null=False)
    email=models.EmailField(max_length=100, default='', null=False)
    mobileNumber=models.IntegerField(null=False, default='+255')
    image=models.ImageField(upload_to='profile_images/', blank=True, null=True)
    dateJoined=models.DateField()
    collage=models.CharField(max_length=100, default='', null=False,choices=COLLAGE_CHOICES)
    yearOfStudy=models.CharField(max_length=100, default='', null=False,choices=YEAR_OF_STUDY_CHOICE)
    program=models.CharField(max_length=100, default='', null=False)


class educationLeaderAllMembers(models.Model):
    YEAR_OF_STUDY_CHOICE=[
        ('choose year of study', 'Choose year of study'),
        ('first year', 'First  year'),
        ('second year', 'Second year'),
        ('third year', 'Third year'),
        ('fourth year', 'Fourth year'),
        ('fifth year', 'Fifth year'),
        ('masters', 'Masters'),

   ]
    COLLAGE_CHOICES = [
        ('cive', 'CIVE'),
        ('humanities', 'HUMANITIES'),
        ('social', 'SOCIAL'),
        ('coed', 'COED'),
        ('cnms', 'CNMS'),
        ('coese', 'COESE'),
        ('cobe', 'COBE'),
    ]
    username=models.CharField(max_length=100, default='', null=False)
    fullname=models.CharField(max_length=100, default='', null=False)
    email=models.EmailField(max_length=100, default='', null=False)
    mobileNumber=models.IntegerField(null=False, default='+255')
    image=models.ImageField(upload_to='profile_images/', blank=True, null=True)
    dateJoined=models.DateField()
    collage=models.CharField(max_length=100, default='', null=False,choices=COLLAGE_CHOICES)
    yearOfStudy=models.CharField(max_length=100, default='', null=False,choices=YEAR_OF_STUDY_CHOICE)
    program=models.CharField(max_length=100, default='', null=False)

class educationsLeadersGoals(models.Model):
    STATUS=[
        ('completed','completed'),
        ('pending','pending'),
        ('on process','on process')
    ]
    goalName=models.CharField(max_length=100, default='', null=False)
    cost = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    expression=tinymce_models.HTMLField()
    status=models.CharField(max_length=20,default='completed', null=False,choices=STATUS)


# **************education LEADER posts*****************
class EducationLeaderPosts(models.Model):
    title=models.CharField(max_length=500)
    text=tinymce_models.HTMLField()

    def __str__(self):
        return self.title
    


class  EducationEvents(models.Model):
    event_name=models.CharField(max_length=100, default='', blank=False)
    date_of_event=models.DateField()
    cost_used=models.CharField(max_length=100, default='', blank=False)



    def __str__(self):
        return self.event_name
    

class EducationFeesDeficitMembers(models.Model):
        COLLAGE_CHOICE=[
            ('select collage', 'select collage'),
            ('cive', 'CIVE'),
            ('social','SOCIAL'),
            ('tiba','TIBA'),
            ('coed','COED'),
            ('humanity','HUMANITIES'),
        ]

        FEES_STATUS_CHOICE=[
            ('choose status', "choose status"),
            ('pending', 'pending'),
            ('on process', 'on process'),
            ('completed', 'completed'),
        ]
        firstName=models.CharField(max_length=100, default='', blank=False)
        collage=models.CharField(max_length=100, default='', blank=False, choices=COLLAGE_CHOICE)
        feesStatus=models.CharField(max_length=100, default='', blank=False, choices=FEES_STATUS_CHOICE)

        def __str__(self):
            return self.firstName
        

class EducationOwenedAssets(models.Model):
        AssetName=models.CharField(max_length=100, default='', blank=False)
        value=models.IntegerField(blank=False, default='00')

        def __str__(self):
            return self.AssetName
