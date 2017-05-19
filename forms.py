from django import forms
from datetime import datetime
from django.core.validators import RegexValidator

from accounts.models import BaseTimeStamp
from locations.models import Location, LocationCustomEmail, LocationPhone, LocationAddress, LocationWebAddress, \
    LocationIMaddress, LocationEvent, location_phone_choices
from positions.models import Positions


class LocationForm(forms.ModelForm):
    location_name = forms.RegexField(regex=r'[a-zA-Z]',
                                     error_message=(
                                         "Only alphabets is allowed."))

    class Meta:
        model = Location
        exclude = ('priority', 'base_timestamp', 'location_email')

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['location_name'].widget.attrs.update({'class': 'form-control dm-form label-up-can'})
        self.fields['parent'].widget.attrs.update({'class': 'form-control  drop-menu-for-small'})
        self.fields['location_type'].widget.attrs.update({'class': 'form-control  drop-menu-for-small'})



    def save(self, user, commit=True):
        location = super(LocationForm, self).save(commit=False)
        if commit:
            time_stamp = BaseTimeStamp.objects.create(creation_timestamp=datetime.now(),
                                                      created_by=user)
            location.base_timestamp = time_stamp
            location.save()
        return location


class LocationCustomEmailForm(forms.ModelForm):
    class Meta:
        model = LocationCustomEmail
        exclude = ('location', 'base_timestamp', 'is_important')

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LocationCustomEmailForm, self).__init__(*args, **kwargs)
        self.fields['custom_email'].widget.attrs.update({'class': 'form-control dm-form label-up-can'})
        self.fields['email_type'].widget.attrs.update({'class': 'form-control  drop-menu-for-small'})

    def save(self, user, commit=True):
        location = super(LocationCustomEmailForm, self).save(commit=False)
        if commit:
            time_stamp = BaseTimeStamp.objects.create(creation_timestamp=datetime.now(),
                                                      created_by=user)
            location.base_timestamp = time_stamp
            location.save()
        return location


class LocationCustomPhoneForm(forms.ModelForm):
    EXTRA_CHOICES = [
        ('custom', 'custom'),

    ]

    class Meta:
        model = LocationPhone
        exclude = ('location', 'base_timestamp', 'is_important')

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LocationCustomPhoneForm, self).__init__(*args, **kwargs)
        choices = [(lp.id, unicode(lp)) for lp in location_phone_choices.objects.all()]
        choices.extend(self.EXTRA_CHOICES)
        self.fields['phone_type'].choices = choices
        self.fields['location_phone'].widget.attrs.update({'class': 'form-control dm-form label-up-can validate_ph'})
        self.fields['phone_type'].widget.attrs.update({'class': 'form-control phone_choices_validate  drop-menu-for-small'})

    def save(self, user, commit=True):
        location = super(LocationCustomPhoneForm, self).save(commit=False)
        if commit:
            time_stamp = BaseTimeStamp.objects.create(creation_timestamp=datetime.now(),
                                                      created_by=user)
            location.base_timestamp = time_stamp
            location.save()
        return location


class LocationAddressForm(forms.ModelForm):
    class Meta:
        model = LocationAddress
        exclude = ('location', 'base_timestamp')

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LocationAddressForm, self).__init__(*args, **kwargs)
        self.fields['town'].widget.attrs.update({'class': 'form-control dm-form label-up-can'})
        self.fields['post'].widget.attrs.update({'class': 'form-control dm-form label-up-can'})
        self.fields['address_type'].widget.attrs.update({'class': 'form-control  drop-menu-for-small'})

    def save(self, user, commit=True):
        location = super(LocationAddressForm, self).save(commit=False)
        if commit:
            time_stamp = BaseTimeStamp.objects.create(creation_timestamp=datetime.now(),
                                                      created_by=user)
            location.base_timestamp = time_stamp
            location.save()
        return location


class LocationWebAddressForm(forms.ModelForm):
    class Meta:
        model = LocationWebAddress
        exclude = ('location', 'base_timestamp')

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LocationWebAddressForm, self).__init__(*args, **kwargs)
        self.fields['web_address'].widget.attrs.update({'class': 'form-control dm-form label-up-can'})
        self.fields['web_address_type'].widget.attrs.update({'class': 'form-control  drop-menu-for-small'})

    def save(self, user, commit=True):
        location = super(LocationWebAddressForm, self).save(commit=False)
        if commit:
            time_stamp = BaseTimeStamp.objects.create(creation_timestamp=datetime.now(),
                                                      created_by=user)
            location.base_timestamp = time_stamp
            location.save()
        return location


class LocationIMaddressForm(forms.ModelForm):
    class Meta:
        model = LocationIMaddress
        exclude = ('location', 'base_timestamp')

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LocationIMaddressForm, self).__init__(*args, **kwargs)
        self.fields['im_address'].widget.attrs.update({'class': 'form-control dm-form label-up-can'})
        self.fields['im_address_type'].widget.attrs.update({'class': 'form-control  drop-menu-for-small'})

    def save(self, user, commit=True):
        location = super(LocationIMaddressForm, self).save(commit=False)
        if commit:
            time_stamp = BaseTimeStamp.objects.create(creation_timestamp=datetime.now(),
                                                      created_by=user)
            location.base_timestamp = time_stamp
            location.save()
        return location


class LocationEventForm(forms.ModelForm):
    class Meta:
        model = LocationEvent
        exclude = ('location', 'base_timestamp')

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(LocationEventForm, self).__init__(*args, **kwargs)
        self.fields['event'].widget.attrs.update({'class': 'form-control dm-form label-up-can'})
        self.fields['event_type'].widget.attrs.update({'class': 'form-control  drop-menu-for-small'})

    def save(self, user, commit=True):
        location = super(LocationEventForm, self).save(commit=False)
        if commit:
            time_stamp = BaseTimeStamp.objects.create(creation_timestamp=datetime.now(),
                                                      created_by=user)
            location.base_timestamp = time_stamp
            location.save()
        return location
