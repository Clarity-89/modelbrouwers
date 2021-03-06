from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from brouwers.builds.models import Build
from brouwers.utils.admin.decorators import link_list
from .models import Brand, Scale, ModelKit


def merge_duplicates(modeladmin, request, queryset):
    """
    Marks the queryset objects as duplicates.

    This needs an intermediate page to select which object it's a duplicate of.
    """
    if not request.user.is_superuser:
        raise PermissionDenied

    opts = modeladmin.model._meta

    # create the form
    target_queryset = modeladmin.model.objects.exclude(pk__in=queryset.values_list('pk', flat=True))
    DuplicateForm = type(b'DuplicateForm', (forms.Form,), {
        'target': forms.ModelChoiceField(queryset=target_queryset, empty_label=None, label=_('merge into'))
    })

    if request.POST.get('post'):
        form = DuplicateForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data['target']
            for item in queryset:
                item.modelkit_set.update(**{opts.model_name: target})

            queryset.delete()
            # Return None to display the change list page again.
            return None

    if len(queryset) == 1:
        objects_name = force_text(opts.verbose_name)
    else:
        objects_name = force_text(opts.verbose_name_plural)

    context = {
        'title': _('Merge duplicates'),
        'queryset': queryset,
        'form': DuplicateForm(),
        'objects_name': objects_name,
        'opts': opts,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    }
    return TemplateResponse(request, 'admin/kits/mark_duplicate.html', context)
merge_duplicates.short_description = _('Merge selected %(verbose_name_plural)s')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'is_active', 'slug')
    list_filter = ('is_active',)
    search_fields = ('=id', 'name')
    actions = [merge_duplicates]


@admin.register(Scale)
class ScaleAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('scale',)
    actions = [merge_duplicates]


@admin.register(ModelKit)
class ModelKitAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'scale', 'get_builds', 'get_box_image_url')
    list_filter = ('is_reviewed', 'brand', 'scale')
    search_fields = ('name', 'kit_number')
    raw_id_fields = ('submitter',)
    filter_horizontal = ('duplicates',)

    def get_queryset(self, request=None):
        prefetch = Prefetch('builds', queryset=Build.objects.select_related('user'))
        return super(ModelKitAdmin, self).get_queryset(request=request).prefetch_related(prefetch)

    @link_list(short_description=_('builds'))
    def get_builds(self, obj):
        return obj.builds.all()

    def get_box_image_url(self, obj):
        if obj.box_image:
            return '<a href="{0}" target="_blank">{1}</a>'.format(obj.box_image.url, _('view image'))
        return ''
    get_box_image_url.allow_tags = True
    get_box_image_url.short_description = _('boxart')
