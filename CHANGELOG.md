Changelog
=========

### 2.0
Features:
* Use COMPRESSOR_REQUIREJS_GLOBAL_CONFIG option for specifying a global
  configuration (no longer COMPRESSOR_REQUIREJS_GLOBAL_PRECONFIG)
* Support for using raw "main" JS files (ignoring the build file) when
  `COMPRESS_ENABLED` is `False`.

Backward incompatible changes:
* Change path to the Django Compressor precompiler. Now located at
  'compressor_requirejs.filters.RequireJSPrecompiler'
* Remove logic for including Django template language tags in your JS files.
  This simplifies configuration and eliminates the PyExecJs dependency.
* Remove the COMPRESSOR_REQUIREJS_TMP setting and the associated internal temp
  file logic
* Remove cache configuration (COMPRESSOR_REQUIREJS_CACHE_BACKEND,
  COMPRESSOR_REQUIREJS_CACHE_TIMEOUT)
* Remove custom cache code and logic
* Remove custom logging configuration

### 1.3
* install_requires command added
* support for django-compressor 1.4 precompiler constructor

### 1.2
* invalidate cache on compiling error
* support for custom logging

### 1.1.1
* fixed setup file

### 1.1
* required libs support

### 1.0
* initial version
