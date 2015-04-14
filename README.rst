Introduction
============

This module allows you to use the r.js optimizer for RequireJS via your Django
template, with the added bonus of having django-compressor syntax and rollup.
Built files will only be generated and used when ``COMPRESS_ENABLED`` is
``True``, allowing for development without using compiled RequireJS files.

Features:
---------

-  Use the RequireJS optimizer via Django for using built optimized files,
   rather than relying exclusively on asynchronous module loading
-  All the features of django-compressor, e.g.:

   -  processing with Django template markup
   -  adding hashes to filenames
   -  rolling up multiple files into a single file
   -  including built content in a file or inline

Requirements
============

-  Django >= 1.5
-  django\_compressor >= 1.3
-  node js (or another environment capable of executing the r.js optimizer)

Installation
============

1. Add ``compressor_requirejs`` to installed apps
2. Setup ``django_compressor`` properties for working with django compressor
3. Setup ``compressor_requirejs``:

   -  Set ``COMPRESS_PRECOMPILERS`` of django compressor for using with
      standard markup in compress tags

.. code:: python

    COMPRESS_PRECOMPILERS = (
        ('text/requirejs', 'compressor_requirejs.filters.RequireJSPrecompiler'),
    )

Advanced configuration
======================

.. code:: python


        # COMPRESSOR_REQUIREJS config

        # Absolute path to r.js
        # default: path to the local copy in this compressor_requirejs package
        COMPRESSOR_REQUIREJS_R_JS = 'path/to/r.js'

        # Path to the global build configuration for RequireJS (the
        # "mainConfigFile" in r.js optimization configuration). The path should
        # be relative to STATIC_ROOT
        # default: no global configuration used
        COMPRESSOR_REQUIREJS_GLOBAL_CONFIG = 'path/to/global/requirejs/config.js'

        # Executable path for running the r.js optimization. It is preferred to
        # have 'node' on your PATH
        # default: node
        COMPRESSOR_REQUIREJS_ENVIORNMENT_EXECUTABLE = 'node'


Usage
=====

Prepare at least two js files, one build file and one module file:

build.js
--------

.. code:: javascript

    ({
        baseUrl: '.',
        name: 'main'
    })

main.js
-------

.. code:: javascript

    require([], function () {
        console.log('wow, its working');
    });

Put those files in static directory of your app. ``build.js`` pointing to
``main.js`` with ``name`` attribute, so launching build file compile ``main.js``
with other dependencies. Add your own configuration to build.js as needed. You
can use a global config file (see below) for common shared configuration.

Django template usage
---------------------

::

     {% compress js %}
          <script type="text/requirejs" src="{{ STATIC_URL }}js/app/main.js" data-build="{{ STATIC_URL }}js/app/build.js"></script>
     {% endcompress %}

If django-compressor's ``COMPRESS_ENABLED`` setting is set to ``False``, the
output will contain the raw contents of the ``src`` file ("main.js" in this
example).

If ``COMPRESS_ENABLED`` is set to ``True``, the output will be that of running
the r.js optimizer on the ``data-build`` file ("build.js" in this example).

This allows you to test using async-module loading when ``COMPRESS_ENABLED`` is
``False``, and the built output when ``COMPRESS_ENABLED`` is ``True``.

You will have to include the ``require.js`` file elsewhere.

::

    {% compress js %}
        <script src="{{ STATIC_URL }}mainapp/js/require.js"></script>
    {% endcompress %}


An advantage of having require.js separate is that you do not need to use the
``data-main`` attribute on the requirejs script tag and can instead customize
the order of files and the rollup of those files (e.g., including requirejs and
your built file inside the same ``compress`` block).


Global configuration for r.js builds
------------------------------------
Use the ``COMPRESSOR_REQUIREJS_GLOBAL_CONFIG`` option for specifying which
main configuration file to use when running the r.js optimizer. This is handy
for sharing configuration across multiple files (e.g., a shim configuration,
paths configuration, etc.) and staying DRY.

This will be passed to r.js as the mainConfigFile parameter (and will override
configuration specified in your build.js files). By default, no main config file
will be included.


Global js library mappings
--------------------------

You can use global path mappings for javascript files, for example if you have a
few apps in project and one handle main libraries simply add them to global
paths.

.. code:: python

    COMPRESSOR_REQUIREJS_REQUIRED_LIBS = {}

In django object simply type key value elements, where key is valid path mapping and value is path to js file.

**IMPORTANT**

- mapping name can be only solid string without dots eg.: ``mapping_for_path`` not ``mapping.for.path``
- path can be relative to current project and will be processed with defined static file finder


.. code:: python

    COMPRESSOR_REQUIREJS_REQUIRED_LIBS = {
        'jquery': 'mainapp/js/libs/jquery-2.1.0.min.js'
    }
