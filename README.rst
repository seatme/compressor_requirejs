

NEWS v1.3
=========

- install_requires added,
- support for django compressor 1.4 precompiler constructor

update v1.2
===========

- invalidate cache on compiling error,
- support for custom logging


Introduction
============

This module ables django compressor to compile requirejs files into one
or a few bigger files using r.js.

Features:
---------

-  compiling plenty of files into one file
-  making a few compiled files for splitting functionality
-  all features of django compressor i.e.:

   -  caching files,
   -  adding hashes,
   -  processing with django template markup,
   -  post compiling

-  tracing build files for modification (caching results)

Requirements
============

-  Django >= 1.5
-  django\_compressor >= 1.3
-  PyExecJs 1.0.4

-  node js

Installation
============

1. Add ``compressor_requirejs`` to installed apps
2. Setup ``django_compressor`` properties for working with django
   compressor
3. Setup ``compressor_requirejs``:

   -  Set ``COMPRESS_PRECOMPILERS`` of django compressor for using with
      standard markup in compress tags
   -  Set ``COMPRESSOR_REQUIREJS_TMP`` to a custom **existing**
      temporary directory path

.. code:: python

    COMPRESS_PRECOMPILERS = (
        ('text/requirejs', 'compressor_requirejs.compressor.r_precompiler.RequireJSPrecompiler'),
    )

    COMPRESSOR_REQUIREJS_TMP = django_project_path_join('tmp')

Advanced configuration
======================

.. code:: python


        #COMPRESSOR_REQUIREJS config

        #absolute path to r.js
        #default: path in resources of this package
        COMPRESSOR_REQUIREJS_R_JS = 'path/to/r.js'

        #absolute path to temporary directory
        COMPRESSOR_REQUIREJS_TMP = '/tmp'

        # Path to the global build configuration for RequireJS (the
        # "mainConfigFile" in r.js optimization configuration). The path should
        # be relative to STATIC_ROOT
        COMPRESSOR_REQUIREJS_GLOBAL_CONFIG = 'path/to/global/requirejs/config.js'

        # Executable path for running the r.js optimization. It is preferred to
        # have 'node' on your PATH
        # default: node
        COMPRESSOR_REQUIREJS_ENVIORNMENT_EXECUTABLE = 'node'


Using
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

Put those files in static directory of your app. ``build.js`` pointing
to ``main.js`` with ``name`` attribute, so launching build file compile
``main.js`` with other dependencies.

Django template configuration
-----------------------------

::

     {% compress js %}
          <script type="text/requirejs" src="{{ STATIC_URL }}mainapp/js/build.js"></script>
     {% endcompress %}

Of course you have to include ``require.js`` file, ex:

::

    {% compress js %}
        <script src="{{ STATIC_URL }}mainapp/js/require.js"></script>
    {% endcompress %}


Global js library mappings
--------------------------

You can use global path mappings for javascript files,
for example if you have a few apps in project and one handle main libraries simply add them to global paths.

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
