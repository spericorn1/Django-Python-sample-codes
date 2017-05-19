import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from profiling import profile, Profiler
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
from accounts.models import User
from permissions.models import Permissions, PermissionModule, PermissionMode
from positions.forms import PositionForm
from positions.mixins import PositionMixin
from positions.models import Positions


class PositionListingView(ListView,PositionMixin):
    """
    Handles position view and contexts
    """
    template_name = 'business-position.html'
    model = Positions

    @csrf_exempt
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PositionListingView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        
        :param kwargs: nil
        :return: 
        """
        context = super(PositionListingView, self).get_context_data(**kwargs)
        context['position_form'] = PositionForm()
        context['all_positions'] = Positions.objects.all().select_related('parent')
        context['all_permissions'] = Permissions.objects.all()
        context['permission_modes'] = PermissionMode.objects.all()
        return context


class CreatePositions(ListView,PositionMixin):
    """
    Handles all actions related to model Position
    """
    template_name = 'business-position.html'
    model = User

    @csrf_exempt
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePositions, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreatePositions, self).get_context_data(**kwargs)
        context['position_form'] = PositionForm()
        return context

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.is_ajax():
            response_data = {}
            if request.POST.get('type') == 'update-form':
                response_data['create_position'] = render_to_string('ajax/create-position.html',{'position_form':PositionForm()})
                response_data['create_edit_position'] = render_to_string('ajax/create-edit-position.html',{'position_form':PositionForm()})

            elif request.POST.get('type') == 'edit-position':
                position_instance = self.get_position_by_id(request.POST.get('postn_id'))
                response_data['status'] = True
                response_data['create_edit_position'] = render_to_string('ajax/create-edit-position.html',
                                                                         {'position_form': PositionForm(instance=position_instance),'form_id':position_instance})
            else:
                if request.POST.get('is_instance'):
                    form = PositionForm(request.POST,instance=self.get_position_by_id(request.POST.get('is_instance')))
                else:
                    form = PositionForm(request.POST)
                if form.is_valid():
                    position_instance = form.save(request.user)
                    response_data['status'] = True
                    response_data['position_table'] = render_to_string('ajax/position_table.html',
                                                                                 {'all_positions': Positions.objects.all().select_related('parent')})
                    if request.POST.get('type') == 'create-edit-form':
                        response_data['create_edit_position'] = render_to_string('ajax/create-edit-position.html',
                                                                                 {'position_form': PositionForm(instance=position_instance),'form_id':position_instance})

                else:
                    response_data['status'] = False
                    response_data['errors'] = form.errors
            return HttpResponse(json.dumps(response_data), content_type="application/json")
