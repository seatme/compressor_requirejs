#!/usr/bin/env python
import codecs

from compressor.filters.base import FilterBase
from compressor.js import JsCompressor
from django.conf import settings as django_settings

from compressor_requirejs.compiler import RequireJSCompiler
from compressor_requirejs.config import settings


class RequireJSPrecompiler(FilterBase):

    def __init__(self, content, attrs=None, filter_type=None, charset=None, filename=None):
        self.content = content
        self.attrs = attrs
        self.filter_type = filter_type
        self.filename = filename
        self.charset = charset

        # The main module to load, which should correspond to the "name" in the
        # build file
        self.module_name = self.attrs.get('data-name')

        # The RequireJS compiler for building optimized JS
        self.requireJSCompiler = RequireJSCompiler()

        # Use Django-Compressor's builtin Compressor tools to get the file
        # paths and contents of needed files
        self.compressor = JsCompressor()

    def input(self, **kwargs):
        if getattr(django_settings, 'COMPRESS_ENABLED', False):
            # Only use built files (from the RequireJS optimizer) when compress
            # is enabled
            build_filename = self.get_filepath(kwargs['basename'])

            global_config = getattr(settings, 'COMPRESSOR_REQUIREJS_GLOBAL_CONFIG', None)
            config_path = self.get_filepath(global_config)

            paths = self.get_paths_from_required_libs()

            return self.requireJSCompiler.requirejs(
                build_filename, config_path=config_path, paths=paths,
                charset=self.charset)
        else:
            # Return the content of the main file, with no RequireJS
            # optimization (i.e., just use async-loading for all modules)
            module_filepath = self.get_filepath(self.module_name)
            with codecs.open(module_filepath, 'r', self.charset) as f:
                return f.read()

    def get_paths_from_required_libs(self):
        paths = []
        if hasattr(settings, 'COMPRESSOR_REQUIREJS_REQUIRED_LIBS'):
            for arg in settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS.keys():
                path = self.get_filepath(settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS[arg])
                if path.endswith('.js'):
                    path = path[:-3]
                paths.append('paths.%s=%s' % (arg, path))
        return paths

    def get_filepath(self, static_path):
        """
        Get the absolute file-path of the the file given its
        STATIC_ROOT-relative path.

        Returns the file path on the file system.
        """
        basename = self.compressor.get_basename(static_path)
        return self.compressor.get_filename(basename)
