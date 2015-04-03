#!/usr/bin/env python
import os

from compressor.filters.base import FilterBase
from django.contrib.staticfiles import finders

from compressor_requirejs.compiler import RequireJSCompiler
from compressor_requirejs.config import settings


class RequireJSPrecompiler(FilterBase):

    def __init__(self, content, attrs=None, filter_type=None, charset=None, filename=None):
        self.content = content
        self.attrs = attrs
        self.filter_type = filter_type
        self.filename = filename
        self.charset = charset
        self.requireJSCompiler = RequireJSCompiler()

    def input(self, **kwargs):
        build_filename = self.get_fullpath(kwargs['basename'], resolve_path=True)

        global_config = getattr(settings, 'COMPRESSOR_REQUIREJS_GLOBAL_CONFIG', None)
        config_path = self.get_fullpath(global_config)

        paths = self.get_paths_from_required_libs()

        return self.requireJSCompiler.requirejs(
            build_filename, config_path=config_path, paths=paths)

    def get_fullpath(self, path, resolve_path=True):
        if os.path.isabs(path):
            return path
        if not resolve_path:
            return path
        files = finders.find(path, all=True)
        if isinstance(files, list):
            if len(files) > 0:
                return files[0]
            else:
                return path
        elif files is not None:
            return files
        else:
            return path

    def get_paths_from_required_libs(self):
        paths = []
        if hasattr(settings, 'COMPRESSOR_REQUIREJS_REQUIRED_LIBS'):
            for arg in settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS.keys():
                path = self.get_fullpath(settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS[arg])
                if path.endswith('.js'):
                    path = path[:-3]
                paths.append('paths.%s=%s' % (arg, path))
        return paths
