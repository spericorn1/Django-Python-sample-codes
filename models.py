from __future__ import unicode_literals
from django.core import validators
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

# ####################### USER ###################################

ADDRESS_TYPES = (
    ('Town', 'Town'),
    ('Suburb', 'Suburb'),
)



class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    VARIFICATION_CHOICES = (
        ('Email', 'Email'),
        ('Mobile', 'Mobile'),
    )
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    username = models.CharField(
        _('username'), null=True, blank=True,
        max_length=30,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    preferred_name = models.CharField(_('preferred name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True, )
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("self", null=True, blank=True, related_name='created_user')
    modified_by = models.ForeignKey("self", null=True, blank=True, related_name='modified_user')
    verification = models.CharField(_('verification'), max_length=150, choices=VARIFICATION_CHOICES, default='1')
    gender = models.CharField(_('gender'), max_length=100, choices=GENDER_CHOICES, default='1')
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True, )
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(245, 62)],
                                           format='JPEG',
                                           options={'quality': 60})
    active_position = models.ForeignKey('positions.Positions', related_name='current_user_position',null=True,blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_varified = models.BooleanField(
        _('varified'),
        default=False,
        help_text=_(
            'Designates whether this user has verified email/mobile. '

        ),
    )
    date_of_birth = models.DateField(_('date of birth'), default=timezone.now)
    start_date = models.DateTimeField(_('start date'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_position(self):
        """
        :return:high priority position of user
        """
        all_positions = self.user_current_position.select_related('position').order_by('position__priority').first()
        if all_positions:
            return all_positions.position
        else:
            return None

    def has_permission(self,permission):
        arr = permission.split('.')
        module = arr[0]
        permi = arr[1]

        return permission


class BaseTimeStamp(models.Model):
    """
    base model for timestamp and creation...
    """
    creation_timestamp = models.DateTimeField(_('Creation timestamp'), null=True, blank=True)
    modified_timestamp = models.DateTimeField(_('Modified timestamp'), null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='module_created_user')
    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='module_modified_user')


class UserOtherEmails(models.Model):
    user = models.ForeignKey(User, related_name='user_other_email')
    email = models.EmailField(_('email address'), unique=True, )
    base_timestamp = models.ForeignKey(BaseTimeStamp, related_name='user_other_email_timestamp')

    def __str__(self):
        return self.email


class UserContact(models.Model):
    CONTACT_TYPE = (
        ('mine', 'mine'),
        ('friend', 'friend'),
    )
    user = models.ForeignKey(User, related_name='user_contact')
    contact_type = models.CharField(_('Type'), max_length=150, choices=CONTACT_TYPE)
    is_primary = models.BooleanField(
        _('is primary'),
        default=False,

    )
    base_timestamp = models.ForeignKey(BaseTimeStamp, related_name='user_contact_timestamp')

    def __str__(self):
        return self.user.username


class UserEmergencyContact(models.Model):
    user = models.ForeignKey(User, related_name='user_emergency_contact')
    name = models.CharField(_('Name'), max_length=250)
    number = models.CharField(_('Number'), max_length=250)
    is_primary = models.BooleanField(
        _('is primary'),
        default=False,

    )
    base_timestamp = models.ForeignKey(BaseTimeStamp, related_name='user_emergency_contact_timestamp')

    def __str__(self):
        return self.user.username




class UserPostalAddress(models.Model):
    user = models.ForeignKey(User, related_name='user_postal_address')
    address_type = models.CharField(_('Town/Suburb'), max_length=150, choices=ADDRESS_TYPES)
    address = models.CharField(_('Address'), max_length=250)
    address_sub_line = models.CharField(_('Address Line 2'), max_length=250)
    base_timestamp = models.ForeignKey(BaseTimeStamp, related_name='user_postal_address_timestamp')

    def __str__(self):
        return self.user.username


class UserResidentialAddress(models.Model):
    user = models.ForeignKey(User, related_name='user_residentail_address')
    address_type = models.CharField(_('Town/Suburb'), max_length=150, choices=ADDRESS_TYPES)
    address = models.CharField(_('Address'), max_length=250)
    address_sub_line = models.CharField(_('Address Line 2'), max_length=250)
    base_timestamp = models.ForeignKey(BaseTimeStamp, related_name='user_res_address_timestamp')

    def __str__(self):
        return self.user.username


class AccountTypes(models.Model):
    account_type = models.CharField(_('Type'), max_length=200)
    base_timestamp = models.ForeignKey(BaseTimeStamp, related_name='account_type_timestamp')


class UserPayments(models.Model):
    user = models.ForeignKey(User, related_name='user_payments')
    account_type = models.ForeignKey(AccountTypes, related_name='user_account_type')
    bsb = models.CharField(_('BSB'), max_length=255, null=True, blank=True)
    account = models.CharField(_('Account'), max_length=9, null=True, blank=True)
    base_timestamp = models.ForeignKey(BaseTimeStamp, related_name='user_payments_timestamp')


    def __str__(self):
        return self.user.username



