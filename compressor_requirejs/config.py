from os.path import dirname, abspath, join

from django.conf import settings as django_settings


THIS_PATH = dirname(abspath(__file__))


class LazySettings(object):
    @property
    def COMPRESSOR_REQUIREJS_R_JS(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_R_JS", join(THIS_PATH, join('resources', 'r.js')))

    @property
    def COMPRESSOR_REQUIREJS_GLOBAL_CONFIG(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_GLOBAL_CONFIG", None)

    @property
    def COMPRESSOR_REQUIREJS_ENVIORNMENT_EXECUTABLE(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_ENVIORNMENT_EXECUTABLE", 'node')

    @property
    def COMPRESSOR_REQUIREJS_REQUIRED_LIBS(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_REQUIRED_LIBS", {})


settings = LazySettings()
