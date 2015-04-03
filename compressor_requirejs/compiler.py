import codecs
import subprocess
import os

from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles import finders

from .config import settings


APP_NAME = 'compressor_requirejs'


class CompressorRequireJSException(Exception):
    pass


class RequireJSCompiler(object):
    def __init__(self):
        self.r = getattr(settings, 'COMPRESSOR_REQUIREJS_R_JS', None)
        if not self.r:
            raise ImproperlyConfigured('COMPRESSOR_REQUIREJS_R_JS not set')
        self.tmp = getattr(settings, 'COMPRESSOR_REQUIREJS_TMP', None)
        if not self.tmp:
            raise ImproperlyConfigured('COMPRESSOR_REQUIREJS_TMP not set')

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

    def required_libs(self):
        paths = []
        if hasattr(settings, 'COMPRESSOR_REQUIREJS_REQUIRED_LIBS'):
            for arg in settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS.keys():
                path = self.get_fullpath(settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS[arg])
                if path.endswith('.js'):
                    path = path[:-3]
                paths.append('paths.%s=%s' % (arg, path))
        return paths

    def _tmp_file_gen(self, filename, postfix):
        return os.path.join(self.tmp, filename.replace('\\', '_').replace('/', '_').replace('.', '_') + postfix)

    def requirejs(self, filename, resolve_path=True, include_tags=True):
        libs = self.required_libs()
        global_config = getattr(settings, 'COMPRESSOR_REQUIREJS_GLOBAL_CONFIG', None)
        outfile = self._tmp_file_gen(filename, '_build.js')
        build_filename = self.get_fullpath(filename, resolve_path)
        process_args = [settings.COMPRESSOR_REQUIREJS_ENVIORNMENT_EXECUTABLE,
                        self.r,
                        '-o', build_filename,
                        'out=' + outfile] + libs
        if global_config:
            process_args.append('mainConfigFile=' + self.get_fullpath(global_config))

        try:
            output = subprocess.check_output(process_args)
        except Exception as e:
            raise CompressorRequireJSException(e)

        if 'Error' in output:
            raise CompressorRequireJSException(output)

        f = codecs.open(outfile, 'r', 'utf-8')
        ret = '<script>%s</script>' % f.read() if include_tags else f.read()
        f.close()
        return ret
