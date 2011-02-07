from django import forms
from django.conf import settings
from django.forms.widgets import flatatt
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.utils.simplejson import *
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import ugettext as _

DEFAULT_CONFIG = {
    'default': {
        'toolbar': [
            [ 'Source','-','Bold', 'Italic', 'Underline',
             '-','NumberedList','BulletedList',
              '-', 'Link', 'Unlink','Image',
              '-',  'Scayt',
            ],
        ],
        'width': 800,
        'height': 88,
    },
    'introtext': {
        'toolbar': [
            [ 'Source','-','Bold', 'Italic', 'Underline',
             '-','NumberedList','BulletedList',
              '-', 'Link', 'Unlink','Image',
              '-',  'Scayt',
            ],
        ],
        'width': 800,
        'height': 88,
    },
    'content': {
        'toolbar': [
            [ 'Source','-','Bold', 'Italic', 'Underline','Strike','Blockquote'],
            ['NumberedList','BulletedList','Blockquote'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            ['Font','FontSize','TextColor','BGColor'],
            ['Scayt',],
            '/',
            ['Link', 'Unlink','Image','Table'],
            ['HorizontalRule','SpecialChar'],
        ],
        'width': 800,
        'height': 400,
    },
}

def get_lang_title(value):
    for code,title in settings.LANGUAGES:
        if value==code:
            return _(title)

class CKEditorWidget(forms.Textarea):
    def __init__(self, config_name='default', attrs=None, mce_attrs=None):
        super(CKEditorWidget, self).__init__(attrs)
        self.config_name=config_name

    class Media:
        try:
            js = (
                settings.CKEDITOR_MEDIA_PREFIX + 'ckeditor/ckeditor.js',
            )
        except AttributeError:
            raise ImproperlyConfigured("django-ckeditor requires CKEDITOR_MEDIA_PREFIX setting. This setting specifies a URL prefix to the ckeditor JS and CSS media (not uploaded media). Make sure to use a trailing slash: CKEDITOR_MEDIA_PREFIX = '/media/ckeditor/'")

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)

        self_config = getattr(DEFAULT_CONFIG, config_name, None)
        configs = getattr(settings, 'CKEDITOR_CONFIGS', None)
        if configs != None:
            if isinstance(configs, dict):
                # Make sure the config_name exists.
                if configs.has_key(self.config_name):
                    config = configs[self.config_name].copy()
                    # Make sure the configuration is a dictionary.
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('CKEDITOR_CONFIGS["%s"] setting must be a dictionary type.' % self.config_name)
                    self_config.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' found in your CKEDITOR_CONFIGS setting." % self.config_name)
            else:
                raise ImproperlyConfigured('CKEDITOR_CONFIGS setting must be a dictionary type.')

        ck_json = JSONEncoder().encode(self_config)
        return mark_safe(u'<textarea%s>%s</textarea> <script type="text/javascript" charset="utf-8"> \
            CKEDITOR.replace( "%s", %s); \
        </script>' % (flatatt(final_attrs), escape(value),'id_'+name,ck_json)
        )
