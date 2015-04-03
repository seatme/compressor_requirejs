#!/usr/bin/env python
from compressor.filters.base import FilterBase

from compressor_requirejs.compiler import RequireJSCompiler


class RequireJSPrecompiler(FilterBase):

    def __init__(self, content, attrs=None, filter_type=None, charset=None, filename=None):
        self.content = content
        self.attrs = attrs
        self.filter_type = filter_type
        self.filename = filename
        self.charset = charset
        self.requireJSCompiler = RequireJSCompiler()

    def input(self, **kwargs):
        return self.requireJSCompiler.requirejs(kwargs['basename'], True, False)
