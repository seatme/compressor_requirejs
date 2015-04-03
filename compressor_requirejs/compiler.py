import codecs
import subprocess
import tempfile

from django.core.exceptions import ImproperlyConfigured

from .config import settings


APP_NAME = 'compressor_requirejs'


class RequireJSCompilerException(Exception):
    pass


class RequireJSCompiler(object):
    """
    A compiler that runs the r.js optimizer on a build config for a single file.
    """
    def __init__(self):
        self.rjs = getattr(settings, 'COMPRESSOR_REQUIREJS_R_JS', None)
        if not self.rjs:
            raise ImproperlyConfigured('COMPRESSOR_REQUIREJS_R_JS not set')

    def requirejs(self, build_filename, config_path=None, paths=None,
                  charset='utf-8'):
        """
        Returns a string of the compiled JS for the given build file.

        Args:
            - build_filename - The full file path of the build file to use.
            - config_path - (optional) The full file path of the main
                config file to use for this build (see requireJS mainConfigFile)
            - paths - (optional) List of command line path arguments to pass to
                the r.js optimizer
            - charset - The charset to use for reading the output JS
        """
        outfile = tempfile.NamedTemporaryFile()

        process_args = [
            settings.COMPRESSOR_REQUIREJS_ENVIORNMENT_EXECUTABLE,
            self.rjs,
            '-o',
            build_filename,
            'out=%s' % outfile.name
        ]

        if paths is not None:
            process_args += paths

        if config_path:
            process_args.append('mainConfigFile=%s' % config_path)

        try:
            output = subprocess.check_output(process_args)
        except Exception as e:
            raise RequireJSCompilerException(e)

        if 'Error' in output:
            raise RequireJSCompilerException(output)

        with codecs.open(outfile.name, 'r', charset) as f:
            compiled_js = f.read()

        outfile.close()

        return compiled_js
