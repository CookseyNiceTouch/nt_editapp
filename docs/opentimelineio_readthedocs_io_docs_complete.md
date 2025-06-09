# Complete Documentation from https://opentimelineio.readthedocs.io/en/stable/

> Scraped on: 2025-06-02 11:14:21
> Source: [https://opentimelineio.readthedocs.io/en/stable/](https://opentimelineio.readthedocs.io/en/stable/)
> Pages scraped: 81

---



## Page 1: Stable

**Source:** [https://opentimelineio.readthedocs.io/en/stable/](https://opentimelineio.readthedocs.io/en/stable/)

* Welcome to OpenTimelineIO’s documentation!
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/index.rst)


# Welcome to OpenTimelineIO’s documentation![¶](#welcome-to-opentimelineio-s-documentation "Permalink to this heading")


## Overview[¶](#overview "Permalink to this heading")

OpenTimelineIO (OTIO) is an API and interchange format for editorial cut
information. You can think of it as a modern Edit Decision List (EDL) that also
includes an API for reading, writing, and manipulating editorial data. It also
includes a plugin system for translating to/from existing editorial formats as
well as a plugin system for linking to proprietary media storage schemas.

OTIO supports clips, timing, tracks, transitions, markers, metadata, etc. but
not embedded video or audio. Video and audio media are referenced externally. We
encourage 3rd party vendors, animation studios and visual effects studios to
work together as a community to provide adaptors for each video editing tool and
pipeline.


## Links[¶](#links "Permalink to this heading")

[OpenTimelineIO Home Page](http://opentimeline.io/)

[OpenTimelineIO Discussion Group](https://lists.aswf.io/g/otio-discussion)


## Quick Start[¶](#quick-start "Permalink to this heading")

Quick Start

* [Quickstart](tutorials/quickstart.html)
  + [Install Prerequisites](tutorials/quickstart.html#install-prerequisites)

  + [Install OTIO](tutorials/quickstart.html#install-otio)

  + [Setup Any Additional Adapters You May Want](tutorials/quickstart.html#setup-any-additional-adapters-you-may-want)

  + [Run OTIOView](tutorials/quickstart.html#run-otioview)

* [Developer Quickstart](tutorials/quickstart.html#developer-quickstart)

  + [To build OTIO for C++ development:](tutorials/quickstart.html#to-build-otio-for-c-development)

  + [To build OTIO for Python development:](tutorials/quickstart.html#to-build-otio-for-python-development)

  + [To build OTIO for both C++ and Python development:](tutorials/quickstart.html#to-build-otio-for-both-c-and-python-development)

* [Debugging Quickstart](tutorials/quickstart.html#debugging-quickstart)

  + [Linux / GDB / LLDB](tutorials/quickstart.html#linux-gdb-lldb)

* [How to Generate the C++ Documentation:](tutorials/quickstart.html#how-to-generate-the-c-documentation)

  + [Mac / Linux](tutorials/quickstart.html#mac-linux)

* [Environment Variables](tutorials/otio-env-variables.html)
  + [Plugin Configuration](tutorials/otio-env-variables.html#plugin-configuration)

  + [Unit tests](tutorials/otio-env-variables.html#unit-tests)


## Tutorials[¶](#tutorials "Permalink to this heading")

Tutorials

* [Adapters](tutorials/adapters.html)
  + [Built-In Adapters](tutorials/adapters.html#built-in-adapters)

  + [Batteries-Included Adapters](tutorials/adapters.html#batteries-included-adapters)

  + [Additional Adapters](tutorials/adapters.html#additional-adapters)

  + [Custom Adapters](tutorials/adapters.html#custom-adapters)

* [Architecture](tutorials/architecture.html)
  + [Overview](tutorials/architecture.html#overview)

  + [Canonical Structure](tutorials/architecture.html#canonical-structure)

  + [Modules](tutorials/architecture.html#modules)

  + [Time on otio.schema.Clip](tutorials/architecture.html#time-on-otio-schema-clip)

  + [Time On Clips in Containers](tutorials/architecture.html#time-on-clips-in-containers)

  + [otio.opentime](tutorials/architecture.html#otio-opentime)

  + [otio.adapters](tutorials/architecture.html#otio-adapters)

  + [otio.media\_linkers](tutorials/architecture.html#otio-media-linkers)

  + [Example Scripts](tutorials/architecture.html#example-scripts)

* [Contributing](tutorials/contributing.html)
  + [Contributor License Agreement](tutorials/contributing.html#contributor-license-agreement)

  + [Coding Conventions](tutorials/contributing.html#coding-conventions)

  + [Platform Support Policy](tutorials/contributing.html#platform-support-policy)

  + [Git Workflow](tutorials/contributing.html#git-workflow)

* [Feature Matrix](tutorials/feature-matrix.html)
* [Timeline Structure](tutorials/otio-timeline-structure.html)
  + [Rendering](tutorials/otio-timeline-structure.html#rendering)

  + [Simple Cut List](tutorials/otio-timeline-structure.html#simple-cut-list)

  + [Transitions](tutorials/otio-timeline-structure.html#transitions)

  + [Multiple Tracks](tutorials/otio-timeline-structure.html#multiple-tracks)

  + [Nested Compositions](tutorials/otio-timeline-structure.html#nested-compositions)

* [Time Ranges](tutorials/time-ranges.html)
  + [Overview](tutorials/time-ranges.html#overview)

  + [Clips](tutorials/time-ranges.html#clips)

  + [Tracks](tutorials/time-ranges.html#tracks)

  + [Markers](tutorials/time-ranges.html#markers)

  + [Transitions](tutorials/time-ranges.html#transitions)

  + [Gaps](tutorials/time-ranges.html#gaps)

  + [Stacks](tutorials/time-ranges.html#stacks)

  + [Timelines](tutorials/time-ranges.html#timelines)

* [File Bundles](tutorials/otio-filebundles.html)
  + [Overview](tutorials/otio-filebundles.html#overview)

  + [Source Timeline](tutorials/otio-filebundles.html#source-timeline)

  + [Structure](tutorials/otio-filebundles.html#structure)

  + [Read Behavior](tutorials/otio-filebundles.html#read-behavior)

  + [MediaReferencePolicy](tutorials/otio-filebundles.html#mediareferencepolicy)

  + [OTIOD](tutorials/otio-filebundles.html#otiod)

  + [OTIOZ](tutorials/otio-filebundles.html#otioz)

  + [Example usage in otioconvert](tutorials/otio-filebundles.html#example-usage-in-otioconvert)

* [Writing an OTIO Adapter](tutorials/write-an-adapter.html)
  + [Sharing an Adapter You’ve Written With the Community](tutorials/write-an-adapter.html#sharing-an-adapter-youve-written-with-the-community)

  + [Required Functions](tutorials/write-an-adapter.html#required-functions)

  + [Constructing a Timeline](tutorials/write-an-adapter.html#constructing-a-timeline)

  + [Traversing a Timeline](tutorials/write-an-adapter.html#traversing-a-timeline)

  + [Examples](tutorials/write-an-adapter.html#examples)

* [Writing an OTIO Media Linker](tutorials/write-a-media-linker.html)
  + [Registering Your Media Linker](tutorials/write-a-media-linker.html#registering-your-media-linker)

  + [Writing a Media Linker](tutorials/write-a-media-linker.html#writing-a-media-linker)

  + [For Testing](tutorials/write-a-media-linker.html#for-testing)

* [Writing a Hook Script](tutorials/write-a-hookscript.html)
  + [Registering Your Hook Script](tutorials/write-a-hookscript.html#registering-your-hook-script)

  + [Running a Hook Script](tutorials/write-a-hookscript.html#running-a-hook-script)

  + [Order of Hook Scripts](tutorials/write-a-hookscript.html#order-of-hook-scripts)

  + [Example Hooks](tutorials/write-a-hookscript.html#example-hooks)

* [Writing an OTIO SchemaDef Plugin](tutorials/write-a-schemadef.html)
  + [Registering Your SchemaDef Plugin](tutorials/write-a-schemadef.html#registering-your-schemadef-plugin)

  + [Using the New Schema in Your Code](tutorials/write-a-schemadef.html#using-the-new-schema-in-your-code)

* [OTIO Spatial Coordinate System](tutorials/spatial-coordinates.html)
  + [Coordinate System](tutorials/spatial-coordinates.html#coordinate-system)

  + [Bounds](tutorials/spatial-coordinates.html#bounds)

  + [Bounds and Clips](tutorials/spatial-coordinates.html#bounds-and-clips)

  + [Non-Bounds representations](tutorials/spatial-coordinates.html#non-bounds-representations)

* [Schema Proposal and Development Workflow](tutorials/developing-a-new-schema.html)
  + [Introduction](tutorials/developing-a-new-schema.html#introduction)

  + [Examples](tutorials/developing-a-new-schema.html#examples)

  + [Core schema or Plugin?](tutorials/developing-a-new-schema.html#core-schema-or-plugin)

  + [Proposal](tutorials/developing-a-new-schema.html#proposal)

  + [Implementing and Iterating on a branch](tutorials/developing-a-new-schema.html#implementing-and-iterating-on-a-branch)

  + [Demo Adapter](tutorials/developing-a-new-schema.html#demo-adapter)

  + [Incrementing Other Schemas](tutorials/developing-a-new-schema.html#incrementing-other-schemas)

  + [Conclusion](tutorials/developing-a-new-schema.html#conclusion)

* [Versioning Schemas](tutorials/versioning-schemas.html)
  + [Overview](tutorials/versioning-schemas.html#overview)

  + [Schema/Version Introduction](tutorials/versioning-schemas.html#schema-version-introduction)

  + [Schema Upgrading](tutorials/versioning-schemas.html#schema-upgrading)

  + [Schema Downgrading](tutorials/versioning-schemas.html#schema-downgrading)

  + [Downgrading at Runtime](tutorials/versioning-schemas.html#downgrading-at-runtime)

  + [For Developers](tutorials/versioning-schemas.html#for-developers)


## Use Cases[¶](#use-cases "Permalink to this heading")

Use Cases

* [Animation Shot Frame Ranges Changed](use-cases/animation-shot-frame-ranges.html)
  + [Summary](use-cases/animation-shot-frame-ranges.html#summary)

  + [Example](use-cases/animation-shot-frame-ranges.html#example)

  + [Features Needed in OTIO](use-cases/animation-shot-frame-ranges.html#features-needed-in-otio)

  + [Features of Python Script](use-cases/animation-shot-frame-ranges.html#features-of-python-script)

* [Conform New Renders Into The Cut](use-cases/conform-new-renders-into-cut.html)
  + [Summary](use-cases/conform-new-renders-into-cut.html#summary)

  + [Workflow](use-cases/conform-new-renders-into-cut.html#workflow)

* [Shots Added or Removed From The Cut](use-cases/shots-added-removed-from-cut.html)
  + [Summary](use-cases/shots-added-removed-from-cut.html#summary)

  + [Example](use-cases/shots-added-removed-from-cut.html#example)

  + [Features Needed in OTIO](use-cases/shots-added-removed-from-cut.html#features-needed-in-otio)

  + [Features of Python Script](use-cases/shots-added-removed-from-cut.html#features-of-python-script)


## API References[¶](#api-references "Permalink to this heading")

API References

* [Python](python_reference.html)
  + [opentimelineio](api/python/opentimelineio.html)
    - [opentimelineio.adapters](api/python/opentimelineio.adapters.html)
    - [opentimelineio.algorithms](api/python/opentimelineio.algorithms.html)
    - [opentimelineio.console](api/python/opentimelineio.console.html)
    - [opentimelineio.core](api/python/opentimelineio.core.html)
    - [opentimelineio.exceptions](api/python/opentimelineio.exceptions.html)
    - [opentimelineio.hooks](api/python/opentimelineio.hooks.html)
    - [opentimelineio.media\_linker](api/python/opentimelineio.media_linker.html)
    - [opentimelineio.opentime](api/python/opentimelineio.opentime.html)
    - [opentimelineio.plugins](api/python/opentimelineio.plugins.html)
    - [opentimelineio.schema](api/python/opentimelineio.schema.html)
    - [opentimelineio.schemadef](api/python/opentimelineio.schemadef.html)
    - [opentimelineio.test\_utils](api/python/opentimelineio.test_utils.html)
    - [opentimelineio.url\_utils](api/python/opentimelineio.url_utils.html)
    - [opentimelineio.versioning](api/python/opentimelineio.versioning.html)
* [Language Bridges](cxx/bridges.html)
  + [Python](cxx/bridges.html#python)

  + [Swift](cxx/bridges.html#swift)

  + [Bridging to C (and other languages)](cxx/bridges.html#bridging-to-c-and-other-languages)

* [C++ Implementation Details](cxx/cxx.html)
  + [Dependencies](cxx/cxx.html#dependencies)

  + [Starting Examples](cxx/cxx.html#starting-examples)

    - [Defining a Schema](cxx/cxx.html#defining-a-schema)

    - [Reading/Writing Properties](cxx/cxx.html#reading-writing-properties)

  + [Using Schemas](cxx/cxx.html#using-schemas)

  + [Serializable Data](cxx/cxx.html#serializable-data)

  + [C++ Properties](cxx/cxx.html#c-properties)

  + [Object Graphs and Serialization](cxx/cxx.html#object-graphs-and-serialization)

  + [Memory Management](cxx/cxx.html#memory-management)

    - [Examples](cxx/cxx.html#examples)

  + [Error Handling](cxx/cxx.html#error-handling)

  + [Thread Safety](cxx/cxx.html#thread-safety)

  + [Proposed OTIO C++ Header Files](cxx/cxx.html#proposed-otio-c-header-files)

  + [Extended Memory Management Discussion](cxx/cxx.html#extended-memory-management-discussion)

* [Writing OTIO in C, C++ or Python (June 2018)](cxx/older.html)
  + [Python C-API](cxx/older.html#python-c-api)

  + [Boost-Python](cxx/older.html#boost-python)

  + [PyBind11](cxx/older.html#pybind11)

  + [Conclusion](cxx/older.html#conclusion)


## Schema Reference[¶](#schema-reference "Permalink to this heading")

Schema Reference

* [File Format Specification](tutorials/otio-file-format-specification.html)
  + [Version](tutorials/otio-file-format-specification.html#version)

  + [Note](tutorials/otio-file-format-specification.html#note)

  + [Naming](tutorials/otio-file-format-specification.html#naming)

  + [Contents](tutorials/otio-file-format-specification.html#contents)

  + [Structure](tutorials/otio-file-format-specification.html#structure)

  + [Nesting](tutorials/otio-file-format-specification.html#nesting)

  + [Metadata](tutorials/otio-file-format-specification.html#metadata)

  + [Example:](tutorials/otio-file-format-specification.html#example)

  + [Schema Specification](tutorials/otio-file-format-specification.html#schema-specification)

* [Serialized Data Documentation](tutorials/otio-serialized-schema.html)
* [Class Documentation](tutorials/otio-serialized-schema.html#class-documentation)

  + [Module: opentimelineio.adapters](tutorials/otio-serialized-schema.html#module-opentimelineio-adapters)

  + [Module: opentimelineio.core](tutorials/otio-serialized-schema.html#module-opentimelineio-core)

  + [Module: opentimelineio.hooks](tutorials/otio-serialized-schema.html#module-opentimelineio-hooks)

  + [Module: opentimelineio.media\_linker](tutorials/otio-serialized-schema.html#module-opentimelineio-media-linker)

  + [Module: opentimelineio.opentime](tutorials/otio-serialized-schema.html#module-opentimelineio-opentime)

  + [Module: opentimelineio.plugins](tutorials/otio-serialized-schema.html#module-opentimelineio-plugins)

  + [Module: opentimelineio.schema](tutorials/otio-serialized-schema.html#module-opentimelineio-schema)

* [Serialized Data (Fields Only)](tutorials/otio-serialized-schema-only-fields.html)
* [Classes](tutorials/otio-serialized-schema-only-fields.html#classes)

  + [Module: opentimelineio.adapters](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-adapters)

  + [Module: opentimelineio.core](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-core)

  + [Module: opentimelineio.hooks](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-hooks)

  + [Module: opentimelineio.media\_linker](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-media-linker)

  + [Module: opentimelineio.opentime](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-opentime)

  + [Module: opentimelineio.plugins](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-plugins)

  + [Module: opentimelineio.schema](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-schema)


## Autogenerated Plugin Reference[¶](#autogenerated-plugin-reference "Permalink to this heading")

Plugins Reference

* [Plugin Documentation](tutorials/otio-plugins.html)
* [Manifests](tutorials/otio-plugins.html#manifests)

* [Core Plugins](tutorials/otio-plugins.html#core-plugins)

  + [Adapter Plugins](tutorials/otio-plugins.html#adapter-plugins)

  + [Media Linkers](tutorials/otio-plugins.html#media-linkers)

  + [SchemaDefs](tutorials/otio-plugins.html#schemadefs)

  + [HookScripts](tutorials/otio-plugins.html#hookscripts)

  + [Hooks](tutorials/otio-plugins.html#hooks)


## Indices and tables[¶](#indices-and-tables "Permalink to this heading")

* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)

---



## Page 2: Opentimelineio.Media Linker.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.media_linker.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.media_linker.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.media\_linker
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.media_linker.rst)


# opentimelineio.media\_linker[¶](#module-opentimelineio.media_linker "Permalink to this heading")

MediaLinker plugins fire after an adapter has read a file in order to produce
[`MediaReference`](opentimelineio.core.html#opentimelineio.core.MediaReference

"opentimelineio.core.MediaReference")s that point at valid, site specific media.

They expose a `link_media_reference` function with the signature:

opentimelineio.media\_linker.link\_media\_reference(*in\_clip: [opentimelineio.schema.Clip](opentimelineio.schema.html#opentimelineio.schema.Clip "opentimelineio.schema.Clip")*) → [opentimelineio.core.MediaReference](opentimelineio.core.html#opentimelineio.core.MediaReference "opentimelineio.core.MediaReference")

Example link\_media\_reference function.

To get context information, they can inspect the metadata on the clip and on the
media reference. The
[`Composable.parent()`](opentimelineio.core.html#opentimelineio.core.Composable.parent

"opentimelineio.core.Composable.parent") method can be used to find the
containing track if metadata is stored there.

*class* opentimelineio.media\_linker.MediaLinker[¶](#opentimelineio.media_linker.MediaLinker "Permalink to this definition")is\_default\_linker()[¶](#opentimelineio.media_linker.MediaLinker.is_default_linker "Permalink to this definition")link\_media\_reference(*in\_clip*, *media\_linker\_argument\_map=None*)[¶](#opentimelineio.media_linker.MediaLinker.link_media_reference "Permalink to this definition")plugin\_info\_map()[¶](#opentimelineio.media_linker.MediaLinker.plugin_info_map "Permalink to this definition")

Adds extra adapter-specific information to call to the parent fn.

*class* opentimelineio.media\_linker.MediaLinkingPolicy[¶](#opentimelineio.media_linker.MediaLinkingPolicy "Permalink to this definition")

Enum describing different media linker policies

DoNotLinkMedia *= '\_\_do\_not\_link\_media'*[¶](#opentimelineio.media_linker.MediaLinkingPolicy.DoNotLinkMedia "Permalink to this definition")ForceDefaultLinker *= '\_\_default'*[¶](#opentimelineio.media_linker.MediaLinkingPolicy.ForceDefaultLinker "Permalink to this definition")opentimelineio.media\_linker.available\_media\_linker\_names()[¶](#opentimelineio.media_linker.available_media_linker_names "Permalink to this definition")

Return a string list of the available media linker plugins.

opentimelineio.media\_linker.default\_media\_linker()[¶](#opentimelineio.media_linker.default_media_linker "Permalink to this definition")opentimelineio.media\_linker.from\_name(*name*)[¶](#opentimelineio.media_linker.from_name "Permalink to this definition")

Fetch the media linker object by the name of the adapter directly.

opentimelineio.media\_linker.linked\_media\_reference(*target\_clip*, *media\_linker\_name='\_\_default'*, *media\_linker\_argument\_map=None*)[¶](#opentimelineio.media_linker.linked_media_reference "Permalink to this definition")

---



## Page 3: Otio Serialized Schema.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-serialized-schema.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-serialized-schema.html)

* Serialized Data Documentation
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/otio-serialized-schema.md)


# Serialized Data Documentation[¶](#serialized-data-documentation "Permalink to this heading")

This documents all the OpenTimelineIO classes that serialize to and from JSON,
omitting SchemaDef plugins. This document is automatically generated by running:

`src/py-opentimelineio/opentimelineio/console/autogen_serialized_datamodel.py`

or by running:

`make doc-model`

It is part of the unit tests suite and should be updated whenever the schema
changes. If it needs to be updated and this file regenerated, run:

`make doc-model-update`


# Class Documentation[¶](#class-documentation "Permalink to this heading")


## Module: opentimelineio.adapters[¶](#module-opentimelineio-adapters "Permalink to this heading")


### Adapter.1[¶](#adapter-1 "Permalink to this heading")

*full module path*: `opentimelineio.adapters.Adapter`

*documentation*:

```
Adapters convert between OTIO and other formats.

    Note that this class is not subclassed by adapters. Rather, an adapter is
    a python module that implements at least one of the following functions:

    .. code-block:: python

        write_to_string(input_otio)
        write_to_file(input_otio, filepath) (optionally inferred)
        read_from_string(input_str)
        read_from_file(filepath) (optionally inferred)

    ...as well as a small json file that advertises the features of the adapter
    to OTIO.  This class serves as the wrapper around these modules internal
    to OTIO.  You should not need to extend this class to create new adapters
    for OTIO.

    For more information: https://opentimelineio.readthedocs.io/en/latest/tutorials/write-an-
adapter.html. # noqa


```

parameters:

* *filepath*: Absolute path or relative path to adapter module from location of
  json.
* *name*: Adapter name.
* *suffixes*: File suffixes associated with this adapter.


## Module: opentimelineio.core[¶](#module-opentimelineio-core "Permalink to this heading")


### Composable.1[¶](#composable-1 "Permalink to this heading")

*full module path*: `opentimelineio.core.Composable`

*documentation*:

```

An object that can be composed within a :class:`~Composition` (such as :class:`~Track` or
:class:`.Stack`).

```

parameters:

* *metadata*:
* *name*:


### Composition.1[¶](#composition-1 "Permalink to this heading")

*full module path*: `opentimelineio.core.Composition`

*documentation*:

```

Base class for an :class:`~Item` that contains :class:`~Composable`\s.

Should be subclassed (for example by :class:`.Track` and :class:`.Stack`), not used directly.

```

parameters:

* *effects*:
* *enabled*: If true, an Item contributes to compositions. For example, when an
  audio/video clip is `enabled=false` the clip is muted/hidden.
* *markers*:
* *metadata*:
* *name*:
* *source\_range*:


### Item.1[¶](#item-1 "Permalink to this heading")

*full module path*: `opentimelineio.core.Item`

*documentation*:

```
None

```

parameters:

* *effects*:
* *enabled*: If true, an Item contributes to compositions. For example, when an
  audio/video clip is `enabled=false` the clip is muted/hidden.
* *markers*:
* *metadata*:
* *name*:
* *source\_range*:


### MediaReference.1[¶](#mediareference-1 "Permalink to this heading")

*full module path*: `opentimelineio.core.MediaReference`

*documentation*:

```
None

```

parameters:

* *available\_image\_bounds*:
* *available\_range*:
* *metadata*:
* *name*:


### SerializableObjectWithMetadata.1[¶](#serializableobjectwithmetadata-1 "Permalink to this heading")

*full module path*: `opentimelineio.core.SerializableObjectWithMetadata`

*documentation*:

```
None

```

parameters:

* *metadata*:
* *name*:


## Module: opentimelineio.hooks[¶](#module-opentimelineio-hooks "Permalink to this heading")


### HookScript.1[¶](#hookscript-1 "Permalink to this heading")

*full module path*: `opentimelineio.hooks.HookScript`

*documentation*:

```
None

```

parameters:

* *filepath*: Absolute path or relative path to adapter module from location of
  json.
* *name*: Adapter name.


## Module: opentimelineio.media\_linker[¶](#module-opentimelineio-media-linker "Permalink to this heading")


### MediaLinker.1[¶](#medialinker-1 "Permalink to this heading")

*full module path*: `opentimelineio.media_linker.MediaLinker`

*documentation*:

```
None

```

parameters:

* *filepath*: Absolute path or relative path to adapter module from location of
  json.
* *name*: Adapter name.


## Module: opentimelineio.opentime[¶](#module-opentimelineio-opentime "Permalink to this heading")


### RationalTime.1[¶](#rationaltime-1 "Permalink to this heading")

*full module path*: `opentimelineio.opentime.RationalTime`

*documentation*:

```

The RationalTime class represents a measure of time of :math:`rt.value/rt.rate` seconds.
It can be rescaled into another :class:`~RationalTime`'s rate.

```

parameters:

* *rate*:
* *value*:


### TimeRange.1[¶](#timerange-1 "Permalink to this heading")

*full module path*: `opentimelineio.opentime.TimeRange`

*documentation*:

```

The TimeRange class represents a range in time. It encodes the start time and the duration,
meaning that :meth:`end_time_inclusive` (last portion of a sample in the time range) and
:meth:`end_time_exclusive` can be computed.

```

parameters:

* *duration*:
* *start\_time*:


### TimeTransform.1[¶](#timetransform-1 "Permalink to this heading")

*full module path*: `opentimelineio.opentime.TimeTransform`

*documentation*:

```
1D transform for :class:`~RationalTime`. Has offset and scale.

```

parameters:

* *offset*:
* *rate*:
* *scale*:


## Module: opentimelineio.plugins[¶](#module-opentimelineio-plugins "Permalink to this heading")


### PluginManifest.1[¶](#pluginmanifest-1 "Permalink to this heading")

*full module path*: `opentimelineio.plugins.Manifest`

*documentation*:

```
Defines an OTIO plugin Manifest.

    This is considered an internal OTIO implementation detail.

    A manifest tracks a collection of plugins and enables finding them by name
    or other features (in the case of adapters, what file suffixes they
    advertise support for).

    For more information, consult the documenation.


```

parameters:

* *adapters*: Adapters this manifest describes.
* *hook\_scripts*: Scripts that can be attached to hooks.
* *hooks*: Hooks that hooks scripts can be attached to.
* *media\_linkers*: Media Linkers this manifest describes.
* *schemadefs*: Schemadefs this manifest describes.
* *version\_manifests*: Sets of versions to downgrade schemas to.


### SerializableObject.1[¶](#serializableobject-1 "Permalink to this heading")

*full module path*: `opentimelineio.plugins.PythonPlugin`

*documentation*:

```
A class of plugin that is encoded in a python module, exposed via a
    manifest.


```

parameters:

* *filepath*: Absolute path or relative path to adapter module from location of
  json.
* *name*: Adapter name.


## Module: opentimelineio.schema[¶](#module-opentimelineio-schema "Permalink to this heading")


### Clip.2[¶](#clip-2 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Clip`

*documentation*:

```

A :class:`~Clip` is a segment of editable media (usually audio or video).

Contains a :class:`.MediaReference` and a trim on that media reference.

```

parameters:

* *active\_media\_reference\_key*:
* *effects*:
* *enabled*: If true, an Item contributes to compositions. For example, when an
  audio/video clip is `enabled=false` the clip is muted/hidden.
* *markers*:
* *media\_references*:
* *metadata*:
* *name*:
* *source\_range*:


### Effect.1[¶](#effect-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Effect`

*documentation*:

```
None

```

parameters:

* *effect\_name*:
* *metadata*:
* *name*:


### ExternalReference.1[¶](#externalreference-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.ExternalReference`

*documentation*:

```
None

```

parameters:

* *available\_image\_bounds*:
* *available\_range*:
* *metadata*:
* *name*:
* *target\_url*:


### FreezeFrame.1[¶](#freezeframe-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.FreezeFrame`

*documentation*:

```
Hold the first frame of the clip for the duration of the clip.

```

parameters:

* *effect\_name*:
* *metadata*:
* *name*:
* *time\_scalar*: Linear time scalar applied to clip. 2.0 means the clip occupies
  half the time in the parent item, i.e. plays at double speed, 0.5 means the clip
  occupies twice the time in the parent item, i.e. plays at half speed.

Note that adjusting the time\_scalar of a :class:`~LinearTimeWarp` does not
affect the duration of the item this effect is attached to. Instead it affects
the speed of the media displayed within that item.


### Gap.1[¶](#gap-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Gap`

*documentation*:

```
None

```

parameters:

* *effects*:
* *enabled*: If true, an Item contributes to compositions. For example, when an
  audio/video clip is `enabled=false` the clip is muted/hidden.
* *markers*:
* *metadata*:
* *name*:
* *source\_range*:


### GeneratorReference.1[¶](#generatorreference-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.GeneratorReference`

*documentation*:

```
None

```

parameters:

* *available\_image\_bounds*:
* *available\_range*:
* *generator\_kind*:
* *metadata*:
* *name*:
* *parameters*:


### ImageSequenceReference.1[¶](#imagesequencereference-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.ImageSequenceReference`

*documentation*:

```

An ImageSequenceReference refers to a numbered series of single-frame image files. Each file can be
referred to by a URL generated by the :class:`~ImageSequenceReference`.

Image sequences can have URLs with discontinuous frame numbers, for instance if you've only rendered
 every other frame in a sequence, your frame numbers may be 1, 3, 5, etc. This is configured using
the ``frame_step`` attribute. In this case, the 0th image in the sequence is frame 1 and the 1st
image in the sequence is frame 3. Because of this there are two numbering concepts in the image
sequence, the image number and the frame number.

Frame numbers are the integer numbers used in the frame file name. Image numbers are the 0-index
based numbers of the frames available in the reference. Frame numbers can be discontinuous, image
numbers will always be zero to the total count of frames minus 1.

An example for 24fps media with a sample provided each frame numbered 1-1000 with a path
``/show/sequence/shot/sample_image_sequence.%04d.exr`` might be

.. code-block:: json

    {
      "available_range": {
        "start_time": {
          "value": 0,
          "rate": 24
        },
        "duration": {
          "value": 1000,
          "rate": 24
        }
      },
      "start_frame": 1,
      "frame_step": 1,
      "rate": 24,
      "target_url_base": "file:///show/sequence/shot/",
      "name_prefix": "sample_image_sequence.",
      "name_suffix": ".exr"
      "frame_zero_padding": 4,
    }

The same duration sequence but with only every 2nd frame available in the sequence would be

.. code-block:: json

    {
      "available_range": {
        "start_time": {
          "value": 0,
          "rate": 24
        },
        "duration": {
          "value": 1000,
          "rate": 24
        }
      },
      "start_frame": 1,
      "frame_step": 2,
      "rate": 24,
      "target_url_base": "file:///show/sequence/shot/",
      "name_prefix": "sample_image_sequence.",
      "name_suffix": ".exr"
      "frame_zero_padding": 4,
    }

A list of all the frame URLs in the sequence can be generated, regardless of frame step, with the
following list comprehension

.. code-block:: python

    [ref.target_url_for_image_number(i) for i in range(ref.number_of_images_in_sequence())]

Negative ``start_frame`` is also handled. The above example with a ``start_frame`` of ``-1`` would
yield the first three target urls as:

- ``file:///show/sequence/shot/sample_image_sequence.-0001.exr``
- ``file:///show/sequence/shot/sample_image_sequence.0000.exr``
- ``file:///show/sequence/shot/sample_image_sequence.0001.exr``

```

parameters:

* *available\_image\_bounds*:
* *available\_range*:
* *frame\_step*: Step between frame numbers in file names.
* *frame\_zero\_padding*: Number of digits to pad zeros out to in frame numbers.
* *metadata*:
* *missing\_frame\_policy*: Directive for how frames in sequence not found during
  playback or rendering should be handled.
* *name*:
* *name\_prefix*: Everything in the file name leading up to the frame number.
* *name\_suffix*: Everything after the frame number in the file name.
* *rate*: Frame rate if every frame in the sequence were played back.
* *start\_frame*: The first frame number used in file names.
* *target\_url\_base*: Everything leading up to the file name in the `target_url`.


### LinearTimeWarp.1[¶](#lineartimewarp-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.LinearTimeWarp`

*documentation*:

```

A time warp that applies a linear speed up or slow down across the entire clip.

```

parameters:

* *effect\_name*:
* *metadata*:
* *name*:
* *time\_scalar*: Linear time scalar applied to clip. 2.0 means the clip occupies
  half the time in the parent item, i.e. plays at double speed, 0.5 means the clip
  occupies twice the time in the parent item, i.e. plays at half speed.

Note that adjusting the time\_scalar of a :class:`~LinearTimeWarp` does not
affect the duration of the item this effect is attached to. Instead it affects
the speed of the media displayed within that item.


### Marker.2[¶](#marker-2 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Marker`

*documentation*:

```

A marker indicates a marked range of time on an item in a timeline, usually with a name, color or
other metadata.

The marked range may have a zero duration. The marked range is in the owning item's time coordinate
system.

```

parameters:

* *color*: Color string for this marker (for example: ‘RED’), based on the
  :class:`~Color` enum.
* *comment*: Optional comment for this marker.
* *marked\_range*: Range this marker applies to, relative to the :class:`.Item`
  this marker is attached to (e.g. the :class:`.Clip` or :class:`.Track` that owns
  this marker).
* *metadata*:
* *name*:


### MissingReference.1[¶](#missingreference-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.MissingReference`

*documentation*:

```

Represents media for which a concrete reference is missing.

Note that a :class:`~MissingReference` may have useful metadata, even if the location of the media
is not known.

```

parameters:

* *available\_image\_bounds*:
* *available\_range*:
* *metadata*:
* *name*:


### SerializableCollection.1[¶](#serializablecollection-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.SerializableCollection`

*documentation*:

```

A container which can hold an ordered list of any serializable objects. Note that this is not a
:class:`.Composition` nor is it :class:`.Composable`.

This container approximates the concept of a bin - a collection of :class:`.SerializableObject`\s
that do
not have any compositional meaning, but can serialize to/from OTIO correctly, with metadata and
a named collection.

A :class:`~SerializableCollection` is useful for serializing multiple timelines, clips, or media
references to a single file.

```

parameters:

* *metadata*:
* *name*:


### Stack.1[¶](#stack-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Stack`

*documentation*:

```
None

```

parameters:

* *effects*:
* *enabled*: If true, an Item contributes to compositions. For example, when an
  audio/video clip is `enabled=false` the clip is muted/hidden.
* *markers*:
* *metadata*:
* *name*:
* *source\_range*:


### TimeEffect.1[¶](#timeeffect-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.TimeEffect`

*documentation*:

```
Base class for all effects that alter the timing of an item.

```

parameters:

* *effect\_name*:
* *metadata*:
* *name*:


### Timeline.1[¶](#timeline-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Timeline`

*documentation*:

```
None

```

parameters:

* *global\_start\_time*:
* *metadata*:
* *name*:
* *tracks*:


### Track.1[¶](#track-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Track`

*documentation*:

```
None

```

parameters:

* *effects*:
* *enabled*: If true, an Item contributes to compositions. For example, when an
  audio/video clip is `enabled=false` the clip is muted/hidden.
* *kind*:
* *markers*:
* *metadata*:
* *name*:
* *source\_range*:


### Transition.1[¶](#transition-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.Transition`

*documentation*:

```
Represents a transition between the two adjacent items in a :class:`.Track`. For example, a cross
dissolve or wipe.

```

parameters:

* *in\_offset*: Amount of the previous clip this transition overlaps, exclusive.
* *metadata*:
* *name*:
* *out\_offset*: Amount of the next clip this transition overlaps, exclusive.
* *transition\_type*: Kind of transition, as defined by the :class:`Type` enum.


### SchemaDef.1[¶](#schemadef-1 "Permalink to this heading")

*full module path*: `opentimelineio.schema.SchemaDef`

*documentation*:

```
None

```

parameters:

* *filepath*: Absolute path or relative path to adapter module from location of
  json.
* *name*: Adapter name.

---



## Page 4: Opentimelineio.Console.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.console
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.rst)


# opentimelineio.console[¶](#module-opentimelineio.console "Permalink to this heading")

Console scripts for OpenTimelineIO

Modules

|  |  |
| --- | --- |
| [`opentimelineio.console.autogen_plugin_documentation`](opentimelineio.console.autogen_plugin_documentation.html#module-opentimelineio.console.autogen_plugin_documentation "opentimelineio.console.autogen_plugin_documentation") | Generates documentation of all the built in plugins for OpenTimelineIO |

| [`opentimelineio.console.autogen_serialized_datamodel`](opentimelineio.console.autogen_serialized_datamodel.html#module-opentimelineio.console.autogen_serialized_datamodel "opentimelineio.console.autogen_serialized_datamodel") | Generates documentation of the serialized data model for OpenTimelineIO. |

| [`opentimelineio.console.autogen_version_map`](opentimelineio.console.autogen_version_map.html#module-opentimelineio.console.autogen_version_map "opentimelineio.console.autogen_version_map") | Generate the CORE\_VERSION\_MAP for this version of OTIO |

| [`opentimelineio.console.console_utils`](opentimelineio.console.console_utils.html#module-opentimelineio.console.console_utils "opentimelineio.console.console_utils") |  |

| [`opentimelineio.console.otiocat`](opentimelineio.console.otiocat.html#module-opentimelineio.console.otiocat "opentimelineio.console.otiocat") | Print the contents of an OTIO file to stdout. |

| [`opentimelineio.console.otioconvert`](opentimelineio.console.otioconvert.html#module-opentimelineio.console.otioconvert "opentimelineio.console.otioconvert") | Python wrapper around OTIO to convert timeline files between formats. |

| [`opentimelineio.console.otiopluginfo`](opentimelineio.console.otiopluginfo.html#module-opentimelineio.console.otiopluginfo "opentimelineio.console.otiopluginfo") | Print information about the OTIO plugin ecosystem. |

| [`opentimelineio.console.otiostat`](opentimelineio.console.otiostat.html#module-opentimelineio.console.otiostat "opentimelineio.console.otiostat") | Print statistics about the otio file, including validation information. |

| [`opentimelineio.console.otiotool`](opentimelineio.console.otiotool.html#module-opentimelineio.console.otiotool "opentimelineio.console.otiotool") | otiotool is a multipurpose command line tool for inspecting, modifying, combining, and splitting OTIO files. |

---



## Page 5: Python Reference.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/python_reference.html](https://opentimelineio.readthedocs.io/en/stable/python_reference.html)

* Python
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/python_reference.rst)


# Python[¶](#python "Permalink to this heading")

|  |  |
| --- | --- |
| [`opentimelineio`](api/python/opentimelineio.html#module-opentimelineio "opentimelineio") | An editorial interchange format and library. |

---



## Page 6: Otio Serialized Schema Only Fields.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-serialized-schema-only-fields.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-serialized-schema-only-fields.html)

* Serialized Data (Fields Only)
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/otio-serialized-schema-only-fields.md)


# Serialized Data (Fields Only)[¶](#serialized-data-fields-only "Permalink to this heading")

This document is a list of all the OpenTimelineIO classes that serialize to and
from JSON, omitting plugins classes and docstrings.

This document is automatically generated by running:

`src/py-opentimelineio/opentimelineio/console/autogen_serialized_datamodel.py`

or by running:

`make doc-model`

It is part of the unit tests suite and should be updated whenever the schema
changes. If it needs to be updated and this file regenerated, run:

`make doc-model-update`


# Classes[¶](#classes "Permalink to this heading")


## Module: opentimelineio.adapters[¶](#module-opentimelineio-adapters "Permalink to this heading")


### Adapter.1[¶](#adapter-1 "Permalink to this heading")

parameters:

* *filepath*
* *name*
* *suffixes*


## Module: opentimelineio.core[¶](#module-opentimelineio-core "Permalink to this heading")


### Composable.1[¶](#composable-1 "Permalink to this heading")

parameters:

* *metadata*
* *name*


### Composition.1[¶](#composition-1 "Permalink to this heading")

parameters:

* *effects*
* *enabled*
* *markers*
* *metadata*
* *name*
* *source\_range*


### Item.1[¶](#item-1 "Permalink to this heading")

parameters:

* *effects*
* *enabled*
* *markers*
* *metadata*
* *name*
* *source\_range*


### MediaReference.1[¶](#mediareference-1 "Permalink to this heading")

parameters:

* *available\_image\_bounds*
* *available\_range*
* *metadata*
* *name*


### SerializableObjectWithMetadata.1[¶](#serializableobjectwithmetadata-1 "Permalink to this heading")

parameters:

* *metadata*
* *name*


## Module: opentimelineio.hooks[¶](#module-opentimelineio-hooks "Permalink to this heading")


### HookScript.1[¶](#hookscript-1 "Permalink to this heading")

parameters:

* *filepath*
* *name*


## Module: opentimelineio.media\_linker[¶](#module-opentimelineio-media-linker "Permalink to this heading")


### MediaLinker.1[¶](#medialinker-1 "Permalink to this heading")

parameters:

* *filepath*
* *name*


## Module: opentimelineio.opentime[¶](#module-opentimelineio-opentime "Permalink to this heading")


### RationalTime.1[¶](#rationaltime-1 "Permalink to this heading")

parameters:

* *rate*
* *value*


### TimeRange.1[¶](#timerange-1 "Permalink to this heading")

parameters:

* *duration*
* *start\_time*


### TimeTransform.1[¶](#timetransform-1 "Permalink to this heading")

parameters:

* *offset*
* *rate*
* *scale*


## Module: opentimelineio.plugins[¶](#module-opentimelineio-plugins "Permalink to this heading")


### PluginManifest.1[¶](#pluginmanifest-1 "Permalink to this heading")

parameters:

* *adapters*
* *hook\_scripts*
* *hooks*
* *media\_linkers*
* *schemadefs*
* *version\_manifests*


### SerializableObject.1[¶](#serializableobject-1 "Permalink to this heading")

parameters:

* *filepath*
* *name*


## Module: opentimelineio.schema[¶](#module-opentimelineio-schema "Permalink to this heading")


### Clip.2[¶](#clip-2 "Permalink to this heading")

parameters:

* *active\_media\_reference\_key*
* *effects*
* *enabled*
* *markers*
* *media\_references*
* *metadata*
* *name*
* *source\_range*


### Effect.1[¶](#effect-1 "Permalink to this heading")

parameters:

* *effect\_name*
* *metadata*
* *name*


### ExternalReference.1[¶](#externalreference-1 "Permalink to this heading")

parameters:

* *available\_image\_bounds*
* *available\_range*
* *metadata*
* *name*
* *target\_url*


### FreezeFrame.1[¶](#freezeframe-1 "Permalink to this heading")

parameters:

* *effect\_name*
* *metadata*
* *name*
* *time\_scalar*


### Gap.1[¶](#gap-1 "Permalink to this heading")

parameters:

* *effects*
* *enabled*
* *markers*
* *metadata*
* *name*
* *source\_range*


### GeneratorReference.1[¶](#generatorreference-1 "Permalink to this heading")

parameters:

* *available\_image\_bounds*
* *available\_range*
* *generator\_kind*
* *metadata*
* *name*
* *parameters*


### ImageSequenceReference.1[¶](#imagesequencereference-1 "Permalink to this heading")

parameters:

* *available\_image\_bounds*
* *available\_range*
* *frame\_step*
* *frame\_zero\_padding*
* *metadata*
* *missing\_frame\_policy*
* *name*
* *name\_prefix*
* *name\_suffix*
* *rate*
* *start\_frame*
* *target\_url\_base*


### LinearTimeWarp.1[¶](#lineartimewarp-1 "Permalink to this heading")

parameters:

* *effect\_name*
* *metadata*
* *name*
* *time\_scalar*


### Marker.2[¶](#marker-2 "Permalink to this heading")

parameters:

* *color*
* *comment*
* *marked\_range*
* *metadata*
* *name*


### MissingReference.1[¶](#missingreference-1 "Permalink to this heading")

parameters:

* *available\_image\_bounds*
* *available\_range*
* *metadata*
* *name*


### SerializableCollection.1[¶](#serializablecollection-1 "Permalink to this heading")

parameters:

* *metadata*
* *name*


### Stack.1[¶](#stack-1 "Permalink to this heading")

parameters:

* *effects*
* *enabled*
* *markers*
* *metadata*
* *name*
* *source\_range*


### TimeEffect.1[¶](#timeeffect-1 "Permalink to this heading")

parameters:

* *effect\_name*
* *metadata*
* *name*


### Timeline.1[¶](#timeline-1 "Permalink to this heading")

parameters:

* *global\_start\_time*
* *metadata*
* *name*
* *tracks*


### Track.1[¶](#track-1 "Permalink to this heading")

parameters:

* *effects*
* *enabled*
* *kind*
* *markers*
* *metadata*
* *name*
* *source\_range*


### Transition.1[¶](#transition-1 "Permalink to this heading")

parameters:

* *in\_offset*
* *metadata*
* *name*
* *out\_offset*
* *transition\_type*


### SchemaDef.1[¶](#schemadef-1 "Permalink to this heading")

parameters:

* *filepath*
* *name*

---



## Page 7: Animation Shot Frame Ranges.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/use-cases/animation-shot-frame-ranges.html](https://opentimelineio.readthedocs.io/en/stable/use-cases/animation-shot-frame-ranges.html)

* Animation Shot Frame Ranges Changed
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/use-cases/animation-shot-frame-ranges.md)


# Animation Shot Frame Ranges Changed[¶](#animation-shot-frame-ranges-changed "Permalink to this heading")

**Status: Planned**


## Summary[¶](#summary "Permalink to this heading")

This case is very similar to the [Shots Added or Removed From The
Cut](shots-added-removed-from-cut.html). The editorial and animation departments
are working with a sequence of shots simultaneously over the course of a few
weeks. The initial delivery of rendered video clips from animation to editorial
provides enough footage for the editor(s) to work with, at least as a starting
point. As the cut evolves, the editor(s) may need more frames at the head or
tail of some shots, or they may trim frames from the head or tail that are no
longer needed. Usually there is an agreement that some extra frames, called
handles, should be present at the head and tail of each shot to give the editors
some flexibility. In the case where the editors need more frames than the
handles provide, they might use a freeze frame effect, or a slow down effect to
stretch the clip, or simply repeat a segment of a clip to fill the gap. This is
a sign that new revisions of those shots should be animated and rendered with
more frames to fill the needs of the cut. Furthermore, as the sequence nears
completion, the cut becomes more stable and the cost of rendering frames becomes
higher, so there is a desire to trim unused handles from the shots on the
animation side. In both cases, we can use OTIO to compare the frame range of
each shot between the two departments.


## Example[¶](#example "Permalink to this heading")

Animation delivers the first pass of 100 shots to editorial. Editorial makes an
initial cut of the sequence. In the cut, several shots are trimmed down to less
than half of the initial length, but 2 shots need to be extended. Editorial
exports an EDL or AAF of the sequence from Avid Media Composer and gives this
cut to the animation department. Animation runs a Python script which compares
the frame range of each shot used in the cut to the frame range of the most
recent take of each shot being animated. Any shot that is too short must be
extended and any shot that is more than 12 frames too long can be trimmed down.
The revised shots are animated, re-rendered and re-delivered to editorial. Upon
receiving these new deliveries, editorial will cut them into the sequence (see
also [Conform New Renders Into The Cut](conform-new-renders-into-cut.html)). For
shots that used timing effects to temporarily extend them, those effects can be
removed, since the new version of those shots is now longer.


## Features Needed in OTIO[¶](#features-needed-in-otio "Permalink to this heading")

* EDL reading

  + Clip names for video track
  + Source frame range for each clip
  + [Timing
    effects](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues/39)
* [AAF
  reading](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues/1)

  + Clip names across all video tracks, subclips, etc.
  + Source frame range for each clip
  + Timing effects
* Timeline should include (done)

  + a Stack of tracks, each of which is a Sequence
* Sequence should include (done)

  + a list of Clips
* Clips should include (done)

  + Name
  + Metadata
  + Timing effects
* [Timing
  effects](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues/39)

  + Source frame range of each clip as effected by timing effects.
* Composition

  + Clips in lower tracks that are obscured (totally or partially) by overlapping
    clips in higher tracks are considered trimmed or hidden.
  + Visible frame range for each clip.


## Features of Python Script[¶](#features-of-python-script "Permalink to this heading")

* Use OTIO to read the EDL or AAF
* Iterate through every Clip in the Timeline, printing its name and visible frame
  range

---



## Page 8: Versioning Schemas.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/versioning-schemas.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/versioning-schemas.html)

* Versioning Schemas
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/versioning-schemas.md)


# Versioning Schemas[¶](#versioning-schemas "Permalink to this heading")


## Overview[¶](#overview "Permalink to this heading")

This document describes OpenTimelineIO’s systems for dealing with different
schema versions when reading files, writing files, or during development of the
library itself. It is intended for developers who are integrating OpenTimelineIO
into their pipelines or applications, or working directly on OpenTimelineIO.

TL;DR for users: OpenTimelineIO should be able to read files produced by older
versions of the library and be able to write files that are compatible with
older versions of the library from newer versions.


## Schema/Version Introduction[¶](#schema-version-introduction "Permalink to this heading")

Each SerializableObject (the base class of OpenTimelineIO) has `schema_name` and
`schema_version` fields. The `schema_name` is a string naming the schema, for
example, `Clip`, and the `schema_version` is an integer of the current version
number, for example, `3`.

SerializableObjects can be queried for these using the `.schema_name()` and
`.schema_version()` methods. For a given release of the OpenTimelineIO library,
in-memory objects the library creates will always be the same schema version. In
other words, if `otio.schema.Clip()` instantiates an object with
`schema_version` 2, there is no way to get an in-memory `Clip` object with
version 1.

OpenTimelineIO can still interoperate with older and newer versions of the
library by way of the schema upgrading/downgrading system. As OpenTimelineIO
deserializes json from a string or disk, it will upgrade the schemas to the
version supported by the library before instantiating the concrete in-memory
object. Similarly, when serializing OpenTimelineIO back to disk, the user can
instruct OpenTimelineIO to downgrade the JSON to older versions of the schemas.
In this way, a newer version of OpenTimelineIO can read files with older
schemas, and a newer version of OpenTimelineIO can generate JSON with older
schemas in it.


## Schema Upgrading[¶](#schema-upgrading "Permalink to this heading")

Once a type is registered to OpenTimelineIO, developers may also register
upgrade functions. In python, each upgrade function takes a dictionary and
returns a dictionary. In C++, the AnyDictionary is manipulated in place. Each
upgrade function is associated with a version number - this is the version
number that it upgrades to.

C++ Example (can be viewed/run in `examples/upgrade_downgrade_example.cpp`):

```
class SimpleClass : public otio::SerializableObject
{
public:
    struct Schema
    {
        static auto constexpr name   = "SimpleClass";
        static int constexpr version = 2;
    };

    void set_new_field(int64_t val) { _new_field = val; }
    int64_t new_field() const { return _new_field; }

protected:
    using Parent = SerializableObject;

    virtual ~SimpleClass() = default;

    virtual bool
    read_from(Reader& reader)
    {
        auto result = (
            reader.read("new_field", &_new_field)
            && Parent::read_from(reader)
        );

        return result;
    }

    virtual void
    write_to(Writer& writer) const
    {
        Parent::write_to(writer);
        writer.write("new_field", _new_field);
    }

private:
    int64_t _new_field;
};

    // later, during execution:

    // register type and upgrade/downgrade functions
    otio::TypeRegistry::instance().register_type<SimpleClass>();

    // 1->2
    otio::TypeRegistry::instance().register_upgrade_function(
        SimpleClass::Schema::name,
        2,
        
        {
            (*d)["new_field"] = (*d)["my_field"];
            d->erase("my_field");
        }
    );

```

Python Example:

```
@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.2"
  my_field = otio.core.serializable_field("new_field", int)

@otio.core.upgrade_function_for(SimpleClass, 2)
def upgrade_one_to_two(data):
  return {"new_field" : data["my_field"] }

```

When upgrading schemas, OpenTimelineIO will call each upgrade function in order
in an attempt to get to the current version. For example, if a schema is
registered to have version 3, and a file with version 1 is read, OpenTimelineIO
will attempt to call the 1->2 function, then the 2->3 function before
instantiating the concrete class.


## Schema Downgrading[¶](#schema-downgrading "Permalink to this heading")

Similarly, once a type is registered, downgrade functions may be registered.
Downgrade functions take a dictionary of the version specified and return a
dictionary of the schema version one lower. For example, if a downgrade function
is registered for version 5, that will downgrade from 5 to 4.

C++ Example, building off the prior section SimpleClass example (can be
viewed/run in `examples/upgrade_downgrade_example.cpp`):

```
// 2->1
otio::TypeRegistry::instance().register_downgrade_function(
    SimpleClass::Schema::name,
    2,
    
    {
        (*d)["my_field"] = (*d)["new_field"];
        d->erase("new_field");
    }
);

```

Python Example:

```
@otio.core.upgrade_function_for(SimpleClass, 2)
def downgrade_two_to_one(data):
  return {"my_field" : data["new_field"] }

```

To specify what version of a schema to downgrade to, the serialization functions
include an optional `schema_version_targets` argument which is a map of schema
name to target schema version. During serialization, any schemas who are listed
in the map and are of greater version than specified in the map will be
converted to AnyDictionary and run through the necessary downgrade functions
before being serialized.

Example C++:

```
auto sc = otio::SerializableObject::Retainer<SimpleClass>(new SimpleClass());
sc->set_new_field(12);

// this will only downgrade the SimpleClass, to version 1
otio::schema_version_map downgrade_manifest = {
    {"SimpleClass", 1}
};

// write it out to disk, downgrading to version 1
sc->to_json_file("/var/tmp/simpleclass.otio", &err, &downgrade_manifest);

```

Example python:

```
sc = SimpleClass()
otio.adapters.write_to_file(
    sc,
    "/path/to/output.otio",
    target_schema_versions={"SimpleClass":1}
)

```


### Schema-Version Sets[¶](#schema-version-sets "Permalink to this heading")

In addition to passing in dictionaries of desired target schema versions,
OpenTimelineIO also provides some tools for having sets of schemas with an
associated label. The core C++ library contains a compiled-in map of them, the
`CORE_VERSION_MAP`. This is organized (as of v0.15.0) by library release
versions label, ie “0.15.0”, “0.14.0” and so on.

In order to downgrade to version 0.15.0 for example:

```
auto downgrade_manifest = otio::CORE_VERSION_MAP["0.15.0"];

// write it out to disk, downgrading to version 1
sc->to_json_file("/var/tmp/simpleclass.otio", &err, &downgrade_manifest);

```

In python, an additional level of indirection is provided, “FAMILY”, which is
intended to allow developers to define their own sets of target versions for
their plugin schemas. For example, a studio might have a family named “MYFAMILY”
under which they organize labels for their internal releases of their own
plugins.

These can be defined in a plugin manifest, which is a `.plugin_manifest.json`
file found on the environment variable
[OTIO\_PLUGIN\_MANIFEST\_PATH](otio-env-variables.html#term-OTIO_PLUGIN_MANIFEST_PATH).

For example:

```
{
    "OTIO_SCHEMA" : "PluginManifest.1",
    "version_manifests": {
        "MYFAMILY": {
            "June2022": {
                "SimpleClass": 2,
                ...
            },
            "May2022": {
                "SimpleClass": 1,
                ...
            }
        }
    }
}

```

To fetch the version maps and work with this, the python API provides some
additional functions:

```

# example using a built in family

downgrade_manifest = otio.versioning.fetch_map("OTIO_CORE", "0.15.0")
otio.adapters.write_to_file(
    sc,
    "/path/to/file.otio",
    target_schema_versions=downgrade_manifest
)


# using a custom family defined in a plugin manifest json file

downgrade_manifest = otio.versioning.fetch_map("MYFAMILY", "June2022")
otio.adapters.write_to_file(
    sc,
    "/path/to/file.otio",
    target_schema_versions=downgrade_manifest
)

```

To fetch the version sets defined by the core from python, use the `OTIO_CORE`
family of version sets.

See the [versioning module](../api/python/opentimelineio.versioning.html) for
more information on accessing these.


## Downgrading at Runtime[¶](#downgrading-at-runtime "Permalink to this heading")

If you are using multiple pieces of software built with mismatched versions of
OTIO, you may need to configure the newer one(s) to write out OTIO in an older
format without recompiling or modifying the software.

You can accomplish this in two ways:

* The
  [OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL](otio-env-variables.html#term-OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL)

  environment variable can specify a family and version.
* The `otioconvert` utility program can downgrade an OTIO file to an older
  version.


### OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL Environment Variable[¶](#otio-default-target-version-family-label-environment-variable "Permalink to this heading")

If your software uses OTIO’s Python adapter system, then you can set the
[OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL](otio-env-variables.html#term-OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL)

environment variable with a `FAMILY:VERSION` value. For example, in a \*nix
shell: `env OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL=OTIO_CORE:0.14.0
my_program`

The `OTIO_CORE` family is pre-populated with the core OTIO schema versions for
previous OTIO releases, for example `0.14.0`. If you have custom schema that
needs to be downgraded as well, you will need to specify your own family and
version mapping, as described above.


### Downgrading with otioconvert[¶](#downgrading-with-otioconvert "Permalink to this heading")

If your software uses OTIO’s C++ API, then it does not look for the
[OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL](otio-env-variables.html#term-OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL)

environment variable, but you can convert an OTIO file after it has been created
with the `otioconvert` utility.

You can either use a family like this:

```
env OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL=OTIO_CORE:0.14.0 otioconvert -i input.otio -o output.otio

```

or you can specify the version mapping for each schema you care about like this:

```
otioconvert -i input.otio -o output.otio -A target_schema_versions="{'Clip':1, 'Timeline':1, 'Marker':2}"

```


## For Developers[¶](#for-developers "Permalink to this heading")

During the development of OpenTimelineIO schemas, whether they are in the core
or in plugins, it is expected that schemas will change and evolve over time.
Here are some processes for doing that.


### Changing a Field[¶](#changing-a-field "Permalink to this heading")

Given `SimpleClass`:

```
import opentimelineio as otio

@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.1"
  my_field = otio.core.serializable_field("my_field", int)

```

And `my_field` needs to be renamed to `new_field`. To do this:

* Make the change in the class
* Bump the version number in the label
* add upgrade and downgrade functions

```
@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.2"
  new_field = otio.core.serializable_field("new_field", int)

@otio.core.upgrade_function_for(SimpleClass, 2)
def upgrade_one_to_two(data):
  return {"new_field" : data["my_field"] }

@otio.core.downgrade_function_from(SimpleClass, 2)
def downgrade_two_to_one(data):
    return {"my_field": data["new_field"]}

```

Changing it again, now `new_field` becomes `even_newer_field`.

```
@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.2"
  even_newer_field = otio.core.serializable_field("even_newer_field", int)

@otio.core.upgrade_function_for(SimpleClass, 2)
def upgrade_one_to_two(data):
  return {"new_field" : data["my_field"] }


# NOTE we now have a second upgrade function

@otio.core.upgrade_function_for(SimpleClass, 3)
def upgrade_two_to_three(data):
  return {"even_newer_field" : data["new_field"] }

@otio.core.downgrade_function_from(SimpleClass, 2)
def downgrade_two_to_one(data):
    return {"my_field": data["new_field"]}


# ...and corresponding second downgrade function

@otio.core.downgrade_function_from(SimpleClass, 3)
def downgrade_two_to_one(data):
    return {"new_field": data["even_newer_field"]}

```


### Adding or Removing a Field[¶](#adding-or-removing-a-field "Permalink to this heading")

Starting from the same class:

```
@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.1"
  my_field = otio.core.serializable_field("my_field", int)

```

If a change to a schema is to add a field, for which the default value is the
correct value for an old schema, then no upgrade or downgrade function is
needed. The parser ignores values that aren’t in the schema.

Additionally, upgrade functions will be called in order, but they need not cover
every version number. So if there is an upgrade function for version 2 and 4, to
get to version 4, OTIO will automatically apply function 2 and then function 4
in order, skipping the missing 3.

Downgrade functions must be called in order with no gaps.

Example of adding a field (`other_field`):

```
@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.2"
  my_field = otio.core.serializable_field("my_field", int)
  other_field = otio.core.serializable_field("other_field", int)

```

Removing a field (`my_field`):

```
@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.3"
  other_field = otio.core.serializable_field("other_field", int)

```

Similarly, when deleting a field, if the field is now ignored and does not
contribute to computation, no upgrade or downgrade function is needed.

---



## Page 9: Opentimelineio.Adapters.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.adapters
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.adapters.rst)


# opentimelineio.adapters[¶](#module-opentimelineio.adapters "Permalink to this heading")

Expose the adapter interface to developers.

To read from an existing representation, use the read\_from\_string and
read\_from\_file functions. To query the list of adapters, use the
available\_adapter\_names function.

The otio\_json adapter is provided as a the canonical, lossless, serialization
of the in-memory otio schema. Other adapters are to varying degrees lossy. For
more information, consult the documentation in the individual adapter modules.

*class* opentimelineio.adapters.Adapter[¶](#opentimelineio.adapters.Adapter "Permalink to this definition")

Adapters convert between OTIO and other formats.

Note that this class is not subclassed by adapters. Rather, an adapter is a
python module that implements at least one of the following functions:

```
write_to_string(input_otio)
write_to_file(input_otio, filepath) (optionally inferred)
read_from_string(input_str)
read_from_file(filepath) (optionally inferred)

```

…as well as a small json file that advertises the features of the adapter to
OTIO. This class serves as the wrapper around these modules internal to OTIO.
You should not need to extend this class to create new adapters for OTIO.

For more information:
<https://opentimelineio.readthedocs.io/en/latest/tutorials/write-an-adapter.html>.

# noqa

has\_feature(*feature\_string*)[¶](#opentimelineio.adapters.Adapter.has_feature "Permalink to this definition")

return true if adapter supports feature\_string, which must be a key of the
\_FEATURE\_MAP dictionary.

Will trigger a call to
[`PythonPlugin.module()`](opentimelineio.plugins.python_plugin.html#opentimelineio.plugins.python_plugin.PythonPlugin.module

"opentimelineio.plugins.python_plugin.PythonPlugin.module"), which imports the
plugin.

plugin\_info\_map()[¶](#opentimelineio.adapters.Adapter.plugin_info_map "Permalink to this definition")

Adds extra adapter-specific information to call to the parent fn.

read\_from\_file(*filepath*, *media\_linker\_name='\_\_default'*, *media\_linker\_argument\_map=None*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.Adapter.read_from_file "Permalink to this definition")

Execute the read\_from\_file function on this adapter.

If read\_from\_string exists, but not read\_from\_file, execute that with a
trivial file object wrapper.

read\_from\_string(*input\_str*, *media\_linker\_name='\_\_default'*, *media\_linker\_argument\_map=None*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.Adapter.read_from_string "Permalink to this definition")

Call the read\_from\_string function on this adapter.

*property* suffixes[¶](#opentimelineio.adapters.Adapter.suffixes "Permalink to this definition")

File suffixes associated with this adapter.

write\_to\_file(*input\_otio*, *filepath*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.Adapter.write_to_file "Permalink to this definition")

Execute the write\_to\_file function on this adapter.

If write\_to\_string exists, but not write\_to\_file, execute that with a
trivial file object wrapper.

write\_to\_string(*input\_otio*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.Adapter.write_to_string "Permalink to this definition")

Call the write\_to\_string function on this adapter.

opentimelineio.adapters.available\_adapter\_names()[¶](#opentimelineio.adapters.available_adapter_names "Permalink to this definition")

Return a string list of the available adapters.

opentimelineio.adapters.from\_filepath(*filepath*)[¶](#opentimelineio.adapters.from_filepath "Permalink to this definition")

Guess the adapter object to use for a given filepath.

For example, `foo.otio` returns the `otio_json` adapter.

opentimelineio.adapters.from\_name(*name*)[¶](#opentimelineio.adapters.from_name "Permalink to this definition")

Fetch the adapter object by the name of the adapter directly.

opentimelineio.adapters.read\_from\_file(*filepath*, *adapter\_name=None*, *media\_linker\_name='\_\_default'*, *media\_linker\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.read_from_file "Permalink to this definition")

Read filepath using adapter\_name.

If adapter\_name is None, try and infer the adapter name from the filepath.

Example[¶](#id1 "Permalink to this code")

```
 timeline = read_from_file("example_trailer.otio")
 timeline = read_from_file("file_with_no_extension", "cmx_3600")

```

opentimelineio.adapters.read\_from\_string(*input\_str*, *adapter\_name='otio\_json'*, *media\_linker\_name='\_\_default'*, *media\_linker\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.read_from_string "Permalink to this definition")

Read a timeline from input\_str using adapter\_name.

This is useful if you obtain a timeline from someplace other than the
filesystem.

Example[¶](#id2 "Permalink to this code")

```
 raw_text = urlopen(my_url).read()
 timeline = read_from_string(raw_text, "otio_json")

```

opentimelineio.adapters.suffixes\_with\_defined\_adapters(*read=False*, *write=False*)[¶](#opentimelineio.adapters.suffixes_with_defined_adapters "Permalink to this definition")

Return a set of all the suffixes that have adapters defined for them.

opentimelineio.adapters.write\_to\_file(*input\_otio*, *filepath*, *adapter\_name=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.write_to_file "Permalink to this definition")

Write input\_otio to filepath using adapter\_name.

If adapter\_name is None, infer the adapter\_name to use based on the filepath.

Example[¶](#id3 "Permalink to this code")

```
 otio.adapters.write_to_file(my_timeline, "output.otio")

```

opentimelineio.adapters.write\_to\_string(*input\_otio*, *adapter\_name='otio\_json'*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.write_to_string "Permalink to this definition")

Return input\_otio written to a string using adapter\_name.

Example[¶](#id4 "Permalink to this code")

```
 raw_text = otio.adapters.write_to_string(my_timeline, "otio_json")

```

Modules

|  |  |
| --- | --- |
| [`opentimelineio.adapters.adapter`](opentimelineio.adapters.adapter.html#module-opentimelineio.adapters.adapter "opentimelineio.adapters.adapter") | Implementation of the OTIO internal Adapter system. |

| [`opentimelineio.adapters.file_bundle_utils`](opentimelineio.adapters.file_bundle_utils.html#module-opentimelineio.adapters.file_bundle_utils "opentimelineio.adapters.file_bundle_utils") | Common utilities used by the file bundle adapters (otiod and otioz). |

| [`opentimelineio.adapters.otio_json`](opentimelineio.adapters.otio_json.html#module-opentimelineio.adapters.otio_json "opentimelineio.adapters.otio_json") | Adapter for reading and writing native .otio json files. |

| [`opentimelineio.adapters.otiod`](opentimelineio.adapters.otiod.html#module-opentimelineio.adapters.otiod "opentimelineio.adapters.otiod") | OTIOD adapter - bundles otio files linked to local media in a directory |

| [`opentimelineio.adapters.otioz`](opentimelineio.adapters.otioz.html#module-opentimelineio.adapters.otioz "opentimelineio.adapters.otioz") | OTIOZ adapter - bundles otio files linked to local media |

---



## Page 10: Opentimelineio.Schemadef.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schemadef.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schemadef.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.schemadef
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schemadef.rst)


# opentimelineio.schemadef[¶](#module-opentimelineio.schemadef "Permalink to this heading")

---



## Page 11: Otio Timeline Structure.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-timeline-structure.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-timeline-structure.html)

* Timeline Structure
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/otio-timeline-structure.md)


# Timeline Structure[¶](#timeline-structure "Permalink to this heading")

An OpenTimelineIO `Timeline` object can contain many tracks, nested stacks,
clips, gaps, and transitions. This document is meant to clarify how these
objects nest within each other, and how they work together to represent an
audio/video timeline.


## Rendering[¶](#rendering "Permalink to this heading")

Rendering of the image tracks in a timeline is done in painter order. The layers
in a stack are iterated from the bottom (the first entry in the stack) towards
the top (the final entry in the stack). Images in a stack overlay lower images
using an alpha composite operation respecting any alpha in the source materials.
All compositing is assumed to occur over a background of zero values in color
components, and 100% values for alpha components. Within a track, clips may
overlap via a transition. In that case, the contribution of track is the linear
blend of the elements joined by the transition.

If there are effects on a clip, OpenTimelineIO does not say anything about the
impact of the effect and deviation from the base behavior is application
specific.

Rendering of the audio tracks is additive. It is strongly advised, but not
required, that the summed audio is summed as floating point, and that it is
processed through a compression filter in order to prevent clipping and
distortion.


## Simple Cut List[¶](#simple-cut-list "Permalink to this heading")

Let’s start with a simple cut list of a few clips. This is stored as a single
`Timeline` with a single `Track` which contains several `Clip` children, spliced
end-to-end.

*Figure 1 - Simple Cut List*

Since a `Timeline` can hold multiple tracks, it always has a top-level `Stack`
object to hold its `Track` children. In this case, that `Stack` has just one
`Track`, named “Track-001”.

Within “Track-001”, there are four `Clip` objects, named “Clip-001”, “Clip-002”,
“Clip-003”, and “Clip-004”. Each `Clip` has a corresponding media reference,
“Media-001”, “Media-002”, etc.

At the bottom level, we see that each media reference has a target\_url and an
available\_range. The target\_url tells us where to find the media (e.g. a file
path or network URL, etc.) The available\_range specifies the range of media
that is available in the file that it points to. An available\_range is a
`TimeRange` object which specifies a start\_time and duration. The start\_time
and duration are each `RationalTime` objects, which store a value and rate. Thus
we can use `RationalTime(7,24)` to mean frame 7 at 24 frames per second. In the
diagram we write this as just 7 for brevity.

In this case most of our media references have an available\_range that starts
at 0 for some number of frames. One of the media references starts at 100.
Assuming the media is 24 frames per second, this means that the media file
contains media that starts at 4 seconds and 4 frames (timecode 00:00:04:04).

In many cases you might not know the available\_range because the media is
missing, or points to a file path or URL which might be expensive to query. If
that’s the case, then the available\_range of a media\_reference will be `None`.

Above the media references, we see that each `Clip` has a source\_range, which
specifies a trimmed segment of media. In cases where we only want a portion of
the available media, the source\_range will start at a higher start\_time,
and/or have a shorter duration. The colored segments of “Media-001”, “Media-002”
and “Media-003” show the portion that each clip’s source\_range references.

In the case of “Clip-004”, the source\_range is `None`, so it exposes its entire
media reference. In the OTIO API, you can query the trimmed\_range() of a clip
to get the range of media used regardless of whether it has a source\_range,
available\_range or both - but it needs at least one of the two.

Also note that a clip’s source\_range could refer to a segment outside the
available\_range of its media reference. That is fine, and comes up in practice
often (e.g. I only rendered the first half of my shot). OTIO itself does no
snapping or verification of this, but downstream applications may handle this in
a variety of ways.

The single `Track` in this example contains all four clips in order. You can ask
the `Track` or `Stack` for its trimmed\_range() or duration() and it will sum up
the trimmed lengths of its children. In later examples, we will see cases where
a `Track` or `Stack` is trimmed by setting a source\_range, but in this example
they are not trimmed.


## Transitions[¶](#transitions "Permalink to this heading")

A `Transition` is a visual effect, like a cross dissolve or wipe, that blends
two adjacent items on the same track. The most common case is a fade or
cross-dissolve between two clips, but OTIO supports transitions between any two
`Composable` items (`Clip`s, `Gap`s, or nested `Track`s or `Stack`s).

*Figure 2 - Transitions*

In Figure 2, there is a `Transition` between “Clip-002” and “Clip-003”. The
in\_offset and out\_offset of the `Transition` specify how much media from the
adjacent clips is used by the transition.

Notice that the `Transition` itself does not make “Track-001” any shorter or
longer. If a playback tool is not able to render a transition, it may simply
ignore transitions and the overall length of the timeline will not be affected.

In Figure 2, the `Transition`’s in\_offset of 2 frames means that frames 1 and 2
of “Media-003” are used in the cross dissolve. The out\_offset of 3 frames means
that frames 8, 9, 10 of “Media-002” are used. Notice that “Media-002“‘s
available\_range is 2 frames too short to satisfy the desired length of the
cross-dissolve. OTIO does not prevent you from doing this, as it may be
important for some use cases. OTIO also does not specify what a playback tool
might display in this case.

A `Transition`’s in\_offset and out\_offset are not allowed to extend beyond the
duration of the adjacent clips. If a clip has transitions at both ends, the two
transitions are not allowed to overlap. Also, you cannot place two transitions
next to each other in a track; there must be a composable item between them.

A fade to or from black will often be represented as a transition to or from a
`Gap`, which can be 0 duration. If multiple tracks are present note that a `Gap`
is meant to be transparent, so you may need to consider using a `Clip` with a
`GeneratorReference` if you require solid black or any other solid color.


## Multiple Tracks[¶](#multiple-tracks "Permalink to this heading")

A more typical timeline will include multiple video tracks. In Figure 3, the
top-level `Stack` now contains “Track-001”, “Track-002”, and “Track-003” which
contain some `Clip` and `Gap` children. Figure 3 also shows a flattened copy of
the timeline to illustrate how multitrack composition works.

*Figure 3 - Multiple Tracks*

The `Gap` in “Track-001” is 4 frames long, and the track below, “Track-002”, has
frames 102-105 of “Clip-003” aligned with the `Gap` above, so those frames show
through in the resulting flattened `Track`.

Note that the `Gap` at the front of “Track-002” is used just to offset
“Clip-003”. This is a common way to shift clips around on a track, but you may
also use the `Track`’s source\_range to do this, as illustrated in “Track-003”.

“Clip-005” is completely obscured by “Clip-003” above it, so “Clip-005” does not
appear in the flattened timeline at all.

You might also notice that “Track-001” is longer than the other two. If you
wanted “Track-002” to be the same length, then you would need to append a `Gap`
at the end. If you wanted “Track-003” to be the same length, then you could
extend the duration of its source\_range to the desired length. In both cases,
the trimmed\_range() will be the same.


## Nested Compositions[¶](#nested-compositions "Permalink to this heading")

The children of a `Track` can be any `Composable` object, which includes
`Clip`s, `Gap`s, `Track`s, `Stack`s, and `Transition`s. In Figure 4 we see an
example of a `Stack` nested within a `Track`.

*Figure 4 - Nested Compositions*

In this example, the top-level `Stack` contains only one `Track`. “Track-001”
contains four children, “Clip-001”, “Nested Stack”, “Gap”, and “Clip-004”. By
nesting a `Composition` (either `Track` or `Stack`) we can refer to a
`Composition` as though it was just another `Clip` in the outer `Composition`.
If a source\_range is specified, then only a trimmed segment of the inner
`Composition` is included. In this case that is frames 2 through 7 of “Nested
Stack”. If no source\_range is specified, then the full available\_range of the
nested composition is computed and included in the outer composition.

“Nested Stack” contains two tracks, with some clips, gaps, and a track-level
source\_range on the lower track. This illustrates how the content of “Nested
Stack” is composed upwards into “Track-001” so that a trimmed portion of
“Clip-005” and “Clip-003” appear in the flattened composition.

Notice how the `Gap` in “Track-001” cannot see anything inside the nested
composition (“Clip-003”, etc.) because those are not peers to “Track-001”, they
are nested within “Nested Stack” and do not spill over into adjacent `Gap`s. In
other words, “Nested Stack” behaves just like a `Clip` that happens to have
complex contents rather than a simple media reference.

---



## Page 12: Adapters.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/adapters.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/adapters.html)

* Adapters
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/adapters.md)


# Adapters[¶](#adapters "Permalink to this heading")

While OpenTimelineIO favors the `.otio` JSON format, Python OpenTimelineIO
supports many file formats via adapter plugins.


## Built-In Adapters[¶](#built-in-adapters "Permalink to this heading")

The OpenTimelineIO native file format adapters that are present in the
`opentimelineio` python package are:

* [otio\_json](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/src/py-opentimelineio/opentimelineio/adapters/otio_json.py)
  - OpenTimelineIO’s native file format.
* [otiod](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/src/py-opentimelineio/opentimelineio/adapters/otiod.py)
  - a directory bundle of a `.otio` file along with referenced media.
* [otioz](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/src/py-opentimelineio/opentimelineio/adapters/otioz.py)
  - a zip file bundle of a `.otio` file along with referenced media.


## Batteries-Included Adapters[¶](#batteries-included-adapters "Permalink to this heading")

To also install a curated list of additional useful adapters, use the
[OpenTimelineIO-Plugins](https://pypi.org/project/OpenTimelineIO-Plugins/)
python package. In addition to the OpenTimelineIO native adapters, you’ll get
aditional useful adapters including:

* [AAF](https://github.com/OpenTimelineIO/otio-aaf-adapter)
* [ale](https://github.com/OpenTimelineIO/otio-ale-adapter)
* [burnins](https://github.com/OpenTimelineIO/otio-burnins-adapter)
* [cmx\_3600](https://github.com/OpenTimelineIO/otio-cmx3600-adapter)
* [fcp\_xml](https://github.com/OpenTimelineIO/otio-fcp-adapter)
* [fcpx\_xml](https://github.com/OpenTimelineIO/otio-fcpx-xml-adapter)
* [hls\_playlist](https://github.com/OpenTimelineIO/otio-hls-playlist-adapter)
* [maya\_sequencer](https://github.com/OpenTimelineIO/otio-maya-sequencer-adapter)
* [svg](https://github.com/OpenTimelineIO/otio-svg-adapter)
* [xges](https://github.com/OpenTimelineIO/otio-xges-adapter)

These adapters are supported by the broader OpenTimelineIO community. While the
OTIO core team consults and sometimes contribute to their development, they may
be maintained and supported at varying levels.


## Additional Adapters[¶](#additional-adapters "Permalink to this heading")

Below are some other adapters that may be useful to some users:

* [kdenlive](https://invent.kde.org/multimedia/kdenlive-opentimelineio)


## Custom Adapters[¶](#custom-adapters "Permalink to this heading")

Adapters are implemented as plugins for OpenTimelineIO and can either be
registered via an [environment variable](otio-env-variables.html) or by
packaging in a Python module with a particular entrypoint defined. For more
detail, see the [Writing an OTIO Adapter](write-an-adapter.html) tutorial.

---



## Page 13: Opentimelineio.Hooks.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.hooks.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.hooks.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.hooks
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.hooks.rst)


# opentimelineio.hooks[¶](#module-opentimelineio.hooks "Permalink to this heading")

HookScripts are plugins that run at defined points (“Hooks”).

They expose a `hook_function` with signature:

opentimelineio.hooks.hook\_function(*timeline: [opentimelineio.schema.Timeline](opentimelineio.schema.html#opentimelineio.schema.Timeline "opentimelineio.schema.Timeline")*, *optional\_argument\_dict: [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)"), Any]*) → [opentimelineio.schema.Timeline](opentimelineio.schema.html#opentimelineio.schema.Timeline "opentimelineio.schema.Timeline")

Hook function signature

Both hook scripts and the hooks they attach to are defined in the plugin
manifest.

Multiple scripts can be attached to a hook. They will be executed in list order,
first to last.

They are defined by the manifests
[`HookScript`](#opentimelineio.hooks.HookScript

"opentimelineio.hooks.HookScript")s and hooks areas.

```
{
    "OTIO_SCHEMA" : "PluginManifest.1",
    "hook_scripts" : [
        {
            "OTIO_SCHEMA" : "HookScript.1",
            "name" : "example hook",
            "filepath" : "example.py"
        }
    ],
    "hooks" : {
        "pre_adapter_write" : ["example hook"],
        "post_adapter_read" : []
    }
}

```

The `hook_scripts` area loads the python modules with the `hook_function`s to
call in them. The `hooks` area defines the hooks (and any associated scripts).
You can further query and modify these from python.

```
import opentimelineio as otio
hook_list = otio.hooks.scripts_attached_to("some_hook") # -> ['a','b','c']


# to run the hook scripts:

otio.hooks.run("some_hook", some_timeline, optional_argument_dict)

```

This will pass (some\_timeline, optional\_argument\_dict) to `a`, which will a
new timeline that will get passed into `b` with `optional_argument_dict`, etc.

To edit the order, change the order in the list:

```
hook_list[0], hook_list[2] = hook_list[2], hook_list[0]
print hook_list # ['c','b','a']

```

Now `c` will run, then `b`, then `a`.

To delete a function the list:

```
del hook_list[1]

```

*class* opentimelineio.hooks.HookScript[¶](#opentimelineio.hooks.HookScript "Permalink to this definition")run(*in\_timeline*, *argument\_map={}*)[¶](#opentimelineio.hooks.HookScript.run "Permalink to this definition")

Run the hook\_function associated with this plugin.

opentimelineio.hooks.available\_hookscript\_names()[¶](#opentimelineio.hooks.available_hookscript_names "Permalink to this definition")

Return the names of HookScripts that have been registered.

opentimelineio.hooks.available\_hookscripts()[¶](#opentimelineio.hooks.available_hookscripts "Permalink to this definition")

Return the HookScripts objects that have been registered.

opentimelineio.hooks.names()[¶](#opentimelineio.hooks.names "Permalink to this definition")

Return a list of all the registered hooks.

opentimelineio.hooks.run(*hook*, *tl*, *extra\_args=None*)[¶](#opentimelineio.hooks.run "Permalink to this definition")

Run all the scripts associated with hook, passing in tl and extra\_args.

Will return the return value of the last hook script.

If no hookscripts are defined, returns tl.

opentimelineio.hooks.scripts\_attached\_to(*hook*)[¶](#opentimelineio.hooks.scripts_attached_to "Permalink to this definition")

Return an editable list of all the hook scripts that are attached to the
specified hook, in execution order. Changing this list will change the order
that scripts run in, and deleting a script will remove it from executing

---



## Page 14: Opentimelineio.Exceptions.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.exceptions.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.exceptions.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.exceptions
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.exceptions.rst)


# opentimelineio.exceptions[¶](#module-opentimelineio.exceptions "Permalink to this heading")

Exception classes for OpenTimelineIO

*exception* opentimelineio.exceptions.AdapterDoesntSupportFunctionError[¶](#opentimelineio.exceptions.AdapterDoesntSupportFunctionError "Permalink to this definition")*exception* opentimelineio.exceptions.CannotComputeAvailableRangeError[¶](#opentimelineio.exceptions.CannotComputeAvailableRangeError "Permalink to this definition")*exception* opentimelineio.exceptions.CannotTrimTransitionsError[¶](#opentimelineio.exceptions.CannotTrimTransitionsError "Permalink to this definition")*exception* opentimelineio.exceptions.CouldNotReadFileError[¶](#opentimelineio.exceptions.CouldNotReadFileError "Permalink to this definition")*exception* opentimelineio.exceptions.InstancingNotAllowedError[¶](#opentimelineio.exceptions.InstancingNotAllowedError "Permalink to this definition")*exception* opentimelineio.exceptions.InvalidSerializableLabelError[¶](#opentimelineio.exceptions.InvalidSerializableLabelError "Permalink to this definition")*exception* opentimelineio.exceptions.MisconfiguredPluginError[¶](#opentimelineio.exceptions.MisconfiguredPluginError "Permalink to this definition")*exception* opentimelineio.exceptions.NoDefaultMediaLinkerError[¶](#opentimelineio.exceptions.NoDefaultMediaLinkerError "Permalink to this definition")*exception* opentimelineio.exceptions.NoKnownAdapterForExtensionError[¶](#opentimelineio.exceptions.NoKnownAdapterForExtensionError "Permalink to this definition")*exception* opentimelineio.exceptions.NotAChildError[¶](#opentimelineio.exceptions.NotAChildError "Permalink to this definition")*exception* opentimelineio.exceptions.NotSupportedError[¶](#opentimelineio.exceptions.NotSupportedError "Permalink to this definition")*exception* opentimelineio.exceptions.OTIOError[¶](#opentimelineio.exceptions.OTIOError "Permalink to this definition")*exception* opentimelineio.exceptions.ReadingNotSupportedError[¶](#opentimelineio.exceptions.ReadingNotSupportedError "Permalink to this definition")*exception* opentimelineio.exceptions.TransitionFollowingATransitionError[¶](#opentimelineio.exceptions.TransitionFollowingATransitionError "Permalink to this definition")*exception* opentimelineio.exceptions.UnsupportedSchemaError[¶](#opentimelineio.exceptions.UnsupportedSchemaError "Permalink to this definition")*exception* opentimelineio.exceptions.WritingNotSupportedError[¶](#opentimelineio.exceptions.WritingNotSupportedError "Permalink to this definition")

---



## Page 15: Opentimelineio.Algorithms.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.algorithms
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.algorithms.rst)


# opentimelineio.algorithms[¶](#module-opentimelineio.algorithms "Permalink to this heading")

Algorithms for OTIO objects.

Modules

|  |  |
| --- | --- |
| [`opentimelineio.algorithms.filter`](opentimelineio.algorithms.filter.html#module-opentimelineio.algorithms.filter "opentimelineio.algorithms.filter") | Algorithms for filtering OTIO files. |

| [`opentimelineio.algorithms.stack_algo`](opentimelineio.algorithms.stack_algo.html#module-opentimelineio.algorithms.stack_algo "opentimelineio.algorithms.stack_algo") | Algorithms for stack objects. |

| [`opentimelineio.algorithms.timeline_algo`](opentimelineio.algorithms.timeline_algo.html#module-opentimelineio.algorithms.timeline_algo "opentimelineio.algorithms.timeline_algo") | Algorithms for timeline objects. |

| [`opentimelineio.algorithms.track_algo`](opentimelineio.algorithms.track_algo.html#module-opentimelineio.algorithms.track_algo "opentimelineio.algorithms.track_algo") | Algorithms for track objects. |

---



## Page 16: Opentimelineio.Test Utils.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.test_utils.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.test_utils.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.test\_utils
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.test_utils.rst)


# opentimelineio.test\_utils[¶](#module-opentimelineio.test_utils "Permalink to this heading")

Utility assertions for OTIO Unit tests.

*class* opentimelineio.test\_utils.OTIOAssertions[¶](#opentimelineio.test_utils.OTIOAssertions "Permalink to this definition")assertIsOTIOEquivalentTo(*known*, *test\_result*)[¶](#opentimelineio.test_utils.OTIOAssertions.assertIsOTIOEquivalentTo "Permalink to this definition")

Test using the ‘is equivalent to’ method on SerializableObject

assertJsonEqual(*known*, *test\_result*)[¶](#opentimelineio.test_utils.OTIOAssertions.assertJsonEqual "Permalink to this definition")

Convert to json and compare that (more readable).

---



## Page 17: Otio File Format Specification.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-file-format-specification.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-file-format-specification.html)

* File Format Specification
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/otio-file-format-specification.md)


# File Format Specification[¶](#file-format-specification "Permalink to this heading")


## Version[¶](#version "Permalink to this heading")

This DRAFT describes the OpenTimelineIO JSON File Format as of OTIO Beta 13.


## Note[¶](#note "Permalink to this heading")

It is strongly recommended that everyone use the OpenTimelineIO library to read
and write OTIO files instead of implementing a separate parser or writer.


## Naming[¶](#naming "Permalink to this heading")

OpenTimelineIO files should have a `.otio` path extension. Please do not use
`.json` to name OTIO files.


## Contents[¶](#contents "Permalink to this heading")

OpenTimelineIO files are serialized as JSON (http://www.json.org).


### Number Types[¶](#number-types "Permalink to this heading")

Supported number types:

* integers: `int64_t` (signed 64 bit integer)
* floating point numbers: `double` (IEEE754 64 bit signed floating point number)

In addition to the basic JSON spec, OTIO allows the following values for
doubles:

* `NaN` (not a number)
* `Inf`, `Infinity` (positive infinity)
* `-Inf, -Infinity (negative infinity)


## Structure[¶](#structure "Permalink to this heading")

An OTIO file is a tree structure of nested OTIO objects. Each OTIO object is
stored as a JSON dictionary with member fields, each of which may contain simple
data types or nested OTIO objects.

OTIO does not support instancing, there cannot be references the same object
multiple times in the tree structure. If the same clip or media appears multiple
times in a timeline, it will appear as identical copies of the Clip or
MediaReference object.

The top level object in an OTIO file can be any OTIO data type, but is typically
a Timeline. This means that most use cases will assume that the top level object
is a Timeline, but in specific workflows, otio files can be read or written that
contain just a Clip, Track, RationalTime, or any other OTIO data type. Due to
the nature of JSON, arrays of objects can also be read/written, but it is better
to use the OTIO SerializableCollection data type in this case so that metadata
can be attached to the container itself. Code that reads an OTIO file should
guard against unexpected top level types and fail gracefully. Note also, that
this is the reason that there is no top level file format version in OTIO. Each
data type has a version instead to allow for more granular versioning.

Each OTIO object has an `"OTIO_SCHEMA"` key/value pair that identifies the OTIO
data type and version of that type. For example `"OTIO_SCHEMA": "Timeline.1"` or
`"OTIO_SCHEMA": "Clip.5"`. This allows future versions of OTIO to change the
serialization details of each data type independently and introduce new data
types over time. (TODO: Link to discussion on schema versioning.)

Member fields of each data type are encoded as key/value pairs in the containing
object’s dictionary. The value of each key can be a JSON string, number, list,
or dictionary. If the value is a dictionary, then it will often be an OTIO data
type. In some cases (specifically metadata) it can be a regular JSON dictionary.

OTIO JSON files are typically formatted with indentation to make them easier to
read. This makes the files slightly larger, but dramatically improves human
readability which makes debugging much easier. Furthermore, the OTIO library
will write the keys of each object in a predictable order to help with change
tracking, comparisons, etc.

Since human readablility and ease of use are explicit goals of the
OpenTimelineIO project, it is recommended that OTIO JSON not be minified unless
absolutely necessary. If a minimum file size is desired, the recommendation is
to use gzip rather than minifying.


## Nesting[¶](#nesting "Permalink to this heading")

A Timeline has one child, called “tracks” which is a Stack. Each of that Stack’s
children is a Track. From there on down each child can be any of these types:
Clip, Filler, Stack, Track.

In a simple case with one track of 3 clips:

```
Timeline "my timeline"
  Stack "tracks"
    Track "video track"
      Clip "intro"
      Clip "main"
      Clip "credits"

```

In order to make the tree structure easy to traverse, OTIO uses the name
“children” for the list of child objects in each parent (except for Timeline’s
“tracks”).


## Metadata[¶](#metadata "Permalink to this heading")

Timeline, Stack, Track, Clip, MediaReferece, and most other OTIO objects all
have a `metadata` property. This metadata property holds a dictionary of
key/value pairs which may be deeply nested, and may hold any variety of
JSON-compatible data types (numbers, booleans, strings, arrays, dictionaries) as
well as any other OTIO objects.

This is intended to be a place to put information that does not fit into the
schema defined properties. The core of OTIO doesn’t do anything with this
metadata, it only carries it along so that adapters, scripts, applications, or
other workflows can use that metadata however needed. For example, several of
the adapters shipped with OTIO use metadata to store information that doesn’t
(yet) fit into the core OTIO schema.

Due to the fact that many different workflows can and will use metadata, it is
important to group metadata inside namespaces so that independent workflows can
coexist without encountering name collisions. In the example below, there is
metadata on the Timeline and on several Clips for both a hypothetical
`my_playback_tool` and `my_production_tracking_system` that could coexist with
anything else added under a different namespace.

Metadata can also be useful when prototyping new OTIO schemas. An existing
object can be extended with metadata which can later be migrated into a new
schema version, or a custom schema defined in a [SchemaDef
plugin](write-a-schemadef.html).


## Example:[¶](#example "Permalink to this heading")

```
{
    "OTIO_SCHEMA": "Timeline.1",
    "metadata": {
        "my_playback_tool": {
            "metadata_overlay": "full_details",
            "loop": false
        },
        "my_production_tracking_system": {
            "purpose": "dailies",
            "presentation_date": "2020-01-01",
            "owner": "rose"
        }
    },
    "name": "transition_test",
    "tracks": {
        "OTIO_SCHEMA": "Stack.1",
        "children": [
            {
                "OTIO_SCHEMA": "Track.1",
                "children": [
                    {
                        "OTIO_SCHEMA": "Transition.1",
                        "metadata": {},
                        "name": "t0",
                        "transition_type": "SMPTE_Dissolve",
                        "parameters": {},
                        "in_offset": {
                            "OTIO_SCHEMA" : "RationalTime.1",
                            "rate" : 24,
                            "value" : 10
                        },
                        "out_offset": {
                            "OTIO_SCHEMA" : "RationalTime.1",
                            "rate" : 24,
                            "value" : 10
                        }
                    },
                    {
                        "OTIO_SCHEMA": "Clip.1",
                        "effects": [],
                        "markers": [],
                        "media_reference": null,
                        "metadata": {
                            "my_playback_tool": {
                                "tags": ["for_review", "nightly_render"],
                            },
                            "my_production_tracking_system": {
                                "status": "IP",
                                "due_date": "2020-02-01",
                                "assigned_to": "rose"
                            }
                        },
                        "name": "A",
                        "source_range": {
                            "OTIO_SCHEMA": "TimeRange.1",
                            "duration": {
                                "OTIO_SCHEMA": "RationalTime.1",
                                "rate": 24,
                                "value": 50
                            },
                            "start_time": {
                                "OTIO_SCHEMA": "RationalTime.1",
                                "rate": 24,
                                "value": 0.0
                            }
                        }

                    },
                    {
                        "OTIO_SCHEMA": "Transition.1",
                        "metadata": {},
                        "name": "t1",
                        "transition_type": "SMPTE_Dissolve",
                        "parameters": {},
                        "in_offset": {
                            "OTIO_SCHEMA" : "RationalTime.1",
                            "rate" : 24,
                            "value" : 10
                        },
                        "out_offset": {
                            "OTIO_SCHEMA" : "RationalTime.1",
                            "rate" : 24,
                            "value" : 10
                        }
                    },
                    {
                        "OTIO_SCHEMA": "Clip.1",
                        "effects": [],
                        "markers": [],
                        "media_reference": null,
                        "metadata": {
                            "my_playback_tool": {
                                "tags": ["for_review", "nightly_render"],
                            },
                            "my_production_tracking_system": {
                                "status": "IP",
                                "due_date": "2020-02-01",
                                "assigned_to": "rose"
                            }
                        },
                        "name": "B",
                        "source_range": {
                            "OTIO_SCHEMA": "TimeRange.1",
                            "duration": {
                                "OTIO_SCHEMA": "RationalTime.1",
                                "rate": 24,
                                "value": 50
                            },
                            "start_time": {
                                "OTIO_SCHEMA": "RationalTime.1",
                                "rate": 24,
                                "value": 0.0
                            }
                        }

                    },
                    {
                        "OTIO_SCHEMA": "Clip.1",
                        "effects": [],
                        "markers": [],
                        "media_reference": null,
                        "metadata": {
                            "my_playback_tool": {
                                "tags": [],
                            },
                            "my_production_tracking_system": {
                                "status": "final",
                                "due_date": "2020-01-01",
                                "assigned_to": null
                            }
                        },
                        "name": "C",
                        "source_range": {
                            "OTIO_SCHEMA": "TimeRange.1",
                            "duration": {
                                "OTIO_SCHEMA": "RationalTime.1",
                                "rate": 24,
                                "value": 50
                            },
                            "start_time": {
                                "OTIO_SCHEMA": "RationalTime.1",
                                "rate": 24,
                                "value": 0.0
                            }
                        }

                    },
                    {
                        "OTIO_SCHEMA": "Transition.1",
                        "metadata": {},
                        "name": "t3",
                        "transition_type": "SMPTE_Dissolve",
                        "parameters": {},
                        "in_offset": {
                            "OTIO_SCHEMA" : "RationalTime.1",
                            "rate" : 24,
                            "value" : 10
                        },
                        "out_offset": {
                            "OTIO_SCHEMA" : "RationalTime.1",
                            "rate" : 24,
                            "value" : 10
                        }
                    }

                ],
                "effects": [],
                "kind": "Video",
                "markers": [],
                "metadata": {},
                "name": "Track1",
                "source_range": null
            }
        ],
        "effects": [],
        "markers": [],
        "metadata": {},
        "name": "tracks",
        "source_range": null
    }
}

```


## Schema Specification[¶](#schema-specification "Permalink to this heading")

To see an autogenerated documentation of the serialized types and their fields,
see this: [Autogenerated Serialized File Format](otio-serialized-schema.html).

---



## Page 18: Opentimelineio.Versioning.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.versioning.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.versioning.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.versioning
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.versioning.rst)


# opentimelineio.versioning[¶](#module-opentimelineio.versioning "Permalink to this heading")

Tools for fetching the family->label->schema:version maps

opentimelineio.versioning.fetch\_map(*family*, *label*)[¶](#opentimelineio.versioning.fetch_map "Permalink to this definition")

Fetch the version map for the given family and label. OpenTimelineIO includes a
built in family called “OTIO\_CORE”, this is compiled into the C++ core and
represents the core interchange schemas of OpenTimelineIO.

Users may define more family/label/schema:version mappings by way of the version
manifest plugins.

Returns a dictionary mapping Schema name to schema version, like:

```
{
    "Clip": 2,
    "Timeline": 1,
    ...
}

```

Parameters:

* **family** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

  Python v3.12)")) – family of labels (ie: “OTIO\_CORE”)
* **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

  Python v3.12)")) – label of schema-version map (ie: “0.15.0”)
Returns:

a dictionary mapping Schema name to schema version

Return type:

[dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python

v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python

v3.12)"), [int](https://docs.python.org/3/library/functions.html#int "(in Python

v3.12)")]

opentimelineio.versioning.full\_map()[¶](#opentimelineio.versioning.full_map "Permalink to this definition")

Return the full map of schema version sets, including core and plugins.
Organized as follows:

```
{
    "FAMILY_NAME": {
        "LABEL": {
            "SchemaName": schemaversion,
            "Clip": 2,
            "Timeline": 3,
            ...
        }
    }
}

```

The “OTIO\_CORE” family is always provided and represents the built in schemas
defined in the C++ core. IE:

```
{
    "OTIO_CORE": {
        "0.15.0": {
            "Clip": 2,
            ...
        }
    }
}

```

Returns:

full map of schema version sets, including core and plugins

Return type:

[dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python

v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python

v3.12)"), [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in

Python v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in

Python v3.12)"), [dict](https://docs.python.org/3/library/stdtypes.html#dict

"(in Python v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str

"(in Python v3.12)"), [int](https://docs.python.org/3/library/functions.html#int

"(in Python v3.12)")]]]

---



## Page 19: Opentimelineio.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.html)

* [Python](../../python_reference.html)
* opentimelineio
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.rst)


# opentimelineio[¶](#module-opentimelineio "Permalink to this heading")

An editorial interchange format and library.

see: <http://opentimeline.io>

Modules

|  |  |
| --- | --- |
| [`opentimelineio.adapters`](opentimelineio.adapters.html#module-opentimelineio.adapters "opentimelineio.adapters") | Expose the adapter interface to developers. |

| [`opentimelineio.algorithms`](opentimelineio.algorithms.html#module-opentimelineio.algorithms "opentimelineio.algorithms") | Algorithms for OTIO objects. |

| [`opentimelineio.console`](opentimelineio.console.html#module-opentimelineio.console "opentimelineio.console") | Console scripts for OpenTimelineIO |

| [`opentimelineio.core`](opentimelineio.core.html#module-opentimelineio.core "opentimelineio.core") | Core implementation details and wrappers around the C++ library |

| [`opentimelineio.exceptions`](opentimelineio.exceptions.html#module-opentimelineio.exceptions "opentimelineio.exceptions") | Exception classes for OpenTimelineIO |

| [`opentimelineio.hooks`](opentimelineio.hooks.html#module-opentimelineio.hooks "opentimelineio.hooks") | HookScripts are plugins that run at defined points ("Hooks"). |

| [`opentimelineio.media_linker`](opentimelineio.media_linker.html#module-opentimelineio.media_linker "opentimelineio.media_linker") | MediaLinker plugins fire after an adapter has read a file in order to produce [`MediaReference`](opentimelineio.core.html#opentimelineio.core.MediaReference "opentimelineio.core.MediaReference")s that point at valid, site specific media. |

| [`opentimelineio.opentime`](opentimelineio.opentime.html#module-opentimelineio.opentime "opentimelineio.opentime") |  |

| [`opentimelineio.plugins`](opentimelineio.plugins.html#module-opentimelineio.plugins "opentimelineio.plugins") | Plugin system for OTIO |

| [`opentimelineio.schema`](opentimelineio.schema.html#module-opentimelineio.schema "opentimelineio.schema") | User facing classes. |

| [`opentimelineio.schemadef`](opentimelineio.schemadef.html#module-opentimelineio.schemadef "opentimelineio.schemadef") |  |

| [`opentimelineio.test_utils`](opentimelineio.test_utils.html#module-opentimelineio.test_utils "opentimelineio.test_utils") | Utility assertions for OTIO Unit tests. |

| [`opentimelineio.url_utils`](opentimelineio.url_utils.html#module-opentimelineio.url_utils "opentimelineio.url_utils") | Utilities for conversion between urls and file paths |

| [`opentimelineio.versioning`](opentimelineio.versioning.html#module-opentimelineio.versioning "opentimelineio.versioning") | Tools for fetching the family->label->schema:version maps |

---



## Page 20: Opentimelineio.Plugins.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.plugins.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.plugins.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.plugins
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.plugins.rst)


# opentimelineio.plugins[¶](#module-opentimelineio.plugins "Permalink to this heading")

Plugin system for OTIO

Modules

|  |  |
| --- | --- |
| [`opentimelineio.plugins.manifest`](opentimelineio.plugins.manifest.html#module-opentimelineio.plugins.manifest "opentimelineio.plugins.manifest") | OTIO Python Plugin Manifest system: locates plugins to OTIO. |

| [`opentimelineio.plugins.python_plugin`](opentimelineio.plugins.python_plugin.html#module-opentimelineio.plugins.python_plugin "opentimelineio.plugins.python_plugin") | Base class for OTIO plugins that are exposed by manifests. |

---



## Page 21: Write A Schemadef.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/write-a-schemadef.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/write-a-schemadef.html)

* Writing an OTIO SchemaDef Plugin
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/write-a-schemadef.md)


# Writing an OTIO SchemaDef Plugin[¶](#writing-an-otio-schemadef-plugin "Permalink to this heading")

OpenTimelineIO SchemaDef plugins are plugins that define new schemas within the
otio type registry system. You might want to do this to add new schemas that are
specific to your own internal studio workflow and shouldn’t be part of the
generic OpenTimelineIO package.

To write a new SchemaDef plugin, you create a Python source file that defines
and registers one or more new classes subclassed from
`otio.core.SerializeableObject`. Multiple schema classes can be defined and
registered in one plugin, or you can use a separate plugin for each of them.

Here’s an example of defining a very simple class called `MyThing`:

```
import opentimelineio as otio

@otio.core.register_type
class MyThing(otio.core.SerializableObject):
    """A schema for my thing."""

    _serializable_label = "MyThing.1"
    _name = "MyThing"

    def __init__(
        self,
        arg1=None,
        argN=None
    ):
        otio.core.SerializableObject.__init__(self)
        self.arg1 = arg1
        self.argN = argN

    arg1 = otio.core.serializable_field(
        "arg1",
        doc = ( "arg1's doc string")
    )

    argN = otio.core.serializable_field(
        "argN",
        doc = ( "argN's doc string")
    )

    def __str__(self):
        return "MyThing({}, {})".format(
            repr(self.arg1),
            repr(self.argN)
        )

    def __repr__(self):
        return "otio.schema.MyThing(arg1={}, argN={})".format(
            repr(self.arg1),
            repr(self.argN)
        )

```

In the example, the `MyThing` class has two parameters `arg1` and `argN`, but
your schema class could have any number of parameters as needed to contain the
data fields you want to have in your class.

One or more class definitions like this one can be included in a plugin source
file, which must then be added to the plugin manifest as shown below.


## Registering Your SchemaDef Plugin[¶](#registering-your-schemadef-plugin "Permalink to this heading")

To create a new SchemaDef plugin, you need to create a Python source file as
shown in the example above. Let’s call it `mything.py`. Then you must add it to
a plugin manifest:

```
{
    "OTIO_SCHEMA" : "PluginManifest.1",
    "schemadefs" : [
        {
            "OTIO_SCHEMA" : "SchemaDef.1",
            "name" : "mything",
            "filepath" : "mything.py"
         }
    ]
}

```

The same plugin manifest may also include adapters and media linkers, if
desired.

Then you need to add this manifest to your
[OTIO\_PLUGIN\_MANIFEST\_PATH](otio-env-variables.html#term-OTIO_PLUGIN_MANIFEST_PATH)

environment variable.


## Using the New Schema in Your Code[¶](#using-the-new-schema-in-your-code "Permalink to this heading")

Now that we’ve defined a new otio schema, how can we create an instance of the
schema class in our code (for instance, in an adapter or media linker)?

SchemaDef plugins are loaded in a deferred way. The load is triggered either by
reading a file that contains the schema or by manually asking the plugin for its
module object. For example, if you have a `my_thing` schemadef module:

```
import opentimelineio as otio

my_thing = otio.schema.schemadef.module_from_name('my_thing')

```

Once the plugin has been loaded, SchemaDef plugin modules are magically inserted
into a namespace called `otio.schemadef`, so you can create a class instance
just like this:

```
import opentimelineio as otio

mine = otio.schemadef.my_thing.MyThing(arg1, argN)

```

An alternative approach is to use the `instance_from_schema` mechanism, which
requires that you create and provide a dict of the parameters:

```
    mything = otio.core.instance_from_schema("MyThing", 1, {
        "arg1": arg1,
        "argN": argN
    })

```

This `instance_from_schema` approach has the added benefit of calling the schema
upgrade function to upgrade the parameters in the case where the requested
schema version is earlier than the current version defined by the schemadef
plugin. This seems rather unlikely to occur in practice if you keep your code
up-to-date, so the first technique of creating the class instance directly from
`otio.schemadef` is usually preferred.

---



## Page 22: Conform New Renders Into Cut.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/use-cases/conform-new-renders-into-cut.html](https://opentimelineio.readthedocs.io/en/stable/use-cases/conform-new-renders-into-cut.html)

* Conform New Renders Into The Cut
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/use-cases/conform-new-renders-into-cut.md)


# Conform New Renders Into The Cut[¶](#conform-new-renders-into-the-cut "Permalink to this heading")

**Status: Done** This use case is in active use at several feature film
production studios.


## Summary[¶](#summary "Permalink to this heading")

Artists working on the animation or visual effects for shots in a sequence often
want to view their in-progress work in the context of a current cut of the film.
This could be accomplished by importing their latest renders into the editing
system, but that often involves many steps (e.g. transcoding, cutting the clips
into the editing system, etc.) Instead, the artists would like to preview the
cut with their latest work spliced in at their desk.


## Workflow[¶](#workflow "Permalink to this heading")

* In Editorial:

1. Export an EDL from the editorial system (Media Composer, Adobe Premiere, Final
   Cut Pro X, etc.)
2. Export a QuickTime audio/video mixdown that matches that EDL
3. Send the EDL+ QuickTime to the animators or visual effects artists

* At the Artist’s Desk:

1. Open the EDL+QuickTime in a video player tool (RV, etc.)
2. Either: 2a. Use OpenTimelineIO to convert the EDL to OTIO or 2b. A plugin in the
   video player tool uses OpenTimelineIO to read the EDL.
3. In either case, we link the shots in the timeline to segments of the supplied
   QuickTime movie.
4. The artist can now play the sequence and see exactly what the editor saw.
5. The artist can now relink any or all of the shots to the latest renders (either
   via OpenTimelineIO or features of the video player tool)

---



## Page 23: Time Ranges.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/time-ranges.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/time-ranges.html)

* Time Ranges
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/time-ranges.md)


# Time Ranges[¶](#time-ranges "Permalink to this heading")


## Overview[¶](#overview "Permalink to this heading")

A Timeline and all of the Tracks and Stacks it contains work together to place
the Clips, Gaps and Transitions relative to each other in time. You can think of
this as a 1-dimensional coordinate system. Simple cases of assembling Clips into
a Track will lay the Clips end-to-end, but more complex cases involve nesting,
cross-dissolves, trimming, and speed-up/slow-down effects which can lead to
confusion. In an attempt to make this easy to work with OpenTimelineIO uses the
following terminology and API for dealing with time ranges.

Note: You probably also want to refer to [Timeline
Structure](otio-timeline-structure.html).


## Clips[¶](#clips "Permalink to this heading")

There are several ranges you might want from a Clip. For each of these, it is
important to note which time frame (the 1-dimensional coordinate system of time)
the range is relative to. We call these the “Clip time frame” and the “parent
time frame” (usually the Clip’s parent Track).


### Ranges within the Clip and its media:[¶](#ranges-within-the-clip-and-its-media "Permalink to this heading")


#### `Clip.available_range()`[¶](#clip-available-range "Permalink to this heading")

The `available_range()` method on Clip returns a TimeRange that tells you how
much media is available via the Clip’s `media_reference`. If a Clip points to a
movie file on disk, then this should tell you how long that movie is and what
timecode it starts at. For example: “wedding.mov” starts at timecode 01:00:00:00
and is 30 minutes long.

Note that `available_range()` may return `None` if the range is not known.


#### `Clip.source_range`[¶](#clip-source-range "Permalink to this heading")

Setting the `source_range` property on a Clip will trim the Clip to only that
range of media.

The `source_range` is specified in the Clip time frame.

Note that `source_range` may be `None` indicating that the Clip should use the
full `available_range()` whatever that may be. If both `source_range` and
`available_range()` are `None`, then the Clip is invalid. You need at least one
of those.

Usually this will be a shorter segment than the `available_range()` but this is
not a hard constraint. Some use cases will intentionally ask for a Clip that is
longer (or starts earlier) than the available media as a way to request that new
media (a newly animated take, or newly recorded audio) be made to fill the
requested `source_range`.


#### `Clip.trimmed_range()`[¶](#clip-trimmed-range "Permalink to this heading")

This will return the Clip’s `source_range` if it is set, otherwise it will
return the `available_range()`. This tells you how long the Clip is meant to be
in its parent Track or Stack.

The `trimmed_range()` is specified in the Clip time frame.


#### `Clip.visible_range()`[¶](#clip-visible-range "Permalink to this heading")

This will return the same thing as `trimmed_range()` but also takes any adjacent
Transitions into account. For example, a Clip that is trimmed to end at frame
10, but is followed by a cross-dissolve with `out_offset` of 5 frames, will have
a `visible_range()` that ends at frame 15.

The `visible_range()` is specified in the Clip time frame.


#### `Clip.duration()`[¶](#clip-duration "Permalink to this heading")

This is the way to ask for the Clip’s “natural” duration. In `oitoview` or most
common non-linear editors, this is the duration of the Clip you will see in the
timeline user interface.

`Clip.duration()` is a convenience for `Clip.trimmed_range().duration()`. If you
want a different duration, then you can ask for
`Clip.available_range().duration()` or `Clip.visible_range().duration()`
explicitly. This makes it clear in your code when you are asking for a different
duration.


### Ranges of the Clip in its parent Track or Stack:[¶](#ranges-of-the-clip-in-its-parent-track-or-stack "Permalink to this heading")


#### `Clip.range_in_parent()`[¶](#clip-range-in-parent "Permalink to this heading")

The answer to this depends on what type is the Clip’s parent. In the typical
case, the Clip is inside a Track, so the `Clip.range_in_parent()` will give you
the range within that Track where this Clip is visible. Each clip within the
Track will have a start time that is directly after the previous clip’s end. So,
given a Track with clipA and clipB in it, this is always true:

* The `range_in_parent()` is specified in the parent time frame.
* `clipA.range_in_parent().end_time_exclusive() ==
  clipB.range_in_parent().start_time`

If the parent is a Stack, then `range_in_parent()` is less interesting. The
start time will always have `.value == 0` and the duration is the Clip’s
duration. This means that the start of each clip in a Stack is aligned. If you
want to shift them around, then use a Stack of Tracks (like the top-level
Timeline has by default) and then you can use Gaps to shift the contents of each
Track around.


#### `Clip.trimmed_range_in_parent()`[¶](#clip-trimmed-range-in-parent "Permalink to this heading")

This is the same as `Clip.range_in_parent()` but trimmed to the *parent*
`source_range`. In most cases the parent has a `source_range` of `None`, so
there is no trimming, but in cases where the parent is trimmed, you may want to
ask where a Clip is relative to the trimmed parent. In cases where the Clip is
completely trimmed by the parent, the `Clip.trimmed_range_in_parent()` will be
`None`.

The `trimmed_range_in_parent()` is specified in the parent time frame.


## Tracks[¶](#tracks "Permalink to this heading")

TODO.


## Markers[¶](#markers "Permalink to this heading")

Markers can be attached to any Item (Clips, Tracks, Stacks, Gaps, etc.)

Each Marker has a `marked_range` which specifies the position and duration of
the Marker relative to the object it is attached to.

The `marked_range` of a Marker on a Clip is in the Clip’s time frame (same as
the Clip’s `source_range`, `trimmed_range()`, etc.)

The `marked_range` of a Marker on a Track is in the Track’s time frame (same as
the Track’s `source_range`, `trimmed_range()`, etc.)

The `marked_range.duration.value` may be 0 if the Marker is meant to be a
instantaneous moment in time, or some other duration if it spans a length of
time.


## Transitions[¶](#transitions "Permalink to this heading")

TODO.


## Gaps[¶](#gaps "Permalink to this heading")

TODO.


## Stacks[¶](#stacks "Permalink to this heading")

TODO.


## Timelines[¶](#timelines "Permalink to this heading")

TODO.

---



## Page 24: Feature Matrix.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/feature-matrix.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/feature-matrix.html)

* Feature Matrix
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/feature-matrix.rst)


# Feature Matrix[¶](#feature-matrix "Permalink to this heading")

Adapters may or may not support all of the features of OpenTimelineIO or the
format they convert to/from. Here is a list of features and which adapters
do/don’t support those features.

| Feature | OTIO | EDL | FCP7 XML | FCP X | AAF | RV | ALE | GStreamer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Single Track of Clips | ✔ | ✔ | ✔ | ✔ | ✔ | W-O | ✔ | ✔ |
| Multiple Video Tracks | ✔ | ✖ | ✔ | ✔ | ✔ | W-O | ✔ | ✔ |
| Audio Tracks & Clips | ✔ | ✔ | ✔ | ✔ | ✔ | W-O | ✔ | ✔ |
| Gap/Filler | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✖ | ✔ |
| Markers | ✔ | ✔ | ✔ | ✔ | ✔ | N/A | ✖ | ✔ |
| Nesting | ✔ | ✖ | ✔ | ✔ | ✔ | W-O | ✔ | ✔ |
| Transitions | ✔ | ✔ | ✖ | ✖ | ✔ | W-O | ✖ | ✔ |
| Audio/Video Effects | ✖ | ✖ | ✖ | ✖ | ✖ | N/A | ✖ | ✔ |
| Linear Speed Effects | ✔ | ✔ | ✖ | ✖ | R-O | ✖ | ✖ | ✖ |
| Fancy Speed Effects | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ |
| Color Decision List | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ | N/A | ✖ |
| Image Sequence Reference | ✔ | ✔ | ✖ | ✖ | ✖ | W-O | ✖ | ✔ |

N/A: Not Applicable W-O: Write Only R-O: Read Only

---



## Page 25: Developing A New Schema.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/developing-a-new-schema.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/developing-a-new-schema.html)

* Schema Proposal and Development Workflow
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/developing-a-new-schema.md)


# Schema Proposal and Development Workflow[¶](#schema-proposal-and-development-workflow "Permalink to this heading")


## Introduction[¶](#introduction "Permalink to this heading")

This document describes a process for proposing and developing a new schema for
the [OpenTimelineIO project](https://opentimeline.io).

The process includes several steps:

* Proposing at a TSC meeting and gathering interested parties for feedback

  + Outlining example JSON
* Implementing and iterating on a branch
* Building support into an adapter as a demonstration
* Incrementing other schemas that are impacted (Eg. Changes to `Clip` to implement
  `Media Multi Reference`


## Examples[¶](#examples "Permalink to this heading")

A number of schemas have been proposed and introduced during OpenTimelineIO’s
development. These include:

* [ImageSequenceReference](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/pull/602)
* [SpatialCoordinates](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/pull/1219)
* [Multi
  media-reference](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/pull/1241)


## Core schema or Plugin?[¶](#core-schema-or-plugin "Permalink to this heading")

OpenTimelineIO has a number of plugin mechanisms, including the
[Schemadef](write-a-schemadef.html). Plugin schemadefs are great for things that
aren’t expected to be useful to the broader community, or are specific to a
particular studio, workflow, or practice. Example of this might be a reference
to a proprietary database or a proprietary effect. They can also be a good place
to prototype a particular schema before proposing it to the community for
adoption.


## Proposal[¶](#proposal "Permalink to this heading")

A proposal can be as fleshed out as a proposed implementation, or as vague as an
idea. Presenting the proposal at a Technical Steering Committee for discussion
is preferred so that interested parties can form a working group if necessary.
The goal of a TSC presentation would be to find view points / impacts that might
not have been considered and advertise the development to the community at
large.

Including an example JSON excerpt which has the fields you think might be needed
can help.

References that are particularly helpful are examples from existing
applications/formats, information about how (or if) the schema participates in
temporal transformations, and other relevant citations.


## Implementing and Iterating on a branch[¶](#implementing-and-iterating-on-a-branch "Permalink to this heading")

Development of schemas typically takes longer and includes more feedback and
review than normal development. To facilitate this, generally the project will
open a branch on the repository so that pull requests can be merged into the
prototype without disturbing the main branch. For example, the
[ImageSequenceReference](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/pull/602)
branch demonstrates that workflow.

A complete implementation should have a:

* C++ core implementation in src/opentimelineio
* python binding in src/py-opentimelineio
* unit tests


### Unit Tests[¶](#unit-tests "Permalink to this heading")

Unit Tests should include a C++ test for the C++ component, a python test for
the python binding, and a baseline test.


#### C++ test[¶](#c-test "Permalink to this heading")

The C++ test should directly test the C++ interface. For examples of that, see
`tests/*.cpp`.


#### Python tests[¶](#python-tests "Permalink to this heading")

The Python test should test the python binding, including any extra ergonomic
conveniences unique to the python implementation (iterators, etc). We use the
`unittest` python library. For examples of this, see: `tests/test_*.py`.


#### Baseline tests[¶](#baseline-tests "Permalink to this heading")

Baseline tests are written in python and are intended to test the serializer.

They include:

* a file named `tests/baselines/empty_<your_schema>.json`, which is the result of
  calling the constructor and then immediately serializing the object:

```
ys = YourSchema()
otio.adapters.write_to_file(ys, "empty_your_schema.json", adapter="otio_json")

```

* a test in `tests/test_json_backend.py` of the form:

```
class TestJsonFormat(unittest.TestCase, otio_test_utils.OTIOAssertions):
    ...
    def test_your_schema(self):
        ys = YourSchema()
        self.check_against_baseline(ys, "empty_your_schema")
    ...

```


## Demo Adapter[¶](#demo-adapter "Permalink to this heading")

Providing an adapter that supports the schema can show how the schema is
translated into another format. For example, the
[ImageSequenceReference](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/pull/722)
used the RV adapter to demonstrate how it could be used by an adapter.


## Incrementing Other Schemas[¶](#incrementing-other-schemas "Permalink to this heading")

Depending on where the schema fits into the overall structure, other schemas
might need to be incremented or changed. For example, the Media multi-reference
caused the clip schema to increment. Considering and implementing this is part
of the implementation. Providing up and downgrade functions ensure backwards and
forwards compatibility.


## Conclusion[¶](#conclusion "Permalink to this heading")

OpenTimelineIO is designed to evolve, and through its schema versioning system
hopes to adapt to changes in the world of timelines and time math. We hope that
working with and on OpenTimelineIO can be a positive, enriching experience for
the community. Thanks for being a part of it!

---



## Page 26: Cxx.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/cxx/cxx.html](https://opentimelineio.readthedocs.io/en/stable/cxx/cxx.html)

* C++ Implementation Details
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/cxx/cxx.rst)


# C++ Implementation Details[¶](#c-implementation-details "Permalink to this heading")


## Dependencies[¶](#dependencies "Permalink to this heading")

The C++ OpentimelineIO (OTIO) library implementation will have the following
dependencies:

> * [rapidjson](https://github.com/Tencent/rapidjson)
> * any (C++ class)
> * optional (C++ class)
> * The C++ Opentime library (see below)

The need for an “optional” (i.e. a container class that holds either no value or
some specific value, for a given type T) is currently small, but does occur in
one key place (schemas which need to hold either a `TimeRange` or indicate their
time range is undefined).

In contrast, the need for an “any” (a C++ type-erased container) is pervasive,
as it is the primary mechanism that serialization and deserialization rest upon.
It is also the bridge to scripting systems like Python that are not strongly
typed. The C++17 standard defines the types `std::optional` and `std::any` and
these types are available in `std::experimental` in some other cases, and our
implementation targets those. However, since many (probably most) sites are not
yet compiling with C++17, our implementation makes available public domain C++11
compliant versions of these types:

> * [any (C++11 compliant)](https://github.com/thelink2012/any/blob/master/any.hpp)
> * [optional (C++11 compliant)](https://github.com/martinmoene/optional-lite)

Support for Python will require [pybind11](https://github.com/pybind/pybind11).

The C++ Opentime library (i.e. `RationalTime`, `TimeRange` and `TimeTransform`)
will have no outside dependencies. In fact, given the current Python
specification, a C++ Opentime API (should) be fairly straightforward and
uncontroversial.

Reminder: these [sample header
files](https://github.com/davidbaraff/OpenTimelineIO/tree/master/proposed-c%2B%2B-api/opentime)
exist only to show the API; namespacing and other niceties are ommitted.


## Starting Examples[¶](#starting-examples "Permalink to this heading")


### Defining a Schema[¶](#defining-a-schema "Permalink to this heading")

Before jumping into specifics, let’s provide some simple examples of what we
anticipate code for defining and using schemas will look like. Consider the
`Marker` schema, which adds a `TimeRange` and a color to a schema which already
defines properties `name` and `metadata`:

```
class Marker : public SerializableObjectWithMetadata {
public:
    struct Schema {
        static std::string constexpr name = "Marker";
        static int constexpr version = 1;
    };

    using Parent = SerializableObjectWithMetadata;

    Marker(std::string const& name = std::string(),
           TimeRange const& marked_range = TimeRange(),
           std::string const& color = std::string("red"),
           AnyDictionary const& metadata = AnyDictionary());

    TimeRange marked_range() const;
    void set_marked_range(TimeRange marked_range);

    std::string const& color() const;
    void set_color(std::string const& color);

protected:
    virtual ~Marker();

    virtual bool read_from(Reader&);
    virtual void write_to(Writer&) const;

private:
    TimeRange _marked_range;
    std::color _color;
};

```

The contructor takes four properties, two of which (`marked_range` and `color`)
are stored directly in `Marker`, with the remaining two (`name` and `metadata`)
handled by the base class `SerializableObjectWithMetadata`.

For the OTIO API, we will write standard getters/setters to access properties;
outside of OTIO, users could adopt this technique or provide other mechanisms
(e.g. public access to member variables, if they like). The supplied Python
binding code will allow users to define their own schemas in Python exactly as
they do today, with no changes required.

The `Schema` structure exists so that this type can be added to the OTIO type
registry with a simple call:

```
TypeRegistry::instance()::register_type<Marker>();

```

The call to add a schema to the type registry would be done within the OTIO
library itself for schemas known to OTIO; for schemas defined outside OTIO, the
author of the schema would need to make the above call for their class early in
a program’s execution.


### Reading/Writing Properties[¶](#reading-writing-properties "Permalink to this heading")

Code must also be written to read/write the new properties. This is simple as
well:

```
bool Marker::read_from(Reader& reader) {
    return reader.read("color", &_color) &&
        reader.read("marked_range", &_marked_range) &&
        Parent::read_from(reader);
 }

void Marker::write_to(Writer& writer) const {
    Parent::write_to(writer);
    writer.write("color", _color);
    writer.write("marked_range", _marked_range);
}

```

Even when we define more complex properties, the reading/writing code is as
simple as shown above, in almost all cases.

When an error is encountered in reading, `read_from` should set the error on the
`Reader` instance and return `false`:

```
bool Marker::read_from(Reader& reader) {
    if (!reader.read(“color”, &_color)) {
        return false;
    }
    if (_color == “invalid_value”) {
        reader.error( ErrorStatus(ErrorStatus::JSON_PARSE_ERROR,
                                                  “invalid_value not allowed for color”));
        return false;
}
    return reader.read(“marked_range”, &_marked_range) &&
        Parent::read_from(reader);
}

```

This is a contrived example but it describes the basic mechanics. Adjust the
details above as appropriate for your case.

Note

Properties are written to the JSON file in the order they are written to from
within `write_to()`. But the reading code need not be in the same order, and
changes in the ordering of either the reading or writing code will not break
compatability with previously written JSON files.

However, it is vital to invoke `Parent::read_from()` *after* reading all of the
derived class properties, while for writing `Parent::write_to()` must be invoked
*before* writing the derived class properties.

Note

Also note that the order of properties within a JSON file for data that is
essentially a `std::map<>` (see `AnyDictionary` below) is always alphebetical by
key. This ensures deterministic JSON file writing which is important for
comparison and testing.


## Using Schemas[¶](#using-schemas "Permalink to this heading")

Creating and manipulating schema objects is also simple:

```
Track* track = new Track();
Clip* clip1 = new Clip("clip1", new ExternalReference("/path/someFile.mov"));
Clip* clip2 = new Clip("clip2");

track->append_child(clip1);
track->append_child(clip2);

...

for (Item* item: track->children()) {
    for (Effect* effect: item->effects()) {
         std::cout << effect->effect_name();
         ...
    }
}

```


## Serializable Data[¶](#serializable-data "Permalink to this heading")

Data in OTIO schemas must be read and written as JSON. Data must also be
available to C++, in some cases as strongly typed data, while in other cases as
untyped data (i.e. presented as an `any`).

For discussion purposes, let us consider that all data that is read and written
to JSON is transported as a C++ `any`. What can that `any` hold?

First, the `any` can be empty, which corresponds with a `null` JSON value. The
`any` could also hold any of the following “atomic” types: `bool`, `int`,
`double`, `std::string`, `RationalTime`, `TimeRange` and `TimeTransform`. All
but the last three are immediately expressable in JSON, while the three Opentime
types are read/written as compound structures with the same format that the
current Python implementation delivers. The final “atomic” type that an `any`
can hold is a `SerializableObject*`, which represents the C++ base class for all
schemas. (Note: it will not be valid for an `any` to hold a pointer to a derived
class, for example, a `Clip*` value. The actual C++ static type in the `any`
will always be a pointer to the base class `SerializableObject`.)

Next, for any of the above atomic types `T`, excepting for
`SerializableObject*`, an `any` can store a type of `optional<T>`. (Supporting
serialization of an `optional<SerializableObject*>` would be ambiguous and
unneeded; putting a null pointer of type `SerializableObject*` in an `any`, is
written as a `null` to the JSON file.)

Finally, the `any` can hold two more types: an `AnyDictionary` and an
`AnyVector`. For this discussion, consider an `AnyDictionary` to be the type
`std::map<std::string, any>` and the type `AnyVector` to be the type
`std::vector<any>`. The actual implementation is subtly different, but not to
end-users: the API for both these types exactly mirrors the APIs of
`std::vector<any>` and `std::map<std::string, any>` respectively. The
`AnyVector` and `AnyDictionary` types are of course the JSON array and object
types.


## C++ Properties[¶](#c-properties "Permalink to this heading")

In most cases, we expect C++ schemas to hold data as strongly-typed properties.
The notable exception is that low in the inheritance hierarchy, a C++ property
named `metadata` which is of type `AnyDictionary` is made available, which
allows clients to story data of any type they want. Manipulating such data will
be as simple as always, from an untyped language like Python, while in
C++/Swift, the typical and necessary querying and casting would need to be
written.

As we saw above, declaring and handling reading/writing for “atomic” property
types (e.g. `std::string`, `TimeRange`) is straightforward and requires little
effort. Additionally, reading/writing support is automatically provided for the
(recursively defined) types `std::vector<P>`, `std::list<P>` and
`std::map<std::string, P>` where `P` is itself a serializable property type.
Accordingly, one is free to declare a property of type
`std::vector<std::map<std::string, std::list<TimeRange>>>` and it will serialize
and deserialize properly. However, such a type might be hard to reflect/bind in
a Python or Swift bridge. Our current implementation however bridges one-level
deep types such as `std::vector<RationalTime>` or `std::map<std::string,
double>` to Python (and later Swift) quite easily and idiomatically.

Finally, one can declare lists and dictionaries for schema objects, in as
strongly typed fashion as required. That is, a property might be a list of
schema objects of any type, or the property might specify a particular derived
class the schema object must satisfy. Again, this is taken care of
automatically:

```
class DerivedSchema : public SerializableObject {
   ...
private:
   std::vector<MediaReference*> _extra_references;   // (don't actually do this)
};

```

In this case, the derived schema could choose to store extra media references.
The reading/writing code would simply call:

```
reader.read("extra_references", &_extra_references)

```

To read the property, and:

```
writer.write("extra_references", _extra_references)

```

To write the property.

Note

The comment “don’t actually do this” will be explained in the next section; the
actual type of this property needs to be slightly different. The code for
reading/writing the property however is correct.


## Object Graphs and Serialization[¶](#object-graphs-and-serialization "Permalink to this heading")

The current Python implementation assumes that no schema object is referenced
more than once, when it comes to serialization and deserialization.
Specifically, the object “graph” is assumed to implicitly be a tree, although
this is not always enforced. For example, the current Python implementation has
this bug:

```
clip1 = otio.schema.Clip("clip1")
clip2 = otio.schema.Clip("clip2")
ext_ref = otio.schema.ExternalReference("/path/someFile.mov")
clip1.media_reference = ext_ref
clip2.media_reference = ext_ref

```

As written, modifying `ext_ref` modifies the external media reference data for
both `clip1` and `clip2`. However, if one serializes and then deserializes this
data, the serialized data replicates the external references. Thus, upon reading
back this object graph, the new clips no longer share the same media reference.

The C++ implementation for serialization will not have this limitation. That
means that the object structure need no longer be a tree; it doesn’t, strictly
speaking, even need to be a DAG:

```
Clip* clip1 = new Clip();
Clip* clip2 = new Clip();

clip1->metadata()["other_clip"] = clip2;
clip2->metadata()["other_clip"] = clip1;

```

This will work just fine: writing/reading or simply cloning `clip1` would yield
a new `clip1` that pointed to a new `clip2` and vice versa.

Note

This really does work, except that it forms an unbreakable retain cycle in
memory that is only broken by manually severing one of the links by removing,
for example, the value under “other\_clip” in one of the metadata dictionaries.

The above example shows what one could (but shouldn’t do). More practical
examples are that clips could now share media references, or that metadata could
contain references to arbitrary schemas for convenience.

Most importantly, arbitrary serialization lets us separate the concepts of “I am
responsible for reading/writing you” from the “I am your (one and only) parent”
from “I am responsible to deleting you when no longer needed.” In the current
Python implementation, these concepts are not explicitly defined, mostly because
of the automatic nature of memory management in Python. In C++, we must be far
more explicit though.


## Memory Management[¶](#memory-management "Permalink to this heading")

The final topic we must deal with is memory management. Languages like Python
and Swift natually make use of reference counted class instances. We considered
such a route in C++, by requiring that manipulations be done not in terms of
`SerializableObject*` pointers, but rather using
`std::shared_ptr<SerializableObject>` (and the corresponding `std::weak_ptr`).
While some end users would find this a comfortable route, there are others who
would not. Additionally (and this is a topic that is very deep, but that we are
happy to discuss further) the `std::shared_ptr<>` route, coupled with the
`pybind` binding system (or even with the older `boost` Python binding system)
wouldn’t provide an adequate end-user experience in Python. (And we would expect
similar difficulties in Swift.)

Consider the following requirements from the perspective of an OTIO user in a
Python framework. In Python, a user types:

```
clip = otio.schema.Clip()

```

Behind the scenes, in C++, an actual `Clip` instance has been created. From the
user’s perspective, they “own” this clip, and if they immediately type:

```
del clip

```

Then they would expect the Python clip object to be destroyed (and the actual
C++ `Clip` instance to be deleted). Anything less than this is a memory leak.

But what if before typing `del clip` the Python user puts that clip into a
composition? Now neither the Python object corresponding to the clip *nor* the
actual C++ `Clip` instance can be destroyed while the composition has that clip
as a child.

The same situation applies if the end user does not create the objects directly
from Python. Reading back a JSON file from Python creates all objects in C++ and
hands back only the top-most object to Python. Yet that object (and any other
objects subsequently exposed and held by Python) must remain undeletable from
C++ while the Python interpreter has a reference to those objects.

It might seem like shared pointers would fix all this but in fact, they do not.
The reason is that there are in reality two objects: the C++ instance, and the
reflected object in Python. (While it might be feasible to “auto-create” the
reflected Python object whenever it was needed, and really think of having one
object, this choice makes it impossible to allow defining new schemas in Python.
The same consequence applies to allowing for new schemas to be defined in
Swift.) Ensuring a system that does not leak memory, and that also keeps both
objects alive as long as either side (C++ or the bridged language) is, simply
put, challenging.

With all that as a preamble, here is our proposed solution for C++:

* A new instance of a schema object is created by a call to `new`. - All schema
  objects have protected destructors. Given a raw pointer to a schema object,
  client code may not directly invoke the `delete` operator, but may write:

  ```
  Clip* c = new Clip();
  ...
  c->possibly_delete();    // returns true if c was deleted

  ```
* The OTIO C++ API uses raw pointers exclusively in all its function signatures
  (e.g. property access functions, property modifier functions, constructors,
  etc.).
* Schema objects prevent premature destruction of schema instances they are
  interested in by storing them in variables of type
  `SerializableObject::Retainer<T>` where `T` is of type `SerializableObject` (or
  derived from it).

For example:

```
 class ExtendedEffect : public Effect {
 public:
    ...
    MediaReference* best() const {
        return _best;
    }

    void set_best(MediaReference* best) {
        _best = best;
    }

    MediaReference* best_or_other() {
        return _best ? _best : some_other_reference();
    }

private:
  Retainer<MediaReference> _best;
};

```

In this example, the `ExtendedEffect` schema has a property named `best` that
must be a `MediaReference`. To indicate that it needs to retain its instance,
the schema stores the property not as a raw pointer, but using the `Retainer`
structure.

Nothing special needs to be done for the reading/writing code, and there is
automatic two-way conversion between `Retainer<MediaReference>` and
`MediaReference*` which keeps the code simple. Even testing if the property is
set (as `best_or_other()` does) is done as if we were using raw pointers.

The implementation of all this works as follow:

* Creating a new schema instance starts the instance with an internal count of 0.
* Putting a schema instance into a `Retainer` object increases the count by 1.
* Destroying the retainer object or reassigning a new instance to it decreases the
  count by 1 of the object if any in the retainer object. If this causes the count
  to reach zero, the schema instance is destroyed.
* The `possibly_delete()` member function of `SerializableObject*` checks that the
  count of the instance is zero, and if so deletes the object in question.
* An `any` instance holding a `SerializableObject*` actually holds a
  `Retainer<SerializableObject>`. That is, blind data safely retains schema
  instances.

The only rules that a developer needs to know is:

* A new instance of a schema object is created by a call to `new`.
* If your class wants to hold onto something, it needs to store it using a
  `Retainer<T>` type.
* If the caller created a schema object (by calling `new`, or equivalently, by
  obtaining the instance via a `deserialize` call) they are responsible for
  calling `possibly_delete()` when they are done with the instance, or by giving
  the pointer to someone else to hold.

In practice, these rules mean that only the “root” of the object graph needs to
be held by a user in C++ to prevent destruction of the entire graph, and that
calling `possibly_delete()` on the root of the graph will cause deletion of the
entire structure (assuming no cyclic references) and/or assuming the root isn’t
currently sitting in the Python interpreter.

We have extensively tested this scheme with Python and written code for all the
defined schema instances that exist so far. The code has proven to be
lightweight and simple to read and write, with few surprises encountered. The
Python experience has been unchanged from the original implementation.


### Examples[¶](#examples "Permalink to this heading")

Here are some examples that illustrate these rules:

```
Track* t = new Track;

Clip* c1 = new Clip;
c1->possibly_delete();    // c1 is deleted

Clip* c2 = new Clip;
t->add_child(c2);
c2->possibly_delete();   // no effect
t->possibly_delete();   // deletes t and c2

```

Here is an example that would lead to a crash:

```
Track* t = new Track;
Clip* c1 = new Clip;
t->add_child(c1);           // t is now responsible for c1
t->remove_child(0);         // t destroyed c1 when it was removed

std::cout << c1->name();    // <crash>

```

To illustrate the above point in a less contrived fashion, consider this
incorrect code:

```
 void remove_at_index(Composition* c, int index) {
 #if DEBUG

     Item* item = c->children()[index];
 #endif

     c->remove_child(index);

 #if DEBUG

     std::cout << "Debug: removed item named " << item->name();
 #endif

}

```

This could crash, because the call to `remove_child()` might have destroyed
`item`. A correct version of this code would be:

```
 void remove_at_index(Composition* c, int index) {
 #if DEBUG

     SerializableObject::Retainer<Item> item = c->children()[index];
 #endif

     c->remove_child(index);

 #if DEBUG

     std::cout << "Debug: removed item named " << item.value->name();
 #endif

}

```

Note

We do not expect the following scenario to arise, but it is certainly possible
to write a function which returns a raw pointer back to the user *and* also
gives them the responsibility for possibly deleting it:

```
Item* remove_and_return_named_item(Composition* c, std::string const& name) {
    auto& children = c->children();
    for (size_t i = 0; i < children.size(); ++i) {
        if (children[i].value->name() == name) {
            SerializableObject::Retainer<Item> r_item(children[i]);
            c->remove_child(i);
            return r_item.take_value();
        }
    }
    return nullptr;
}

```

The raw pointer in a `Retainer` object is accessed via the `value` member. The
call to `take_value()` decrements the reference count of the pointed to object
but does not delete the instance if the count drops to zero. The pointer is
returned to the caller, and the `Retainer` instance sets its internal pointer to
null. Effectively, this delivers a raw pointer back to the caller, while also
giving them the responsibility to try to delete the object if they were the only
remaining owner of the object.


## Error Handling[¶](#error-handling "Permalink to this heading")

The C++ implementation will not make use of C++ exceptions. A function which can
“fail” will indicate this by taking an argument `ErrorStatus* error_status`. The
`ErrorStatus` structure has two members: an enum code and a “details” string. In
some cases, the details string may give more information than the enum code
(e.g. for a missing key the details string would be the missing string) while
for other cases, the details string might simply be a translation of the error
code string (e.g. “method not implemented”).

Here are examples in the proposed API of some “failable” functions:

```
 class SerializableObject {
   ...
   static SerializableObject* from_json_string(std::string const& input, ErrorStatus* error_status);
   ...
   SerializableObject* clone(std::string* err_msg = nullptr) const;
 };

 class Composition {
   ...
   bool set_children(std::vector<Composable*> const& children, ErrorStatus* error_status);

   bool insert_child(int index, Composable* child, ErrorStatus* error_status);

   bool set_child(int index, Composable* child, ErrorStatus* error_status);
   ...
};

```

The `Composition` schema in particular offers multiple failure paths, ranging
from invalid indices, to trying to add children which are already parented in
another composition. Note that the proposed failure mechanism makes it awkward
to allow constructors to “fail” gracefully. Accordingly, a class like
`Composition` doesn’t allow `children` to be passed into its constructor, but
requires a call to `set_children()` after construction. Neither the Python API
(nor the Swift API) would be subject to this limitation.

The OpenTime and OpenTimelineIO libraries both have their own error definitions.
The tables below outline the errors, which python exceptions they raise, and
what their semantic meaning is.

OpenTime Errors[¶](#id1 "Permalink to this table")| Value | Python Exception Type | Meaning |

| --- | --- | --- |
| OK | n/a | No Error |
| INVALID\_TIMECODE\_RATE | `ValueError` | Timecode rate isn’t a valid SMPTE rate |
| INVALID\_TIMECODE\_STRING | `ValueError` | String is not properly formatted SMPTE timecode string |
| TIMECODE\_RATE\_MISMATCH | `ValueError` | Timecode string has a frame number higher than the frame rate |
| INVALID\_TIME\_STRING | `ValueError` |  |
| NEGATIVE\_VALUE | `ValueError` |  |
| INVALID\_RATE\_FOR\_DROP\_FRAME\_TIMECODE | `ValueError` | Timecode rate isn’t valid for SMPTE Drop-Frame Timecode |

OpenTimelineIO error codes[¶](#id2 "Permalink to this table")| Value | Python Exception Type | Meaning |

| --- | --- | --- |
| OK | n/a | No Error |
| NOT\_IMPLEMENTED | `NotImplementedError` | A feature is known but deliberately unimplemented |
| UNRESOLVED\_OBJECT\_REFERENCE | `ValueError` | An object reference is unresolved while reading |
| DUPLICATE\_OBJECT\_REFERENCE | `ValueError` | An object reference is duplicated while reading |
| MALFORMED\_SCHEMA | `ValueError` | The Schema string was invalid |
| JSON\_PARSE\_ERROR | `ValueError` | Malformed JSON encountered when parsing |
| CHILD\_ALREADY\_PARENTED | `ValueError` | Attempted to add a child to a collection when it’s already a member of another collection instance |
|  |  |  |
| FILE\_OPEN\_FAILED | `ValueError` | failed to open file for reading |
| FILE\_WRITE\_FAILED | `ValueError` | failed to open file for writing |
| SCHEMA\_ALREADY\_REGISTERED | `ValueError` |  |
| SCHEMA\_NOT\_REGISTERED | `ValueError` |  |
| SCHEMA\_VERSION\_UNSUPPORTED | `UnsupportedSchemaError` |  |
| KEY\_NOT\_FOUND | `KeyError` | The key used for a mapping doesn’t exist in the collection |
| ILLEGAL\_INDEX | `IndexError` | The collection index is out of bounds |
| TYPE\_MISMATCH | `ValueError` |  |
| INTERNAL\_ERROR | `ValueError` | Internal error (aka this is a bug) |
| NOT\_AN\_ITEM | `ValueError` |  |
| NOT\_A\_CHILD\_OF | `NotAChildError` |  |
| NOT\_A\_CHILD | `NotAChildError` |  |
| NOT\_DESCENDED\_FROM | `NotAChildError` |  |
| CANNOT\_COMPUTE\_AVAILABLE\_RANGE | `CannotComputeAvailableRangeError` |  |
| INVALID\_TIME\_RANGE | `ValueError` |  |
| OBJECT\_WITHOUT\_DURATION | `ValueError` |  |
| CANNOT\_TRIM\_TRANSITION | `ValueError` |  |


## Thread Safety[¶](#thread-safety "Permalink to this heading")

Multiple threads should be able to examine or traverse the same graph of
constructed objects safely. If a thread mutates or makes any modifications to
objects, then only that single thread may do so safely. Moreover, additional
threads could not safely read the objects while the mutation was underway. It is
the responsibility of client code to ensure this however.


## Proposed OTIO C++ Header Files[¶](#proposed-otio-c-header-files "Permalink to this heading")

[Proposed stripped down OTIO C++ header
files](https://github.com/davidbaraff/OpenTimelineIO/tree/sample-c%2B%2B-headers/proposed-c%2B%2B-api/otio).


## Extended Memory Management Discussion[¶](#extended-memory-management-discussion "Permalink to this heading")

There have been a number of questions about the proposed approach which embeds a
reference count in `SerializableObject` and uses a templated wrapper,
`Retainer<>` to manipulate the reference count. This raises the obvious
question, why not simply used `std::shared_ptr<>`? If we only had C++ to deal
with, that would be an obvious choice; however, wrapping to other languages
complicates things.

Here is a deeper discussion of the issues involved.

What makes this complicated is the following set of rules/constraints:

1. If you access a given C++ object X in Python, this creates a Python wrapper
   object instance P which corresponds to X. As long as the C++ object X remains
   alive, P must persist. This is true even if it appears that the Python
   interpreter holds no references to P, because as long as X exists, it could
   always be given back to Python for manipulation.

   In particular, it is not acceptable to destroy P, and then regenerate a new
   instance P2, as if this was the first time X had been exposed to Python. This
   rule is imperative in a world where we can extend the schema hierarchy by
   deriving in Python. (It is also useful to allow Python code to add arbitrary
   dynamic data onto P, in a persistent fashion.)

   Note that using pybind11 with shared pointers in the standard way does *not*
   satisfy this rule: the pybind11/shared pointer approach will happily regenerate
   a new instance P2 for X if Python loses all references to the original P.
2. As long as Python holds a reference to P, corresponding to some C++ object X,
   the C++ object X cannot be deleted, for obvious reasons.
3. Say that C++ `SerializableObject` B is made a child of A. As long as A retains
   B, then B cannot be destroyed. The same holds if C++ code outside OTIO chooses
   to retain particular C++ objects.
4. If a C++ object X exists, and (3) does not hold, then if X is deleted, and a
   Python wrapper instance P corresponding to X exists, then P must be destroyed
   when X is destroyed.

   Consider the implications of this rule in conjunction with rule (2).
5. If a C++ object X wasn’t ever given out to Python, there will be no
   corresponding wrapper instance P for that C++ object. Note however that it may
   be that the C++ object X was created by virtue of a Python wrapper instance P
   being constructed from Python. Until that C++ object X is passed to C++ in some
   way, then X will exist only as long as P does.

How can we satisfy all these contraints, while ensuring we don’t create retain
cycles (which might be fixable with Python garbage collection, but also might
not)? Here is the solution we came up with; if you have an alternate suggestion,
we would be happy to hear it.

Our scheme works as follows:

> * When you create a Python wrapper instance P for a C++ object X, the Python
>   instance P holds within itself a `Retainer<>` which holds X. The existence of
>   that retainer bumps the reference count of the C++ object up by 1.
> * Whenever X’s C++ reference count increases past 1, which means there is at least
>   one C++ `Retainer<>` object in addition to the one in P, a “keep-alive”
>   reference to P is created and held by X. This ensures that P won’t be destroyed
>   even if the Python interpreter appears to lose all references to P, because
>   we’ve hidden one away. (Remember, the C++ object X could always be passed back
>   to Python, and we can’t/don’t want to regenerate a new P corresponding to X.)
> * However, when X’s C++ count reference count drops back to one, then we know that
>   P is now the only reason we are keeping X alive. At this point, the keep-alive
>   reference to P is destroyed. That means that if/when Python loses the last
>   reference to P, we can (and should) allow both P and X to be destroyed. Of
>   course, if X’s reference count bumps up above 1 before that happens, a new
>   keep-alive reference to P would be created.

The tricky part here is the interaction of watching the reference count of C++
objects oscillate from 1 to greater than one, and vice versa. (There is no way
of watching the Python reference count change, and even if we could, the
performance constraints this would be entail would be likely untenable.)

Essentially, we are monitoring changes in whether or not there is a single
unique `Retainer<>` instance pointing to a given C++ object, or multiple such
retainers. We’ve verified with some extremely processor intensive
multi-threading/multi-core tests that our coding of the mutation of the C++
reference count, coupled with creating/destroying the Python keep-alive
references (when necessary) is: leak free, thread-safe, and deadlock free (the
last being tricky, since there is both a mutex in the C++ object X protecting
the reference count and Python keep-alive callback mechanism, as well as a GIL
lock to contend with whenever we actually manipulate Python references).

Our reasons for not considering `std::shared_ptr` as an implementation mechanism
are two-fold. First, we wanted to keep the C++ API simple, and we have opted for
raw C++ pointers in most API functions, with `Retainer<>` objects only as
members of structures/classes where we need to indicate ownership of an object.
However, even if the community opted to use a smart-pointer approach for the
OTIO API, `std::shared_ptr` wouldn’t work (as far as we know), because there is
no facility in it that would let us catch/monitor transitions between reference
count values of one, and greater than one.

We hope this answers questions about why we have chosen our particular
implementation. This is the only solution we have found that satisfies all the
constraints we listed above, and should work with Swift as well. We are very
happy though to hear ideas for different ways to do all of this.

---



## Page 27: Opentimelineio.Schema.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.schema
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.rst)


# opentimelineio.schema[¶](#module-opentimelineio.schema "Permalink to this heading")

User facing classes.

*class* opentimelineio.schema.Box2d → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")[¶](#opentimelineio.schema.Box2d "Permalink to this definition")*class* opentimelineio.schema.Box2d(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")*class* opentimelineio.schema.Box2d(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*, *arg1: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")

Overloaded function.

1. \_\_init\_\_(self: opentimelineio.\_otio.Box2d) -> None
2. \_\_init\_\_(self: opentimelineio.\_otio.Box2d, arg0: opentimelineio.\_otio.V2d)
   -> None
3. \_\_init\_\_(self: opentimelineio.\_otio.Box2d, arg0: opentimelineio.\_otio.V2d,
   arg1: opentimelineio.\_otio.V2d) -> None

center() → [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")[¶](#opentimelineio.schema.Box2d.center "Permalink to this definition")extendBy(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")[¶](#opentimelineio.schema.Box2d.extendBy "Permalink to this definition")extendBy(*arg0: [opentimelineio.\_otio.Box2d](#opentimelineio.schema.Box2d "opentimelineio._otio.Box2d")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")

Overloaded function.

1. extendBy(arg0: opentimelineio.\_otio.V2d) -> None
2. extendBy(arg0: opentimelineio.\_otio.Box2d) -> None
intersects(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.schema.Box2d.intersects "Permalink to this definition")intersects(*arg0: [opentimelineio.\_otio.Box2d](#opentimelineio.schema.Box2d "opentimelineio._otio.Box2d")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")

Overloaded function.

1. intersects(arg0: opentimelineio.\_otio.V2d) -> bool
2. intersects(arg0: opentimelineio.\_otio.Box2d) -> bool
*property* max[¶](#opentimelineio.schema.Box2d.max "Permalink to this definition")*property* min[¶](#opentimelineio.schema.Box2d.min "Permalink to this definition")*class* opentimelineio.schema.Clip(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *media\_reference: [opentimelineio.\_otio.MediaReference](opentimelineio.core.html#opentimelineio.core.MediaReference "opentimelineio._otio.MediaReference") = None*, *source\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *active\_media\_reference: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = 'DEFAULT\_MEDIA'*)[¶](#opentimelineio.schema.Clip "Permalink to this definition")

A [`Clip`](#opentimelineio.schema.Clip "opentimelineio.schema.Clip") is a

segment of editable media (usually audio or video).

Contains a
[`MediaReference`](opentimelineio.core.html#opentimelineio.core.MediaReference

"opentimelineio.core.MediaReference") and a trim on that media reference.

DEFAULT\_MEDIA\_KEY *= 'DEFAULT\_MEDIA'*[¶](#opentimelineio.schema.Clip.DEFAULT_MEDIA_KEY "Permalink to this definition")*property* active\_media\_reference\_key[¶](#opentimelineio.schema.Clip.active_media_reference_key "Permalink to this definition")find\_clips(*search\_range=None*)[¶](#opentimelineio.schema.Clip.find_clips "Permalink to this definition")*property* media\_reference[¶](#opentimelineio.schema.Clip.media_reference "Permalink to this definition")media\_references() → Dict[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)"), [opentimelineio.\_otio.MediaReference](opentimelineio.core.html#opentimelineio.core.MediaReference "opentimelineio._otio.MediaReference")][¶](#opentimelineio.schema.Clip.media_references "Permalink to this definition")set\_media\_references(*arg0: Dict[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)"), [opentimelineio.\_otio.MediaReference](opentimelineio.core.html#opentimelineio.core.MediaReference "opentimelineio._otio.MediaReference")]*, *arg1: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")[¶](#opentimelineio.schema.Clip.set_media_references "Permalink to this definition")*class* opentimelineio.schema.Effect(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *effect\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.Effect "Permalink to this definition")*property* effect\_name[¶](#opentimelineio.schema.Effect.effect_name "Permalink to this definition")*class* opentimelineio.schema.ExternalReference(*target\_url: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *available\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *available\_image\_bounds: Optional[[opentimelineio.\_otio.Box2d](#opentimelineio.schema.Box2d "opentimelineio._otio.Box2d")] = None*)[¶](#opentimelineio.schema.ExternalReference "Permalink to this definition")*property* target\_url[¶](#opentimelineio.schema.ExternalReference.target_url "Permalink to this definition")*class* opentimelineio.schema.FreezeFrame(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.FreezeFrame "Permalink to this definition")

Hold the first frame of the clip for the duration of the clip.

*class* opentimelineio.schema.Gap(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *source\_range: [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange") = otio.opentime.TimeRange(start\_time=otio.opentime.RationalTime(value=0, rate=1), duration=otio.opentime.RationalTime(value=0, rate=1))*, *effects: Optional[List[[opentimelineio.\_otio.Effect](#opentimelineio.schema.Effect "opentimelineio._otio.Effect")]] = None*, *markers: Optional[List[[opentimelineio.\_otio.Marker](#opentimelineio.schema.Marker "opentimelineio._otio.Marker")]] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")[¶](#opentimelineio.schema.Gap "Permalink to this definition")*class* opentimelineio.schema.Gap(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *duration: [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime") = otio.opentime.RationalTime(value=0, rate=1)*, *effects: Optional[List[[opentimelineio.\_otio.Effect](#opentimelineio.schema.Effect "opentimelineio._otio.Effect")]] = None*, *markers: Optional[List[[opentimelineio.\_otio.Marker](#opentimelineio.schema.Marker "opentimelineio._otio.Marker")]] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")

Overloaded function.

1. \_\_init\_\_(self: opentimelineio.\_otio.Gap, name: str = ‘’, source\_range:
   opentimelineio.\_opentime.TimeRange =
   otio.opentime.TimeRange(start\_time=otio.opentime.RationalTime(value=0, rate=1),
   duration=otio.opentime.RationalTime(value=0, rate=1)), effects:
   Optional[List[opentimelineio.\_otio.Effect]] = None, markers:
   Optional[List[opentimelineio.\_otio.Marker]] = None, metadata: object = None) ->
   None
2. \_\_init\_\_(self: opentimelineio.\_otio.Gap, name: str = ‘’, duration:
   opentimelineio.\_opentime.RationalTime = otio.opentime.RationalTime(value=0,
   rate=1), effects: Optional[List[opentimelineio.\_otio.Effect]] = None, markers:
   Optional[List[opentimelineio.\_otio.Marker]] = None, metadata: object = None) ->
   None
*class* opentimelineio.schema.GeneratorReference(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *generator\_kind: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *available\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *parameters: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *available\_image\_bounds: Optional[[opentimelineio.\_otio.Box2d](#opentimelineio.schema.Box2d "opentimelineio._otio.Box2d")] = None*)[¶](#opentimelineio.schema.GeneratorReference "Permalink to this definition")*property* generator\_kind[¶](#opentimelineio.schema.GeneratorReference.generator_kind "Permalink to this definition")*property* parameters[¶](#opentimelineio.schema.GeneratorReference.parameters "Permalink to this definition")*class* opentimelineio.schema.ImageSequenceReference(*target\_url\_base: str = ''*, *name\_prefix: str = ''*, *name\_suffix: str = ''*, *start\_frame: int = 1*, *frame\_step: int = 1*, *rate: float = 1*, *frame\_zero\_padding: int = 0*, *missing\_frame\_policy: opentimelineio.\_otio.ImageSequenceReference.MissingFramePolicy = <MissingFramePolicy.error: 0>*, *available\_range: Optional[opentimelineio.\_opentime.TimeRange] = None*, *metadata: object = None*, *available\_image\_bounds: Optional[opentimelineio.\_otio.Box2d] = None*)[¶](#opentimelineio.schema.ImageSequenceReference "Permalink to this definition")

An ImageSequenceReference refers to a numbered series of single-frame image
files. Each file can be referred to by a URL generated by the
[`ImageSequenceReference`](#opentimelineio.schema.ImageSequenceReference

"opentimelineio.schema.ImageSequenceReference").

Image sequences can have URLs with discontinuous frame numbers, for instance if
you’ve only rendered every other frame in a sequence, your frame numbers may be
1, 3, 5, etc. This is configured using the `frame_step` attribute. In this case,
the 0th image in the sequence is frame 1 and the 1st image in the sequence is
frame 3. Because of this there are two numbering concepts in the image sequence,
the image number and the frame number.

Frame numbers are the integer numbers used in the frame file name. Image numbers
are the 0-index based numbers of the frames available in the reference. Frame
numbers can be discontinuous, image numbers will always be zero to the total
count of frames minus 1.

An example for 24fps media with a sample provided each frame numbered 1-1000
with a path `/show/sequence/shot/sample_image_sequence.%04d.exr` might be

```
{
  "available_range": {
    "start_time": {
      "value": 0,
      "rate": 24
    },
    "duration": {
      "value": 1000,
      "rate": 24
    }
  },
  "start_frame": 1,
  "frame_step": 1,
  "rate": 24,
  "target_url_base": "file:///show/sequence/shot/",
  "name_prefix": "sample_image_sequence.",
  "name_suffix": ".exr"
  "frame_zero_padding": 4,
}

```

The same duration sequence but with only every 2nd frame available in the
sequence would be

```
{
  "available_range": {
    "start_time": {
      "value": 0,
      "rate": 24
    },
    "duration": {
      "value": 1000,
      "rate": 24
    }
  },
  "start_frame": 1,
  "frame_step": 2,
  "rate": 24,
  "target_url_base": "file:///show/sequence/shot/",
  "name_prefix": "sample_image_sequence.",
  "name_suffix": ".exr"
  "frame_zero_padding": 4,
}

```

A list of all the frame URLs in the sequence can be generated, regardless of
frame step, with the following list comprehension

```
[ref.target_url_for_image_number(i) for i in range(ref.number_of_images_in_sequence())]

```

Negative `start_frame` is also handled. The above example with a `start_frame`
of `-1` would yield the first three target urls as:

* `file:///show/sequence/shot/sample_image_sequence.-0001.exr`
* `file:///show/sequence/shot/sample_image_sequence.0000.exr`
* `file:///show/sequence/shot/sample_image_sequence.0001.exr`

*class* MissingFramePolicy(*value: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")*)[¶](#opentimelineio.schema.ImageSequenceReference.MissingFramePolicy "Permalink to this definition")

Behavior that should be used by applications when an image file in the sequence
can’t be found on disk.

Members:

> error : Application should stop and raise an error.
>
> hold : Application should hold the last available frame before the missing
> frame.
>
> black : Application should use a black frame in place of the missing frame

black *= <MissingFramePolicy.black: 2>*[¶](#opentimelineio.schema.ImageSequenceReference.MissingFramePolicy.black "Permalink to this definition")error *= <MissingFramePolicy.error: 0>*[¶](#opentimelineio.schema.ImageSequenceReference.MissingFramePolicy.error "Permalink to this definition")hold *= <MissingFramePolicy.hold: 1>*[¶](#opentimelineio.schema.ImageSequenceReference.MissingFramePolicy.hold "Permalink to this definition")*property* name[¶](#opentimelineio.schema.ImageSequenceReference.MissingFramePolicy.name "Permalink to this definition")*property* value[¶](#opentimelineio.schema.ImageSequenceReference.MissingFramePolicy.value "Permalink to this definition")abstract\_target\_url(*symbol*)[¶](#opentimelineio.schema.ImageSequenceReference.abstract_target_url "Permalink to this definition")

Generates a target url for a frame where `symbol` is used in place of the frame
number. This is often used to generate wildcard target urls.

end\_frame() → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")[¶](#opentimelineio.schema.ImageSequenceReference.end_frame "Permalink to this definition")

Last frame number in the sequence based on the
[`rate`](#opentimelineio.schema.ImageSequenceReference.rate

"opentimelineio.schema.ImageSequenceReference.rate") and
[`available_range`](opentimelineio.core.html#opentimelineio.core.MediaReference.available_range

"opentimelineio.core.MediaReference.available_range").

frame\_for\_time(*time: [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")[¶](#opentimelineio.schema.ImageSequenceReference.frame_for_time "Permalink to this definition")

Given a
[`RationalTime`](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") within the available range, returns the
frame number.

frame\_range\_for\_time\_range(*time\_range*)[¶](#opentimelineio.schema.ImageSequenceReference.frame_range_for_time_range "Permalink to this definition")

Returns first and last frame numbers for the given time range in the reference.

Return type:

[tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python

v3.12)")[[int](https://docs.python.org/3/library/functions.html#int "(in Python

v3.12)")]

Raises:

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError

"(in Python v3.12)") – if the provided time range is outside the available
range.

*property* frame\_step[¶](#opentimelineio.schema.ImageSequenceReference.frame_step "Permalink to this definition")

Step between frame numbers in file names.

*property* frame\_zero\_padding[¶](#opentimelineio.schema.ImageSequenceReference.frame_zero_padding "Permalink to this definition")

Number of digits to pad zeros out to in frame numbers.

*property* missing\_frame\_policy[¶](#opentimelineio.schema.ImageSequenceReference.missing_frame_policy "Permalink to this definition")

Directive for how frames in sequence not found during playback or rendering
should be handled.

*property* name\_prefix[¶](#opentimelineio.schema.ImageSequenceReference.name_prefix "Permalink to this definition")

Everything in the file name leading up to the frame number.

*property* name\_suffix[¶](#opentimelineio.schema.ImageSequenceReference.name_suffix "Permalink to this definition")

Everything after the frame number in the file name.

number\_of\_images\_in\_sequence() → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")[¶](#opentimelineio.schema.ImageSequenceReference.number_of_images_in_sequence "Permalink to this definition")

Returns the number of images based on the
[`rate`](#opentimelineio.schema.ImageSequenceReference.rate

"opentimelineio.schema.ImageSequenceReference.rate") and
[`available_range`](opentimelineio.core.html#opentimelineio.core.MediaReference.available_range

"opentimelineio.core.MediaReference.available_range").

presentation\_time\_for\_image\_number(*image\_number: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.schema.ImageSequenceReference.presentation_time_for_image_number "Permalink to this definition")

Given an image number, returns the
[`RationalTime`](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") at which that image should be shown in
the space of
[`available_range`](opentimelineio.core.html#opentimelineio.core.MediaReference.available_range

"opentimelineio.core.MediaReference.available_range").

*property* rate[¶](#opentimelineio.schema.ImageSequenceReference.rate "Permalink to this definition")

Frame rate if every frame in the sequence were played back.

*property* start\_frame[¶](#opentimelineio.schema.ImageSequenceReference.start_frame "Permalink to this definition")

The first frame number used in file names.

*property* target\_url\_base[¶](#opentimelineio.schema.ImageSequenceReference.target_url_base "Permalink to this definition")

Everything leading up to the file name in the `target_url`.

target\_url\_for\_image\_number(*image\_number: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")*) → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")[¶](#opentimelineio.schema.ImageSequenceReference.target_url_for_image_number "Permalink to this definition")

Given an image number, returns the `target_url` for that image.

This is roughly equivalent to:

```
f"{target_url_prefix}{(start_frame + (image_number * frame_step)):0{value_zero_padding}}{target_url_postfix}"

```

*class* opentimelineio.schema.LinearTimeWarp(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *time\_scalar: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 1.0*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.LinearTimeWarp "Permalink to this definition")

A time warp that applies a linear speed up or slow down across the entire clip.

*property* time\_scalar[¶](#opentimelineio.schema.LinearTimeWarp.time_scalar "Permalink to this definition")

Linear time scalar applied to clip. 2.0 means the clip occupies half the time in
the parent item, i.e. plays at double speed, 0.5 means the clip occupies twice
the time in the parent item, i.e. plays at half speed.

Note that adjusting the time\_scalar of a
[`LinearTimeWarp`](#opentimelineio.schema.LinearTimeWarp

"opentimelineio.schema.LinearTimeWarp") does not affect the duration of the item
this effect is attached to. Instead it affects the speed of the media displayed
within that item.

*class* opentimelineio.schema.Marker(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *marked\_range: [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange") = otio.opentime.TimeRange(start\_time=otio.opentime.RationalTime(value=0, rate=1), duration=otio.opentime.RationalTime(value=0, rate=1))*, *color: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = 'RED'*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *comment: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*)[¶](#opentimelineio.schema.Marker "Permalink to this definition")

A marker indicates a marked range of time on an item in a timeline, usually with
a name, color or other metadata.

The marked range may have a zero duration. The marked range is in the owning
item’s time coordinate system.

*class* Color[¶](#opentimelineio.schema.Marker.Color "Permalink to this definition")BLACK *= 'BLACK'*[¶](#opentimelineio.schema.Marker.Color.BLACK "Permalink to this definition")BLUE *= 'BLUE'*[¶](#opentimelineio.schema.Marker.Color.BLUE "Permalink to this definition")CYAN *= 'CYAN'*[¶](#opentimelineio.schema.Marker.Color.CYAN "Permalink to this definition")GREEN *= 'GREEN'*[¶](#opentimelineio.schema.Marker.Color.GREEN "Permalink to this definition")MAGENTA *= 'MAGENTA'*[¶](#opentimelineio.schema.Marker.Color.MAGENTA "Permalink to this definition")ORANGE *= 'ORANGE'*[¶](#opentimelineio.schema.Marker.Color.ORANGE "Permalink to this definition")PINK *= 'PINK'*[¶](#opentimelineio.schema.Marker.Color.PINK "Permalink to this definition")PURPLE *= 'PURPLE'*[¶](#opentimelineio.schema.Marker.Color.PURPLE "Permalink to this definition")RED *= 'RED'*[¶](#opentimelineio.schema.Marker.Color.RED "Permalink to this definition")WHITE *= 'WHITE'*[¶](#opentimelineio.schema.Marker.Color.WHITE "Permalink to this definition")YELLOW *= 'YELLOW'*[¶](#opentimelineio.schema.Marker.Color.YELLOW "Permalink to this definition")*property* color[¶](#opentimelineio.schema.Marker.color "Permalink to this definition")

Color string for this marker (for example: ‘RED’), based on the
[`Color`](#opentimelineio.schema.Marker.Color

"opentimelineio.schema.Marker.Color") enum.

*property* comment[¶](#opentimelineio.schema.Marker.comment "Permalink to this definition")

Optional comment for this marker.

*property* marked\_range[¶](#opentimelineio.schema.Marker.marked_range "Permalink to this definition")

Range this marker applies to, relative to the
[`Item`](opentimelineio.core.html#opentimelineio.core.Item

"opentimelineio.core.Item") this marker is attached to (e.g. the
[`Clip`](#opentimelineio.schema.Clip "opentimelineio.schema.Clip") or

[`Track`](opentimelineio.core.html#opentimelineio.core.Track

"opentimelineio.core.Track") that owns this marker).

*class* opentimelineio.schema.MissingReference(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *available\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *available\_image\_bounds: Optional[[opentimelineio.\_otio.Box2d](#opentimelineio.schema.Box2d "opentimelineio._otio.Box2d")] = None*)[¶](#opentimelineio.schema.MissingReference "Permalink to this definition")

Represents media for which a concrete reference is missing.

Note that a [`MissingReference`](#opentimelineio.schema.MissingReference

"opentimelineio.schema.MissingReference") may have useful metadata, even if the
location of the media is not known.

*class* opentimelineio.schema.SchemaDef[¶](#opentimelineio.schema.SchemaDef "Permalink to this definition")module()[¶](#opentimelineio.schema.SchemaDef.module "Permalink to this definition")

Return the module object for this schemadef plugin. If the module hasn’t already
been imported, it is imported and injected into the otio.schemadefs namespace as
a side-effect.

Redefines
[`PythonPlugin.module()`](opentimelineio.plugins.python_plugin.html#opentimelineio.plugins.python_plugin.PythonPlugin.module

"opentimelineio.plugins.python_plugin.PythonPlugin.module").

plugin\_info\_map()[¶](#opentimelineio.schema.SchemaDef.plugin_info_map "Permalink to this definition")

Adds extra schemadef-specific information to call to the parent fn.

*class* opentimelineio.schema.SerializableCollection(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *children: Optional[List[[opentimelineio.\_otio.SerializableObject](opentimelineio.core.html#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")]] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.SerializableCollection "Permalink to this definition")

A container which can hold an ordered list of any serializable objects. Note
that this is not a
[`Composition`](opentimelineio.core.html#opentimelineio.core.Composition

"opentimelineio.core.Composition") nor is it
[`Composable`](opentimelineio.core.html#opentimelineio.core.Composable

"opentimelineio.core.Composable").

This container approximates the concept of a bin - a collection of
[`SerializableObject`](opentimelineio.core.html#opentimelineio.core.SerializableObject

"opentimelineio.core.SerializableObject")s that do not have any compositional
meaning, but can serialize to/from OTIO correctly, with metadata and a named
collection.

A [`SerializableCollection`](#opentimelineio.schema.SerializableCollection

"opentimelineio.schema.SerializableCollection") is useful for serializing
multiple timelines, clips, or media references to a single file.

find\_children(*descended\_from\_type: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *search\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → List[[opentimelineio.\_otio.SerializableObject](opentimelineio.core.html#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.schema.SerializableCollection.find_children "Permalink to this definition")find\_clips(*search\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → List[[opentimelineio.\_otio.SerializableObject](opentimelineio.core.html#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.schema.SerializableCollection.find_clips "Permalink to this definition")insert(*index*, *item*)[¶](#opentimelineio.schema.SerializableCollection.insert "Permalink to this definition")*class* opentimelineio.schema.Stack(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *children: Optional[List[[opentimelineio.\_otio.Composable](opentimelineio.core.html#opentimelineio.core.Composable "opentimelineio._otio.Composable")]] = None*, *source\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *markers: Optional[List[[opentimelineio.\_otio.Marker](#opentimelineio.schema.Marker "opentimelineio._otio.Marker")]] = None*, *effects: Optional[List[[opentimelineio.\_otio.Effect](#opentimelineio.schema.Effect "opentimelineio._otio.Effect")]] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.Stack "Permalink to this definition")find\_clips(*search\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → List[[opentimelineio.\_otio.SerializableObject](opentimelineio.core.html#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.schema.Stack.find_clips "Permalink to this definition")*class* opentimelineio.schema.TimeEffect(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *effect\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.TimeEffect "Permalink to this definition")

Base class for all effects that alter the timing of an item.

*class* opentimelineio.schema.Timeline(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *tracks: Optional[List[[opentimelineio.\_otio.Composable](opentimelineio.core.html#opentimelineio.core.Composable "opentimelineio._otio.Composable")]] = None*, *global\_start\_time: Optional[[opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.Timeline "Permalink to this definition")audio\_tracks() → List[[opentimelineio.\_otio.Track](opentimelineio.core.html#opentimelineio.core.Track "opentimelineio._otio.Track")][¶](#opentimelineio.schema.Timeline.audio_tracks "Permalink to this definition")duration() → [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.schema.Timeline.duration "Permalink to this definition")find\_children(*descended\_from\_type: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *search\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → List[[opentimelineio.\_otio.SerializableObject](opentimelineio.core.html#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.schema.Timeline.find_children "Permalink to this definition")find\_clips(*search\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → List[[opentimelineio.\_otio.SerializableObject](opentimelineio.core.html#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.schema.Timeline.find_clips "Permalink to this definition")*property* global\_start\_time[¶](#opentimelineio.schema.Timeline.global_start_time "Permalink to this definition")range\_of\_child(*arg0: [opentimelineio.\_otio.Composable](opentimelineio.core.html#opentimelineio.core.Composable "opentimelineio._otio.Composable")*) → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.schema.Timeline.range_of_child "Permalink to this definition")*property* tracks[¶](#opentimelineio.schema.Timeline.tracks "Permalink to this definition")video\_tracks() → List[[opentimelineio.\_otio.Track](opentimelineio.core.html#opentimelineio.core.Track "opentimelineio._otio.Track")][¶](#opentimelineio.schema.Timeline.video_tracks "Permalink to this definition")*class* opentimelineio.schema.Transition(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *transition\_type: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *in\_offset: [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime") = otio.opentime.RationalTime(value=0, rate=1)*, *out\_offset: [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime") = otio.opentime.RationalTime(value=0, rate=1)*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.schema.Transition "Permalink to this definition")

Represents a transition between the two adjacent items in a
[`Track`](opentimelineio.core.html#opentimelineio.core.Track

"opentimelineio.core.Track"). For example, a cross dissolve or wipe.

*class* Type[¶](#opentimelineio.schema.Transition.Type "Permalink to this definition")

Enum encoding types of transitions.

Other effects are handled by the [`Effect`](#opentimelineio.schema.Effect

"opentimelineio.schema.Effect") class.

Custom *= 'Custom\_Transition'*[¶](#opentimelineio.schema.Transition.Type.Custom "Permalink to this definition")SMPTE\_Dissolve *= 'SMPTE\_Dissolve'*[¶](#opentimelineio.schema.Transition.Type.SMPTE_Dissolve "Permalink to this definition")duration() → [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.schema.Transition.duration "Permalink to this definition")*property* in\_offset[¶](#opentimelineio.schema.Transition.in_offset "Permalink to this definition")

Amount of the previous clip this transition overlaps, exclusive.

*property* out\_offset[¶](#opentimelineio.schema.Transition.out_offset "Permalink to this definition")

Amount of the next clip this transition overlaps, exclusive.

range\_in\_parent() → Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")][¶](#opentimelineio.schema.Transition.range_in_parent "Permalink to this definition")

Find and return the range of this item in the parent.

*property* transition\_type[¶](#opentimelineio.schema.Transition.transition_type "Permalink to this definition")

Kind of transition, as defined by the
[`Type`](#opentimelineio.schema.Transition.Type

"opentimelineio.schema.Transition.Type") enum.

trimmed\_range\_in\_parent() → Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")][¶](#opentimelineio.schema.Transition.trimmed_range_in_parent "Permalink to this definition")

Find and return the timmed range of this item in the parent.

*class* opentimelineio.schema.V2d → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")[¶](#opentimelineio.schema.V2d "Permalink to this definition")*class* opentimelineio.schema.V2d(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")*class* opentimelineio.schema.V2d(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*, *arg1: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")

Overloaded function.

1. \_\_init\_\_(self: opentimelineio.\_otio.V2d) -> None
2. \_\_init\_\_(self: opentimelineio.\_otio.V2d, arg0: float) -> None
3. \_\_init\_\_(self: opentimelineio.\_otio.V2d, arg0: float, arg1: float) -> None

*static* baseTypeEpsilon() → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.baseTypeEpsilon "Permalink to this definition")*static* baseTypeLowest() → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.baseTypeLowest "Permalink to this definition")*static* baseTypeMax() → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.baseTypeMax "Permalink to this definition")*static* baseTypeSmallest() → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.baseTypeSmallest "Permalink to this definition")cross(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.cross "Permalink to this definition")*static* dimensions() → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.dimensions "Permalink to this definition")dot(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.dot "Permalink to this definition")equalWithAbsError(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*, *arg1: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.equalWithAbsError "Permalink to this definition")equalWithRelError(*arg0: [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")*, *arg1: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.equalWithRelError "Permalink to this definition")length() → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.length "Permalink to this definition")length2() → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.schema.V2d.length2 "Permalink to this definition")normalize() → [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")[¶](#opentimelineio.schema.V2d.normalize "Permalink to this definition")normalizeExc() → [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")[¶](#opentimelineio.schema.V2d.normalizeExc "Permalink to this definition")normalizeNonNull() → [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")[¶](#opentimelineio.schema.V2d.normalizeNonNull "Permalink to this definition")normalized() → [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")[¶](#opentimelineio.schema.V2d.normalized "Permalink to this definition")normalizedExc() → [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")[¶](#opentimelineio.schema.V2d.normalizedExc "Permalink to this definition")normalizedNonNull() → [opentimelineio.\_otio.V2d](#opentimelineio.schema.V2d "opentimelineio._otio.V2d")[¶](#opentimelineio.schema.V2d.normalizedNonNull "Permalink to this definition")*property* x[¶](#opentimelineio.schema.V2d.x "Permalink to this definition")*property* y[¶](#opentimelineio.schema.V2d.y "Permalink to this definition")opentimelineio.schema.timeline\_from\_clips(*clips*)[¶](#opentimelineio.schema.timeline_from_clips "Permalink to this definition")

Convenience for making a single track timeline from a list of clips.

Modules

|  |  |
| --- | --- |
| [`opentimelineio.schema.box2d`](opentimelineio.schema.box2d.html#module-opentimelineio.schema.box2d "opentimelineio.schema.box2d") |  |

| [`opentimelineio.schema.clip`](opentimelineio.schema.clip.html#module-opentimelineio.schema.clip "opentimelineio.schema.clip") |  |

| [`opentimelineio.schema.effect`](opentimelineio.schema.effect.html#module-opentimelineio.schema.effect "opentimelineio.schema.effect") |  |

| [`opentimelineio.schema.external_reference`](opentimelineio.schema.external_reference.html#module-opentimelineio.schema.external_reference "opentimelineio.schema.external_reference") |  |

| [`opentimelineio.schema.generator_reference`](opentimelineio.schema.generator_reference.html#module-opentimelineio.schema.generator_reference "opentimelineio.schema.generator_reference") |  |

| [`opentimelineio.schema.image_sequence_reference`](opentimelineio.schema.image_sequence_reference.html#module-opentimelineio.schema.image_sequence_reference "opentimelineio.schema.image_sequence_reference") |  |

| [`opentimelineio.schema.marker`](opentimelineio.schema.marker.html#module-opentimelineio.schema.marker "opentimelineio.schema.marker") |  |

| [`opentimelineio.schema.schemadef`](opentimelineio.schema.schemadef.html#module-opentimelineio.schema.schemadef "opentimelineio.schema.schemadef") |  |

| [`opentimelineio.schema.serializable_collection`](opentimelineio.schema.serializable_collection.html#module-opentimelineio.schema.serializable_collection "opentimelineio.schema.serializable_collection") |  |

| [`opentimelineio.schema.timeline`](opentimelineio.schema.timeline.html#module-opentimelineio.schema.timeline "opentimelineio.schema.timeline") |  |

| [`opentimelineio.schema.transition`](opentimelineio.schema.transition.html#module-opentimelineio.schema.transition "opentimelineio.schema.transition") |  |

| [`opentimelineio.schema.v2d`](opentimelineio.schema.v2d.html#module-opentimelineio.schema.v2d "opentimelineio.schema.v2d") |  |

---



## Page 28: Bridges.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/cxx/bridges.html](https://opentimelineio.readthedocs.io/en/stable/cxx/bridges.html)

* Language Bridges
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/cxx/bridges.md)


# Language Bridges[¶](#language-bridges "Permalink to this heading")


## Python[¶](#python "Permalink to this heading")

Since OTIO originated as Python (and has an extensive test suite, in Python),
our starting position is that existing Python code (adapters, plugins,
schemadefs) should continue to work, as currently written, with as few changes
as possible. However, in anticipation of the rewrite of the core in C++, some
changes are were made proactively made to ease this transition.

For example, the Opentime types (e.g. `RationalTime`) have value semantics in
C++, but reference semantics in Python, which has actually been a source of
bugs. Recent changes to the Python code have made the Opentime classes
immutable, to ease the transition to them being entirely value types in C++.

Python code in the `core` or `schema` directories were rewritten, but Python
code outside those modules should required little (or in some cases no) changes.

The bridge from C++ to Python (and back) is `pybind11`. Given that existing code
needs to work, clearly, the bridge is implemented so as to make the reflection
of the C++ datastructures, back to Python, utterly “Pythonic.” (It has to be,
since we didn’t want to break existing code.)


## Swift[¶](#swift "Permalink to this heading")

The intention is to expose OTIO in Swift with the same care we take with Python:
we want everything to feel utterly Swift-like. Because Swift can gain automatic
API access to non-member functions written in Objective-C++, and Objective-C++
can directly use the proposed OTIO C++ API, we believe that a bridge to swift
will not require writing an explicit `extern "C"` wrapper around OTIO C++. We
believe that like Python, Swift should be capable of defining new schemas, and
that access to existing and new schemas and their properties should be done in
terms of Swift API’s that conform Swift’s sequence/collection protocols, just as
Python interfaces do with respect to Python.


## Bridging to C (and other languages)[¶](#bridging-to-c-and-other-languages "Permalink to this heading")

Bridging to C (and by extension other languages) would presumably be
accomplished by writing an `extern "C"` wrapper around the OTIO C++ API. This is
of relatively low priority, given that we will have three languages (C++ itself,
Python, and Swift) that do not need this.

---



## Page 29: Stable

**Source:** [https://opentimelineio.readthedocs.io/en/stable](https://opentimelineio.readthedocs.io/en/stable)

* Welcome to OpenTimelineIO’s documentation!
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/index.rst)


# Welcome to OpenTimelineIO’s documentation![¶](#welcome-to-opentimelineio-s-documentation "Permalink to this heading")


## Overview[¶](#overview "Permalink to this heading")

OpenTimelineIO (OTIO) is an API and interchange format for editorial cut
information. You can think of it as a modern Edit Decision List (EDL) that also
includes an API for reading, writing, and manipulating editorial data. It also
includes a plugin system for translating to/from existing editorial formats as
well as a plugin system for linking to proprietary media storage schemas.

OTIO supports clips, timing, tracks, transitions, markers, metadata, etc. but
not embedded video or audio. Video and audio media are referenced externally. We
encourage 3rd party vendors, animation studios and visual effects studios to
work together as a community to provide adaptors for each video editing tool and
pipeline.


## Links[¶](#links "Permalink to this heading")

[OpenTimelineIO Home Page](http://opentimeline.io/)

[OpenTimelineIO Discussion Group](https://lists.aswf.io/g/otio-discussion)


## Quick Start[¶](#quick-start "Permalink to this heading")

Quick Start

* [Quickstart](tutorials/quickstart.html)
  + [Install Prerequisites](tutorials/quickstart.html#install-prerequisites)

  + [Install OTIO](tutorials/quickstart.html#install-otio)

  + [Setup Any Additional Adapters You May Want](tutorials/quickstart.html#setup-any-additional-adapters-you-may-want)

  + [Run OTIOView](tutorials/quickstart.html#run-otioview)

* [Developer Quickstart](tutorials/quickstart.html#developer-quickstart)

  + [To build OTIO for C++ development:](tutorials/quickstart.html#to-build-otio-for-c-development)

  + [To build OTIO for Python development:](tutorials/quickstart.html#to-build-otio-for-python-development)

  + [To build OTIO for both C++ and Python development:](tutorials/quickstart.html#to-build-otio-for-both-c-and-python-development)

* [Debugging Quickstart](tutorials/quickstart.html#debugging-quickstart)

  + [Linux / GDB / LLDB](tutorials/quickstart.html#linux-gdb-lldb)

* [How to Generate the C++ Documentation:](tutorials/quickstart.html#how-to-generate-the-c-documentation)

  + [Mac / Linux](tutorials/quickstart.html#mac-linux)

* [Environment Variables](tutorials/otio-env-variables.html)
  + [Plugin Configuration](tutorials/otio-env-variables.html#plugin-configuration)

  + [Unit tests](tutorials/otio-env-variables.html#unit-tests)


## Tutorials[¶](#tutorials "Permalink to this heading")

Tutorials

* [Adapters](tutorials/adapters.html)
  + [Built-In Adapters](tutorials/adapters.html#built-in-adapters)

  + [Batteries-Included Adapters](tutorials/adapters.html#batteries-included-adapters)

  + [Additional Adapters](tutorials/adapters.html#additional-adapters)

  + [Custom Adapters](tutorials/adapters.html#custom-adapters)

* [Architecture](tutorials/architecture.html)
  + [Overview](tutorials/architecture.html#overview)

  + [Canonical Structure](tutorials/architecture.html#canonical-structure)

  + [Modules](tutorials/architecture.html#modules)

  + [Time on otio.schema.Clip](tutorials/architecture.html#time-on-otio-schema-clip)

  + [Time On Clips in Containers](tutorials/architecture.html#time-on-clips-in-containers)

  + [otio.opentime](tutorials/architecture.html#otio-opentime)

  + [otio.adapters](tutorials/architecture.html#otio-adapters)

  + [otio.media\_linkers](tutorials/architecture.html#otio-media-linkers)

  + [Example Scripts](tutorials/architecture.html#example-scripts)

* [Contributing](tutorials/contributing.html)
  + [Contributor License Agreement](tutorials/contributing.html#contributor-license-agreement)

  + [Coding Conventions](tutorials/contributing.html#coding-conventions)

  + [Platform Support Policy](tutorials/contributing.html#platform-support-policy)

  + [Git Workflow](tutorials/contributing.html#git-workflow)

* [Feature Matrix](tutorials/feature-matrix.html)
* [Timeline Structure](tutorials/otio-timeline-structure.html)
  + [Rendering](tutorials/otio-timeline-structure.html#rendering)

  + [Simple Cut List](tutorials/otio-timeline-structure.html#simple-cut-list)

  + [Transitions](tutorials/otio-timeline-structure.html#transitions)

  + [Multiple Tracks](tutorials/otio-timeline-structure.html#multiple-tracks)

  + [Nested Compositions](tutorials/otio-timeline-structure.html#nested-compositions)

* [Time Ranges](tutorials/time-ranges.html)
  + [Overview](tutorials/time-ranges.html#overview)

  + [Clips](tutorials/time-ranges.html#clips)

  + [Tracks](tutorials/time-ranges.html#tracks)

  + [Markers](tutorials/time-ranges.html#markers)

  + [Transitions](tutorials/time-ranges.html#transitions)

  + [Gaps](tutorials/time-ranges.html#gaps)

  + [Stacks](tutorials/time-ranges.html#stacks)

  + [Timelines](tutorials/time-ranges.html#timelines)

* [File Bundles](tutorials/otio-filebundles.html)
  + [Overview](tutorials/otio-filebundles.html#overview)

  + [Source Timeline](tutorials/otio-filebundles.html#source-timeline)

  + [Structure](tutorials/otio-filebundles.html#structure)

  + [Read Behavior](tutorials/otio-filebundles.html#read-behavior)

  + [MediaReferencePolicy](tutorials/otio-filebundles.html#mediareferencepolicy)

  + [OTIOD](tutorials/otio-filebundles.html#otiod)

  + [OTIOZ](tutorials/otio-filebundles.html#otioz)

  + [Example usage in otioconvert](tutorials/otio-filebundles.html#example-usage-in-otioconvert)

* [Writing an OTIO Adapter](tutorials/write-an-adapter.html)
  + [Sharing an Adapter You’ve Written With the Community](tutorials/write-an-adapter.html#sharing-an-adapter-youve-written-with-the-community)

  + [Required Functions](tutorials/write-an-adapter.html#required-functions)

  + [Constructing a Timeline](tutorials/write-an-adapter.html#constructing-a-timeline)

  + [Traversing a Timeline](tutorials/write-an-adapter.html#traversing-a-timeline)

  + [Examples](tutorials/write-an-adapter.html#examples)

* [Writing an OTIO Media Linker](tutorials/write-a-media-linker.html)
  + [Registering Your Media Linker](tutorials/write-a-media-linker.html#registering-your-media-linker)

  + [Writing a Media Linker](tutorials/write-a-media-linker.html#writing-a-media-linker)

  + [For Testing](tutorials/write-a-media-linker.html#for-testing)

* [Writing a Hook Script](tutorials/write-a-hookscript.html)
  + [Registering Your Hook Script](tutorials/write-a-hookscript.html#registering-your-hook-script)

  + [Running a Hook Script](tutorials/write-a-hookscript.html#running-a-hook-script)

  + [Order of Hook Scripts](tutorials/write-a-hookscript.html#order-of-hook-scripts)

  + [Example Hooks](tutorials/write-a-hookscript.html#example-hooks)

* [Writing an OTIO SchemaDef Plugin](tutorials/write-a-schemadef.html)
  + [Registering Your SchemaDef Plugin](tutorials/write-a-schemadef.html#registering-your-schemadef-plugin)

  + [Using the New Schema in Your Code](tutorials/write-a-schemadef.html#using-the-new-schema-in-your-code)

* [OTIO Spatial Coordinate System](tutorials/spatial-coordinates.html)
  + [Coordinate System](tutorials/spatial-coordinates.html#coordinate-system)

  + [Bounds](tutorials/spatial-coordinates.html#bounds)

  + [Bounds and Clips](tutorials/spatial-coordinates.html#bounds-and-clips)

  + [Non-Bounds representations](tutorials/spatial-coordinates.html#non-bounds-representations)

* [Schema Proposal and Development Workflow](tutorials/developing-a-new-schema.html)
  + [Introduction](tutorials/developing-a-new-schema.html#introduction)

  + [Examples](tutorials/developing-a-new-schema.html#examples)

  + [Core schema or Plugin?](tutorials/developing-a-new-schema.html#core-schema-or-plugin)

  + [Proposal](tutorials/developing-a-new-schema.html#proposal)

  + [Implementing and Iterating on a branch](tutorials/developing-a-new-schema.html#implementing-and-iterating-on-a-branch)

  + [Demo Adapter](tutorials/developing-a-new-schema.html#demo-adapter)

  + [Incrementing Other Schemas](tutorials/developing-a-new-schema.html#incrementing-other-schemas)

  + [Conclusion](tutorials/developing-a-new-schema.html#conclusion)

* [Versioning Schemas](tutorials/versioning-schemas.html)
  + [Overview](tutorials/versioning-schemas.html#overview)

  + [Schema/Version Introduction](tutorials/versioning-schemas.html#schema-version-introduction)

  + [Schema Upgrading](tutorials/versioning-schemas.html#schema-upgrading)

  + [Schema Downgrading](tutorials/versioning-schemas.html#schema-downgrading)

  + [Downgrading at Runtime](tutorials/versioning-schemas.html#downgrading-at-runtime)

  + [For Developers](tutorials/versioning-schemas.html#for-developers)


## Use Cases[¶](#use-cases "Permalink to this heading")

Use Cases

* [Animation Shot Frame Ranges Changed](use-cases/animation-shot-frame-ranges.html)
  + [Summary](use-cases/animation-shot-frame-ranges.html#summary)

  + [Example](use-cases/animation-shot-frame-ranges.html#example)

  + [Features Needed in OTIO](use-cases/animation-shot-frame-ranges.html#features-needed-in-otio)

  + [Features of Python Script](use-cases/animation-shot-frame-ranges.html#features-of-python-script)

* [Conform New Renders Into The Cut](use-cases/conform-new-renders-into-cut.html)
  + [Summary](use-cases/conform-new-renders-into-cut.html#summary)

  + [Workflow](use-cases/conform-new-renders-into-cut.html#workflow)

* [Shots Added or Removed From The Cut](use-cases/shots-added-removed-from-cut.html)
  + [Summary](use-cases/shots-added-removed-from-cut.html#summary)

  + [Example](use-cases/shots-added-removed-from-cut.html#example)

  + [Features Needed in OTIO](use-cases/shots-added-removed-from-cut.html#features-needed-in-otio)

  + [Features of Python Script](use-cases/shots-added-removed-from-cut.html#features-of-python-script)


## API References[¶](#api-references "Permalink to this heading")

API References

* [Python](python_reference.html)
  + [opentimelineio](api/python/opentimelineio.html)
    - [opentimelineio.adapters](api/python/opentimelineio.adapters.html)
    - [opentimelineio.algorithms](api/python/opentimelineio.algorithms.html)
    - [opentimelineio.console](api/python/opentimelineio.console.html)
    - [opentimelineio.core](api/python/opentimelineio.core.html)
    - [opentimelineio.exceptions](api/python/opentimelineio.exceptions.html)
    - [opentimelineio.hooks](api/python/opentimelineio.hooks.html)
    - [opentimelineio.media\_linker](api/python/opentimelineio.media_linker.html)
    - [opentimelineio.opentime](api/python/opentimelineio.opentime.html)
    - [opentimelineio.plugins](api/python/opentimelineio.plugins.html)
    - [opentimelineio.schema](api/python/opentimelineio.schema.html)
    - [opentimelineio.schemadef](api/python/opentimelineio.schemadef.html)
    - [opentimelineio.test\_utils](api/python/opentimelineio.test_utils.html)
    - [opentimelineio.url\_utils](api/python/opentimelineio.url_utils.html)
    - [opentimelineio.versioning](api/python/opentimelineio.versioning.html)
* [Language Bridges](cxx/bridges.html)
  + [Python](cxx/bridges.html#python)

  + [Swift](cxx/bridges.html#swift)

  + [Bridging to C (and other languages)](cxx/bridges.html#bridging-to-c-and-other-languages)

* [C++ Implementation Details](cxx/cxx.html)
  + [Dependencies](cxx/cxx.html#dependencies)

  + [Starting Examples](cxx/cxx.html#starting-examples)

    - [Defining a Schema](cxx/cxx.html#defining-a-schema)

    - [Reading/Writing Properties](cxx/cxx.html#reading-writing-properties)

  + [Using Schemas](cxx/cxx.html#using-schemas)

  + [Serializable Data](cxx/cxx.html#serializable-data)

  + [C++ Properties](cxx/cxx.html#c-properties)

  + [Object Graphs and Serialization](cxx/cxx.html#object-graphs-and-serialization)

  + [Memory Management](cxx/cxx.html#memory-management)

    - [Examples](cxx/cxx.html#examples)

  + [Error Handling](cxx/cxx.html#error-handling)

  + [Thread Safety](cxx/cxx.html#thread-safety)

  + [Proposed OTIO C++ Header Files](cxx/cxx.html#proposed-otio-c-header-files)

  + [Extended Memory Management Discussion](cxx/cxx.html#extended-memory-management-discussion)

* [Writing OTIO in C, C++ or Python (June 2018)](cxx/older.html)
  + [Python C-API](cxx/older.html#python-c-api)

  + [Boost-Python](cxx/older.html#boost-python)

  + [PyBind11](cxx/older.html#pybind11)

  + [Conclusion](cxx/older.html#conclusion)


## Schema Reference[¶](#schema-reference "Permalink to this heading")

Schema Reference

* [File Format Specification](tutorials/otio-file-format-specification.html)
  + [Version](tutorials/otio-file-format-specification.html#version)

  + [Note](tutorials/otio-file-format-specification.html#note)

  + [Naming](tutorials/otio-file-format-specification.html#naming)

  + [Contents](tutorials/otio-file-format-specification.html#contents)

  + [Structure](tutorials/otio-file-format-specification.html#structure)

  + [Nesting](tutorials/otio-file-format-specification.html#nesting)

  + [Metadata](tutorials/otio-file-format-specification.html#metadata)

  + [Example:](tutorials/otio-file-format-specification.html#example)

  + [Schema Specification](tutorials/otio-file-format-specification.html#schema-specification)

* [Serialized Data Documentation](tutorials/otio-serialized-schema.html)
* [Class Documentation](tutorials/otio-serialized-schema.html#class-documentation)

  + [Module: opentimelineio.adapters](tutorials/otio-serialized-schema.html#module-opentimelineio-adapters)

  + [Module: opentimelineio.core](tutorials/otio-serialized-schema.html#module-opentimelineio-core)

  + [Module: opentimelineio.hooks](tutorials/otio-serialized-schema.html#module-opentimelineio-hooks)

  + [Module: opentimelineio.media\_linker](tutorials/otio-serialized-schema.html#module-opentimelineio-media-linker)

  + [Module: opentimelineio.opentime](tutorials/otio-serialized-schema.html#module-opentimelineio-opentime)

  + [Module: opentimelineio.plugins](tutorials/otio-serialized-schema.html#module-opentimelineio-plugins)

  + [Module: opentimelineio.schema](tutorials/otio-serialized-schema.html#module-opentimelineio-schema)

* [Serialized Data (Fields Only)](tutorials/otio-serialized-schema-only-fields.html)
* [Classes](tutorials/otio-serialized-schema-only-fields.html#classes)

  + [Module: opentimelineio.adapters](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-adapters)

  + [Module: opentimelineio.core](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-core)

  + [Module: opentimelineio.hooks](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-hooks)

  + [Module: opentimelineio.media\_linker](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-media-linker)

  + [Module: opentimelineio.opentime](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-opentime)

  + [Module: opentimelineio.plugins](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-plugins)

  + [Module: opentimelineio.schema](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-schema)


## Autogenerated Plugin Reference[¶](#autogenerated-plugin-reference "Permalink to this heading")

Plugins Reference

* [Plugin Documentation](tutorials/otio-plugins.html)
* [Manifests](tutorials/otio-plugins.html#manifests)

* [Core Plugins](tutorials/otio-plugins.html#core-plugins)

  + [Adapter Plugins](tutorials/otio-plugins.html#adapter-plugins)

  + [Media Linkers](tutorials/otio-plugins.html#media-linkers)

  + [SchemaDefs](tutorials/otio-plugins.html#schemadefs)

  + [HookScripts](tutorials/otio-plugins.html#hookscripts)

  + [Hooks](tutorials/otio-plugins.html#hooks)


## Indices and tables[¶](#indices-and-tables "Permalink to this heading")

* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)

---



## Page 30: Write A Media Linker.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/write-a-media-linker.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/write-a-media-linker.html)

* Writing an OTIO Media Linker
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/write-a-media-linker.md)


# Writing an OTIO Media Linker[¶](#writing-an-otio-media-linker "Permalink to this heading")

OpenTimelineIO Media Linkers are plugins that allow OTIO to replace
MissingReferences with valid, site specific MediaReferences after an adapter
reads a file.

The current MediaLinker can be specified as an argument to
`otio.adapters.read_from_file` or via an environment variable. If one is
specified, then it will run after the adapter reads the contents of the file
before it is returned back.

```
    #/usr/bin/env python

    import opentimelineio as otio
    mytimeline = otio.adapters.read_from_file("something.edl", media_linker_name="awesome_studios_media_linker")

```

After the EDL adapter reads something.edl, the media linker
“awesome\_studios\_media\_linker” will run and link the media in the file (if it
can).


## Registering Your Media Linker[¶](#registering-your-media-linker "Permalink to this heading")

To create a new OTIO Adapter, you need to create a file mymedialinker.py. Then
add a manifest that points at that python file:

```
        {
            "OTIO_SCHEMA" : "PluginManifest.1",
            "media_linkers" : [
                {
                    "OTIO_SCHEMA" : "MediaLinker.1",
                    "name" : "awesome_studios_media_linker",
                    "filepath" : "mymedialinker.py"
                 }
            ],
            "adapters" : [
            ]
        }

```

Then you need to add this manifest to your
[OTIO\_PLUGIN\_MANIFEST\_PATH](otio-env-variables.html#term-OTIO_PLUGIN_MANIFEST_PATH)

environment variable.

Finally, to specify this linker as the default media linker, set
[OTIO\_DEFAULT\_MEDIA\_LINKER](otio-env-variables.html#term-OTIO_DEFAULT_MEDIA_LINKER)

to the name of the media linker:

```
    export OTIO_DEFAULT_MEDIA_LINKER="awesome_studios_media_linker"

```

To package and share your media linker, follow [these
instructions](write-an-adapter.html#packaging-and-sharing-custom-adapters).


## Writing a Media Linker[¶](#writing-a-media-linker "Permalink to this heading")

To write a media linker, write a python file with a “link\_media\_reference”
function in it that takes two arguments: “in\_clip” (the clip to try and add a
media reference to) and “media\_linker\_argument\_map” (arguments passed from
the calling function to the media linker.

For example:

```
    def link_media_reference(in_clip, media_linker_argument_map):
        d.update(media_linker_argument_map)
        # you'll probably want to set it to something other than a missing reference

        in_clip.media_reference = otio.schema.MissingReference(
            name=in_clip.name + "_tweaked",
            metadata=d
        )

```


## For Testing[¶](#for-testing "Permalink to this heading")

The otioconvert.py script has a –media-linker argument you can use to test out
your media linker (once its on the path).

```
    env OTIO_PLUGIN_MANIFEST_PATH=mymanifest.otio.json:$OTIO_PLUGIN_MANIFEST_PATH bin/otioconvert.py -i somefile.edl --media-linker="awesome_studios_media_linker" -o /var/tmp/test.otio

```

---



## Page 31: Otio Plugins.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-plugins.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-plugins.html)

* Plugin Documentation
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/otio-plugins.md)


# Plugin Documentation[¶](#plugin-documentation "Permalink to this heading")

This documents all the plugins that ship with in the open source OpenTimelineIO
distribution.

This document is automatically generated by running the
`autogen_plugin_documentation` command, or by running `make plugin-model`. It is
part of the unit tests suite and should be updated whenever the schema changes.
If it needs to be updated, run: `make doc-plugins-update` and this file should
be regenerated.


# Manifests[¶](#manifests "Permalink to this heading")

The manifests describe plugins that are visible to OpenTimelineIO. The core
manifest is listed first, then any user-defined local plugins.

* `opentimelineio/adapters/builtin_adapters.plugin_manifest.json`


# Core Plugins[¶](#core-plugins "Permalink to this heading")

Manifest path: `opentimelineio/adapters/builtin_adapters.plugin_manifest.json`


## Adapter Plugins[¶](#adapter-plugins "Permalink to this heading")

Adapter plugins convert to and from OpenTimelineIO.

[Adapters documentation page for more information](adapters.html).

[Tutorial on how to write an adapter](write-an-adapter.html).


### otio\_json[¶](#otio-json "Permalink to this heading")

```
Adapter for reading and writing native .otio json files.

```

*source*: `opentimelineio/adapters/otio_json.py`

*Supported Features (with arguments)*:

* read\_from\_file:

```
De-serializes an OpenTimelineIO object from a file

  Args:
      filepath (str): The path to an otio file to read from

  Returns:
      OpenTimeline: An OpenTimeline object

```

* filepath
* read\_from\_string:

```
De-serializes an OpenTimelineIO object from a json string

  Args:
      input_str (str): A string containing json serialized otio contents

  Returns:
      OpenTimeline: An OpenTimeline object

```

* input\_str
* write\_to\_file:

```
Serializes an OpenTimelineIO object into a file

  Args:

      input_otio (OpenTimeline): An OpenTimeline object
      filepath (str): The name of an otio file to write to
      indent (int): number of spaces for each json indentation level.
  Use -1 for no indentation or newlines.

  If target_schema_versions is None and the environment variable
  "OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL" is set, will read a map out of
  that for downgrade target.  The variable should be of the form
  FAMILY:LABEL, for example "MYSTUDIO:JUNE2022".

  Returns:
      bool: Write success

  Raises:
      ValueError: on write error
      otio.exceptions.InvalidEnvironmentVariableError: if there is a problem
      with the default environment variable
      "OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL".

```

* input\_otio
* filepath
* target\_schema\_versions
* indent
* write\_to\_string:

```
Serializes an OpenTimelineIO object into a string

  Args:
      input_otio (OpenTimeline): An OpenTimeline object
      indent (int): number of spaces for each json indentation level. Use
  -1 for no indentation or newlines.

  If target_schema_versions is None and the environment variable
  "OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL" is set, will read a map out of
  that for downgrade target.  The variable should be of the form
  FAMILY:LABEL, for example "MYSTUDIO:JUNE2022".

  Returns:
      str: A json serialized string representation

  Raises:
      otio.exceptions.InvalidEnvironmentVariableError: if there is a problem
      with the default environment variable
      "OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL".

```

* input\_otio
* target\_schema\_versions
* indent


### otiod[¶](#otiod "Permalink to this heading")

```
OTIOD adapter - bundles otio files linked to local media in a directory

Takes as input an OTIO file that has media references which are all
ExternalReferences with target_urls to files with unique basenames that are
accessible through the file system and bundles those files and the otio file
into a single directory named with a suffix of .otiod.

```

*source*: `opentimelineio/adapters/otiod.py`

*Supported Features (with arguments)*:

* read\_from\_file:

  + filepath
  + absolute\_media\_reference\_paths
* write\_to\_file:

  + input\_otio
  + filepath
  + media\_policy
  + dryrun


### otioz[¶](#otioz "Permalink to this heading")

```
OTIOZ adapter - bundles otio files linked to local media

Takes as input an OTIO file that has media references which are all
ExternalReferences with target_urls to files with unique basenames that are
accessible through the file system and bundles those files and the otio file
into a single zip file with the suffix .otioz.  Can error out if files aren't
locally referenced or provide missing references

Can also extract the content.otio file from an otioz bundle for processing.

Note that OTIOZ files _always_ use the unix style path separator ('/'). This
ensures that regardless of which platform a bundle was created on, it can be
read on unix and windows platforms.

```

*source*: `opentimelineio/adapters/otioz.py`

*Supported Features (with arguments)*:

* read\_from\_file:

  + filepath
  + extract\_to\_directory
* write\_to\_file:

  + input\_otio
  + filepath
  + media\_policy
  + dryrun


## Media Linkers[¶](#media-linkers "Permalink to this heading")

Media Linkers run after the adapter has read in the file and convert the media
references into valid references where appropriate.

[Tutorial on how to write a Media Linker](write-a-media-linker.html).


## SchemaDefs[¶](#schemadefs "Permalink to this heading")

SchemaDef plugins define new external schema.

[Tutorial on how to write a schemadef](write-a-schemadef.html).


## HookScripts[¶](#hookscripts "Permalink to this heading")

HookScripts are extra plugins that run on *hooks*.

[Tutorial on how to write a hookscript](write-a-hookscript.html).


## Hooks[¶](#hooks "Permalink to this heading")

Hooks are the points at which hookscripts will run.

---



## Page 32: Shots Added Removed From Cut.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/use-cases/shots-added-removed-from-cut.html](https://opentimelineio.readthedocs.io/en/stable/use-cases/shots-added-removed-from-cut.html)

* Shots Added or Removed From The Cut
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/use-cases/shots-added-removed-from-cut.md)


# Shots Added or Removed From The Cut[¶](#shots-added-or-removed-from-the-cut "Permalink to this heading")

**Status: Planned**


## Summary[¶](#summary "Permalink to this heading")

The creative process of editing often involves adding, removing or replacing
shots in a sequence. Other groups of people working on the same project want to
know about changes to the list of shots in use on a day to day basis. For
example, animators working on a shot should be informed if the shot they are
working on has been cut from the sequence, so they can stop working on it.
Similarly, if new shots are added, animation should start working on those
shots. Since the creative decision about which shots are in or out of the cut
comes from editorial, we can use OTIO to communicate these changes.


## Example[¶](#example "Permalink to this heading")

Editorial is working on a short film in Avid Media Composer. They have several
bins of media with live action footage, rendered animation clips, dialogue
recordings, sound effects and music. The lead editor is actively working on the
cut for the short film over the course of a few weeks. At the same time, the
animation department is actively working on the animated shots for the film. As
revisions are made to the animated shots, rendered clips are delivered to
editorial with a well established naming convention. On a daily basis, an EDL or
AAF is exported from Media Composer and passed to the animation department so
they can stay up to date with the current cut.

In each revision of the cut, Animation wants to know which shots have been added
or removed. They run a Python script which uses OpenTimelineIO to read an EDL or
AAF from editorial and produces a list of video clip names found in the cut.
Some of these names match the animation department’s shot naming convention - or
contain shot tracking metadata - and can be compared to existing shots that the
animators are working on.

If there are shots being animated that are not in this cut, then animation can
stop working on those shots, as they are no longer needed.

When the editor wants to request a new shot with a new camera angle or new
animation, he or she can duplicate an existing clip and give it a new name, or
insert a placeholder with a previously unused name, or otherwise flag the new
clip as a request for a new shot. When animation sees this newly requested shot
in the cut, they can respond as appropriate and deliver the new shot to
editorial when it is ready.


## Features Needed in OTIO[¶](#features-needed-in-otio "Permalink to this heading")

* EDL reading (done)

  + Clip names across all tracks
* [AAF
  reading](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/issues/1)

  + Clip names across all tracks, subclips, etc.
* Timeline should include (done)

  + a Stack of tracks, each of which is a Sequence
* Sequence should include (done)

  + a list of Clips
* Clips should include (done)

  + Name
  + Metadata


## Features of Python Script[¶](#features-of-python-script "Permalink to this heading")

* Use OTIO to read the EDL or AAF. (done)
* Iterate through every Clip in the Timeline, printing its name. (done)
* Compare these names to the shots in a production tracking system.

---



## Page 33: Otio Env Variables.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-env-variables.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-env-variables.html)

* Environment Variables
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/otio-env-variables.md)


# Environment Variables[¶](#environment-variables "Permalink to this heading")

This document describes the environment variables that can be used to configure
various aspects of OTIO.


## Plugin Configuration[¶](#plugin-configuration "Permalink to this heading")

These variables must be set *before* the OpenTimelineIO python library is
imported. They only impact the python library. The C++ library has no
environment variables.

OTIO\_PLUGIN\_MANIFEST\_PATH[¶](#term-OTIO_PLUGIN_MANIFEST_PATH "Permalink to this term")

A colon (`:`) on POSIX system (or a semicolon (`;`) on Windows) separated string
with paths to `.manifest.json` files that contain OTIO plugin manifests. See the
[tutorial on how to write an adapter plugin](write-an-adapter.html) for
additional details.

OTIO\_DEFAULT\_MEDIA\_LINKER[¶](#term-OTIO_DEFAULT_MEDIA_LINKER "Permalink to this term")

The name of the default media linker to use after reading a file, if `""` then
no media linker is automatically invoked.

OTIO\_DISABLE\_ENTRYPOINTS\_PLUGINS[¶](#term-OTIO_DISABLE_ENTRYPOINTS_PLUGINS "Permalink to this term")

By default, OTIO will use the `importlib.metadata` entry\_points mechanism to
discover plugins that have been installed into the current python environment.
For users who wish to disable this behavior, this variable can be set to 1.

OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL[¶](#term-OTIO_DEFAULT_TARGET_VERSION_FAMILY_LABEL "Permalink to this term")

If no downgrade arguments are passed to `write_to_file`/`write_to_string`, use
the downgrade manifest specified by the family/label combination in the
variable. Variable is of the form `FAMILY:LABEL`. Only one tuple of
`FAMILY:LABEL` may be specified.


## Unit tests[¶](#unit-tests "Permalink to this heading")

These variables only impact unit tests.

OTIO\_DISABLE\_SHELLOUT\_TESTS[¶](#term-OTIO_DISABLE_SHELLOUT_TESTS "Permalink to this term")

When running the unit tests, skip the console tests that run the otiocat program
and check output through the shell. This is desirable in environments where
running the commandline tests is not meaningful or problematic. Does not disable
the tests that run through python calling mechanisms.

OTIO\_DISABLE\_SERIALIZED\_SCHEMA\_TEST[¶](#term-OTIO_DISABLE_SERIALIZED_SCHEMA_TEST "Permalink to this term")

Skip the unit tests that generate documentation and compare the current state of
the schema against the stored one. Useful if the documentation is not available
from the test directory.

---



## Page 34: Opentimelineio.Core.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.core
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.core.rst)


# opentimelineio.core[¶](#module-opentimelineio.core "Permalink to this heading")

Core implementation details and wrappers around the C++ library

*class* opentimelineio.core.Composable(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.core.Composable "Permalink to this definition")

An object that can be composed within a
[`Composition`](#opentimelineio.core.Composition

"opentimelineio.core.Composition") (such as [`Track`](#opentimelineio.core.Track

"opentimelineio.core.Track") or
[`Stack`](opentimelineio.schema.html#opentimelineio.schema.Stack

"opentimelineio.schema.Stack")).

overlapping() → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.core.Composable.overlapping "Permalink to this definition")parent() → [opentimelineio.\_otio.Composition](#opentimelineio.core.Composition "opentimelineio._otio.Composition")[¶](#opentimelineio.core.Composable.parent "Permalink to this definition")visible() → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.core.Composable.visible "Permalink to this definition")*class* opentimelineio.core.Composition(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *children: Optional[List[[opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable")]] = None*, *source\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.core.Composition "Permalink to this definition")

Base class for an [`Item`](#opentimelineio.core.Item "opentimelineio.core.Item")

that contains [`Composable`](#opentimelineio.core.Composable

"opentimelineio.core.Composable")s.

Should be subclassed (for example by [`Track`](#opentimelineio.core.Track

"opentimelineio.core.Track") and
[`Stack`](opentimelineio.schema.html#opentimelineio.schema.Stack

"opentimelineio.schema.Stack")), not used directly.

child\_at\_time(*search\_time: [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → [opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable")[¶](#opentimelineio.core.Composition.child_at_time "Permalink to this definition")children\_in\_range(*search\_range: [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*) → List[[opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.core.Composition.children_in_range "Permalink to this definition")*property* composition\_kind[¶](#opentimelineio.core.Composition.composition_kind "Permalink to this definition")find\_children(*descended\_from\_type: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *search\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → List[[opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.core.Composition.find_children "Permalink to this definition")handles\_of\_child(*child: [opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable")*) → [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.12)")[¶](#opentimelineio.core.Composition.handles_of_child "Permalink to this definition")has\_clips() → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.core.Composition.has_clips "Permalink to this definition")insert(*index*, *item*)[¶](#opentimelineio.core.Composition.insert "Permalink to this definition")is\_parent\_of(*other: [opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.core.Composition.is_parent_of "Permalink to this definition")range\_of\_all\_children() → [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.12)")[¶](#opentimelineio.core.Composition.range_of_all_children "Permalink to this definition")range\_of\_child(*child: [opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable")*, *reference\_space: [opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable") = None*) → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Composition.range_of_child "Permalink to this definition")range\_of\_child\_at\_index(*index: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")*) → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Composition.range_of_child_at_index "Permalink to this definition")trim\_child\_range(*child\_range: [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*) → Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")][¶](#opentimelineio.core.Composition.trim_child_range "Permalink to this definition")trimmed\_child\_range(*child\_range: [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*) → Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")][¶](#opentimelineio.core.Composition.trimmed_child_range "Permalink to this definition")trimmed\_range\_of\_child(*child: [opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable")*, *reference\_space: [opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable") = None*) → Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")][¶](#opentimelineio.core.Composition.trimmed_range_of_child "Permalink to this definition")trimmed\_range\_of\_child\_at\_index(*index: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")*) → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Composition.trimmed_range_of_child_at_index "Permalink to this definition")*class* opentimelineio.core.Item(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *source\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *effects: Optional[List[[opentimelineio.\_otio.Effect](opentimelineio.schema.html#opentimelineio.schema.Effect "opentimelineio._otio.Effect")]] = None*, *markers: Optional[List[[opentimelineio.\_otio.Marker](opentimelineio.schema.html#opentimelineio.schema.Marker "opentimelineio._otio.Marker")]] = None*, *enabled: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = True*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.core.Item "Permalink to this definition")*property* available\_image\_bounds[¶](#opentimelineio.core.Item.available_image_bounds "Permalink to this definition")available\_range() → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Item.available_range "Permalink to this definition")duration() → [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.core.Item.duration "Permalink to this definition")*property* effects[¶](#opentimelineio.core.Item.effects "Permalink to this definition")*property* enabled[¶](#opentimelineio.core.Item.enabled "Permalink to this definition")

If true, an Item contributes to compositions. For example, when an audio/video
clip is `enabled=false` the clip is muted/hidden.

*property* markers[¶](#opentimelineio.core.Item.markers "Permalink to this definition")range\_in\_parent() → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Item.range_in_parent "Permalink to this definition")*property* source\_range[¶](#opentimelineio.core.Item.source_range "Permalink to this definition")transformed\_time(*time: [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *to\_item: [opentimelineio.\_otio.Item](#opentimelineio.core.Item "opentimelineio._otio.Item")*) → [opentimelineio.\_opentime.RationalTime](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.core.Item.transformed_time "Permalink to this definition")transformed\_time\_range(*time\_range: [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *to\_item: [opentimelineio.\_otio.Item](#opentimelineio.core.Item "opentimelineio._otio.Item")*) → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Item.transformed_time_range "Permalink to this definition")trimmed\_range() → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Item.trimmed_range "Permalink to this definition")trimmed\_range\_in\_parent() → Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")][¶](#opentimelineio.core.Item.trimmed_range_in_parent "Permalink to this definition")visible\_range() → [opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.core.Item.visible_range "Permalink to this definition")*class* opentimelineio.core.MediaReference(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *available\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*, *available\_image\_bounds: Optional[[opentimelineio.\_otio.Box2d](opentimelineio.schema.html#opentimelineio.schema.Box2d "opentimelineio._otio.Box2d")] = None*)[¶](#opentimelineio.core.MediaReference "Permalink to this definition")*property* available\_image\_bounds[¶](#opentimelineio.core.MediaReference.available_image_bounds "Permalink to this definition")*property* available\_range[¶](#opentimelineio.core.MediaReference.available_range "Permalink to this definition")*property* is\_missing\_reference[¶](#opentimelineio.core.MediaReference.is_missing_reference "Permalink to this definition")*class* opentimelineio.core.SerializableObject[¶](#opentimelineio.core.SerializableObject "Permalink to this definition")

Superclass for all classes whose instances can be serialized.

clone() → [opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")[¶](#opentimelineio.core.SerializableObject.clone "Permalink to this definition")deepcopy(*\*args*, *\*\*kwargs*)[¶](#opentimelineio.core.SerializableObject.deepcopy "Permalink to this definition")*static* from\_json\_file(*file\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*) → [opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")[¶](#opentimelineio.core.SerializableObject.from_json_file "Permalink to this definition")*static* from\_json\_string(*input: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*) → [opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")[¶](#opentimelineio.core.SerializableObject.from_json_string "Permalink to this definition")is\_equivalent\_to(*other: [opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.core.SerializableObject.is_equivalent_to "Permalink to this definition")*property* is\_unknown\_schema[¶](#opentimelineio.core.SerializableObject.is_unknown_schema "Permalink to this definition")schema\_name() → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")[¶](#opentimelineio.core.SerializableObject.schema_name "Permalink to this definition")schema\_version() → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")[¶](#opentimelineio.core.SerializableObject.schema_version "Permalink to this definition")to\_json\_file(*file\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*, *indent: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)") = 4*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.core.SerializableObject.to_json_file "Permalink to this definition")to\_json\_string(*indent: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)") = 4*) → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")[¶](#opentimelineio.core.SerializableObject.to_json_string "Permalink to this definition")*class* opentimelineio.core.SerializableObjectWithMetadata(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.core.SerializableObjectWithMetadata "Permalink to this definition")*property* metadata[¶](#opentimelineio.core.SerializableObjectWithMetadata.metadata "Permalink to this definition")*property* name[¶](#opentimelineio.core.SerializableObjectWithMetadata.name "Permalink to this definition")*class* opentimelineio.core.Track(*name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = ''*, *children: Optional[List[[opentimelineio.\_otio.Composable](#opentimelineio.core.Composable "opentimelineio._otio.Composable")]] = None*, *source\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *kind: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)") = 'Video'*, *metadata: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)") = None*)[¶](#opentimelineio.core.Track "Permalink to this definition")*class* Kind[¶](#opentimelineio.core.Track.Kind "Permalink to this definition")Audio *= 'Audio'*[¶](#opentimelineio.core.Track.Kind.Audio "Permalink to this definition")Video *= 'Video'*[¶](#opentimelineio.core.Track.Kind.Video "Permalink to this definition")*class* NeighborGapPolicy(*value: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")*)[¶](#opentimelineio.core.Track.NeighborGapPolicy "Permalink to this definition")

Members:

around\_transitions

never

around\_transitions *= <NeighborGapPolicy.around\_transitions: 1>*[¶](#opentimelineio.core.Track.NeighborGapPolicy.around_transitions "Permalink to this definition")*property* name[¶](#opentimelineio.core.Track.NeighborGapPolicy.name "Permalink to this definition")never *= <NeighborGapPolicy.never: 0>*[¶](#opentimelineio.core.Track.NeighborGapPolicy.never "Permalink to this definition")*property* value[¶](#opentimelineio.core.Track.NeighborGapPolicy.value "Permalink to this definition")find\_clips(*search\_range: Optional[[opentimelineio.\_opentime.TimeRange](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")] = None*, *shallow\_search: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)") = False*) → List[[opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")][¶](#opentimelineio.core.Track.find_clips "Permalink to this definition")*property* kind[¶](#opentimelineio.core.Track.kind "Permalink to this definition")neighbors\_of(*item: opentimelineio.\_otio.Composable*, *policy: opentimelineio.\_otio.Track.NeighborGapPolicy = <NeighborGapPolicy.never: 0>*) → [tuple](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.12)")[¶](#opentimelineio.core.Track.neighbors_of "Permalink to this definition")opentimelineio.core.add\_method(*cls*)[¶](#opentimelineio.core.add_method "Permalink to this definition")opentimelineio.core.deprecated\_field()[¶](#opentimelineio.core.deprecated_field "Permalink to this definition")

For marking attributes on a SerializableObject deprecated.

opentimelineio.core.deserialize\_json\_from\_file(*filename: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*) → [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)")[¶](#opentimelineio.core.deserialize_json_from_file "Permalink to this definition")

Deserialize json file to in-memory objects.

Parameters:

**filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

Python v3.12)")) – path to json file to read

Returns:

root object in the file (usually a Timeline or SerializableCollection)

Return type:

[SerializableObject](#opentimelineio.core.SerializableObject

"opentimelineio.core.SerializableObject")

opentimelineio.core.deserialize\_json\_from\_string(*input: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*) → [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)")[¶](#opentimelineio.core.deserialize_json_from_string "Permalink to this definition")

Deserialize json string to in-memory objects.

Parameters:

**input** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

Python v3.12)")) – json string to deserialize

Returns:

root object in the string (usually a Timeline or SerializableCollection)

Return type:

[SerializableObject](#opentimelineio.core.SerializableObject

"opentimelineio.core.SerializableObject")

opentimelineio.core.downgrade\_function\_from(*cls*, *version\_to\_downgrade\_from*)[¶](#opentimelineio.core.downgrade_function_from "Permalink to this definition")

Decorator for identifying schema class downgrade functions.

Example:

```
@downgrade_function_from(MyClass, 5)
def downgrade_from_five_to_four(data):
    return {"old_attr": data["new_attr"]}

```

This will get called to downgrade a schema of MyClass from version 5 to version
4. MyClass must be a class deriving from
[`SerializableObject`](#opentimelineio.core.SerializableObject

"opentimelineio.core.SerializableObject").

The downgrade function should take a single argument - the dictionary to
downgrade, and return a dictionary with the fields downgraded.

Parameters:

* **cls** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in

  Python v3.12)")*[*[*SerializableObject*](#opentimelineio.core.SerializableObject

  "opentimelineio.core.SerializableObject")*]*) – class to downgrade
* **version\_to\_downgrade\_from**
  ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python

  v3.12)")) – the function downgrading from this version to (version - 1)
opentimelineio.core.flatten\_stack(*in\_stack: [opentimelineio.\_otio.Stack](opentimelineio.schema.html#opentimelineio.schema.Stack "opentimelineio._otio.Stack")*) → [opentimelineio.\_otio.Track](#opentimelineio.core.Track "opentimelineio._otio.Track")[¶](#opentimelineio.core.flatten_stack "Permalink to this definition")opentimelineio.core.flatten\_stack(*tracks: List[[opentimelineio.\_otio.Track](#opentimelineio.core.Track "opentimelineio._otio.Track")]*) → [opentimelineio.\_otio.Track](#opentimelineio.core.Track "opentimelineio._otio.Track")

Overloaded function.

1. flatten\_stack(in\_stack: opentimelineio.\_otio.Stack) ->
   opentimelineio.\_otio.Track
2. flatten\_stack(tracks: List[opentimelineio.\_otio.Track]) ->
   opentimelineio.\_otio.Track
opentimelineio.core.install\_external\_keepalive\_monitor(*so: [opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")*, *apply\_now: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")[¶](#opentimelineio.core.install_external_keepalive_monitor "Permalink to this definition")opentimelineio.core.instance\_from\_schema(*schema\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*, *schema\_version: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")*, *data: [object](https://docs.python.org/3/library/functions.html#object "(in Python v3.12)")*) → [opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")[¶](#opentimelineio.core.instance_from_schema "Permalink to this definition")

Return an instance of the schema from data in the data\_dict.

Raises:

[**UnsupportedSchemaError**](opentimelineio.exceptions.html#opentimelineio.exceptions.UnsupportedSchemaError

"opentimelineio.exceptions.UnsupportedSchemaError") – when the requested schema
version is greater than the registered schema version.

opentimelineio.core.register\_type(*classobj*, *schemaname=None*)[¶](#opentimelineio.core.register_type "Permalink to this definition")

Decorator for registering a SerializableObject type

Example:

```
@otio.core.register_type
class SimpleClass(otio.core.SerializableObject):
  serializable_label = "SimpleClass.2"
  ...

```

Parameters:

* **cls** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in

  Python v3.12)")*[*[*SerializableObject*](#opentimelineio.core.SerializableObject

  "opentimelineio.core.SerializableObject")*]*) – class to register
* **schemaname** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

  Python v3.12)")) – Schema name (default: parse from serializable\_label)
opentimelineio.core.release\_to\_schema\_version\_map() → Dict[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)"), Dict[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)"), [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")]][¶](#opentimelineio.core.release_to_schema_version_map "Permalink to this definition")

Fetch the compiled in CORE\_VERSION\_MAP.

The CORE\_VERSION\_MAP maps OTIO release versions to maps of schema name to
schema version and is autogenerated by the OpenTimelineIO build and release
system. For example: {“0.15.0”: {“Clip”: 2, …}}

Returns:

dictionary mapping core version label to schema\_version\_map

Return type:

[dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python

v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python

v3.12)"), [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in

Python v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in

Python v3.12)"), [int](https://docs.python.org/3/library/functions.html#int "(in

Python v3.12)")]]

opentimelineio.core.serializable\_field(*name*, *required\_type=None*, *doc=None*, *default\_value=None*)[¶](#opentimelineio.core.serializable_field "Permalink to this definition")

Convenience function for adding attributes to child classes of
[`SerializableObject`](#opentimelineio.core.SerializableObject

"opentimelineio.core.SerializableObject") in such a way that they will be
serialized/deserialized automatically.

Use it like this:

```
@core.register_type
class Foo(SerializableObject):
    bar = serializable_field("bar", required_type=int, doc="example")

```

This would indicate that class “foo” has a serializable field “bar”. So:

```
f = foo()
f.bar = "stuff"


# serialize & deserialize

otio_json = otio.adapters.from_name("otio")
f2 = otio_json.read_from_string(otio_json.write_to_string(f))


# fields should be equal

f.bar == f2.bar

```

Additionally, the “doc” field will become the documentation for the property.

Parameters:

* **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

  Python v3.12)")) – name of the field to add
* **required\_type**
  ([*type*](https://docs.python.org/3/library/functions.html#type "(in Python

  v3.12)")) – type required for the field
* **doc** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python

  v3.12)")) – field documentation
* **default\_value** (*Any*) – default value to return if no field value is set
  yet
Returns:

property object

Return type:

[`property`](https://docs.python.org/3/library/functions.html#property "(in

Python v3.12)")

opentimelineio.core.serialize\_json\_to\_file(*root*, *filename*, *schema\_version\_targets=None*, *indent=4*)[¶](#opentimelineio.core.serialize_json_to_file "Permalink to this definition")

Serialize root to a json file. Optionally downgrade resulting schemas to
schema\_version\_targets.

Parameters:

* **root** ([*SerializableObject*](#opentimelineio.core.SerializableObject

  "opentimelineio.core.SerializableObject")) – root object to serialize
* **schema\_version\_targets**
  ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python

  v3.12)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

  Python v3.12)")*,* [*int*](https://docs.python.org/3/library/functions.html#int

  "(in Python v3.12)")*]*) – optional dictionary mapping schema name to desired
  schema version, for downgrading the result to be compatible with older versions
  of OpenTimelineIO.
* **indent** ([*int*](https://docs.python.org/3/library/functions.html#int "(in

  Python v3.12)")) – number of spaces for each json indentation level. Use -1 for
  no indentation or newlines.
Returns:

true for success, false for failure

Return type:

[bool](https://docs.python.org/3/library/functions.html#bool "(in Python

v3.12)")

opentimelineio.core.serialize\_json\_to\_string(*root*, *schema\_version\_targets=None*, *indent=4*)[¶](#opentimelineio.core.serialize_json_to_string "Permalink to this definition")

Serialize root to a json string. Optionally downgrade resulting schemas to
schema\_version\_targets.

Parameters:

* **root** ([*SerializableObject*](#opentimelineio.core.SerializableObject

  "opentimelineio.core.SerializableObject")) – root object to serialize
* **schema\_version\_targets**
  ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python

  v3.12)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in

  Python v3.12)")*,* [*int*](https://docs.python.org/3/library/functions.html#int

  "(in Python v3.12)")*]*) – optional dictionary mapping schema name to desired
  schema version, for downgrading the result to be compatible with older versions
  of OpenTimelineIO.
* **indent** ([*int*](https://docs.python.org/3/library/functions.html#int "(in

  Python v3.12)")) – number of spaces for each json indentation level. Use -1 for
  no indentation or newlines.
Returns:

resulting json string

Return type:

[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")

opentimelineio.core.set\_type\_record(*serializable\_obejct: [opentimelineio.\_otio.SerializableObject](#opentimelineio.core.SerializableObject "opentimelineio._otio.SerializableObject")*, *schema\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*) → [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.12)")[¶](#opentimelineio.core.set_type_record "Permalink to this definition")opentimelineio.core.type\_version\_map() → Dict[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)"), [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")][¶](#opentimelineio.core.type_version_map "Permalink to this definition")

Fetch the currently registered schemas and their versions.

Returns:

Map of all registered schema names to their current versions.

Return type:

[dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python

v3.12)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python

v3.12)"), [int](https://docs.python.org/3/library/functions.html#int "(in Python

v3.12)")]

opentimelineio.core.upgrade\_function\_for(*cls*, *version\_to\_upgrade\_to*)[¶](#opentimelineio.core.upgrade_function_for "Permalink to this definition")

Decorator for identifying schema class upgrade functions.

Example:

```
@upgrade_function_for(MyClass, 5)
def upgrade_to_version_five(data):
    pass

```

This will get called to upgrade a schema of MyClass to version 5. MyClass must
be a class deriving from
[`SerializableObject`](#opentimelineio.core.SerializableObject

"opentimelineio.core.SerializableObject").

The upgrade function should take a single argument - the dictionary to upgrade,
and return a dictionary with the fields upgraded.

Remember that you don’t need to provide an upgrade function for upgrades that
add or remove fields, only for schema versions that change the field names.

Parameters:

* **cls** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in

  Python v3.12)")*[*[*SerializableObject*](#opentimelineio.core.SerializableObject

  "opentimelineio.core.SerializableObject")*]*) – class to upgrade
* **version\_to\_upgrade\_to**
  ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python

  v3.12)")) – the version to upgrade to

Modules

|  |  |
| --- | --- |
| [`opentimelineio.core.composable`](opentimelineio.core.composable.html#module-opentimelineio.core.composable "opentimelineio.core.composable") |  |

| [`opentimelineio.core.composition`](opentimelineio.core.composition.html#module-opentimelineio.core.composition "opentimelineio.core.composition") |  |

| [`opentimelineio.core.item`](opentimelineio.core.item.html#module-opentimelineio.core.item "opentimelineio.core.item") |  |

| [`opentimelineio.core.mediaReference`](opentimelineio.core.mediaReference.html#module-opentimelineio.core.mediaReference "opentimelineio.core.mediaReference") |  |

---



## Page 35: Contributing.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/contributing.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/contributing.html)

* Contributing
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/contributing.md)


# Contributing[¶](#contributing "Permalink to this heading")

We’re excited to collaborate with the community and look forward to the many
improvements you can make to OpenTimelineIO!


## Contributor License Agreement[¶](#contributor-license-agreement "Permalink to this heading")

Before contributing code to OpenTimelineIO, we ask that you sign a Contributor
License Agreement (CLA). When you create a pull request, the Linux Foundation’s
EasyCLA system will guide you through the process of signing the CLA.

If you are unable to use the EasyCLA system, you can send a signed CLA to
`opentimelineio-tsc@aswf.io` (please make sure to include your github username)
and wait for confirmation that we’ve received it.

Here are the two possible CLAs:

* [OTIO\_CLA\_Corporate.pdf](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/raw/main/OTIO_CLA_Corporate.pdf):
  please sign this one for corporate use
* [OTIO\_CLA\_Individual.pdf](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/raw/main/OTIO_CLA_Individual.pdf):
  please sign this one if you’re an individual contributor


## Coding Conventions[¶](#coding-conventions "Permalink to this heading")

Please follow the coding convention and style in each file and in each library
when adding new files.


## Platform Support Policy[¶](#platform-support-policy "Permalink to this heading")

As recomended by the [VFX Platform](https://vfxplatform.com) (see “Support
Guidance”), we support the intended calendar year of the release as well as the
three prior years.


## Git Workflow[¶](#git-workflow "Permalink to this heading")

Here is the workflow we recommend for working on OpenTimelineIO if you intend on
contributing changes back:

Post an issue on github to let folks know about the feature or bug that you
found, and mention that you intend to work on it. That way, if someone else is
working on a similar project, you can collaborate, or you can get early feedback
which can sometimes save time.

Use the github website to fork your own private repository.

Clone your fork to your local machine, like this:

```
git clone https://github.com/you/OpenTimelineIO.git

```

Add the primary OpenTimelineIO repo as upstream to make it easier to update your
remote and local repos with the latest changes:

```
cd OpenTimelineIO
git remote add upstream https://github.com/AcademySoftwareFoundation/OpenTimelineIO.git

```

Now you fetch the latest changes from the OpenTimelineIO repo like this:

```
git fetch upstream
git merge upstream/main

```

All the development should happen against the `main` branch. We recommend you
create a new branch for each feature or fix that you’d like to make and give it
a descriptive name so that you can remember it later. You can checkout a new
branch and create it simultaneously like this:

```
git checkout -b mybugfix upstream/main

```

Now you can work in your branch locally.

Once you are happy with your change, you can verify that the change didn’t cause
tests failures by running tests like this:

```
make test
make lint

```

If all the tests pass and you’d like to send your change in for consideration,
push it to your remote repo:

```
git push origin mybugfix

```

Now your remote branch will have your `mybugfix` branch, which you can now pull
request (to OpenTimelineIO’s `main` branch) using the github UI.

Please make sure that your pull requests are clean. Use the rebase and squash
git facilities as needed to ensure that the pull request is as clean as
possible.

---



## Page 36: Older.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/cxx/older.html](https://opentimelineio.readthedocs.io/en/stable/cxx/older.html)

* Writing OTIO in C, C++ or Python (June 2018)
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/cxx/older.md)


# Writing OTIO in C, C++ or Python (June 2018)[¶](#writing-otio-in-c-c-or-python-june-2018 "Permalink to this heading")

Here are some initial thoughts about the subject, from around June 2018, about
providing languages other than Python. The actual current plan is
[here](cxx.html).

The current python implementation of OTIO has been super helpful for defining
the library and getting studio needs settled, but in order to integrate the
library into vendor tools, a C/C++ implementation is required. We don’t want to
give up the Python API, however, so the plan is to port the library to C/C++
with a Python wrapper that implements an interface to the library as it
currently stands; existing Python code shouldn’t notice the switch. We can use
the existing unit tests to vet the implementation and make sure that it matches
the Python API.

There are several options for how to wrap C/C++ in Python, the intent of this
document is to discuss the options we see and their pros/cons.


## Python C-API[¶](#python-c-api "Permalink to this heading")

link: [Python C-API](https://docs.python.org/2/c-api/index.html)

Pros:

* No extra dependencies

Cons:

* Extremely boilerplate heavy
* Have to manually build every part of the binding
* For users of boost, the bindings won’t be directly compatible with boost
  bindings.
* Error prone: less type-safe and the reference counting must be manually done


## Boost-Python[¶](#boost-python "Permalink to this heading")

link:
[Boost-python](http://www.boost.org/doc/libs/1_64_0/libs/python/doc/html/index.html)

Pros:

* High level binding
* Established, familiarity around the industry, reasonably popular

Cons:

* Heavy dependency to add to projects if they aren’t already using boost


## PyBind11[¶](#pybind11 "Permalink to this heading")

link: [PyBind11 Github](https://github.com/pybind/pybind11)

Pros:

* High level binding
* Takes advantage of C++11/17 features to make wrapping even more terse (if
  they’re available)
* Can be embedded in the project without requiring Boost

Cons:

* For users of boost, the bindings won’t be directly compatible with boost
  bindings.
* Newer and less established than other options.


## Conclusion[¶](#conclusion "Permalink to this heading")

After talking with several vendors, studios, and participants, we have concluded
that we will make this:

* C++ Implementation of OTIO (following VFX Platform CY2017 standard C++11)
* Pybind11 Bindings
* To support other languages will make a `extern "C"` wrapper around the C++ API
* Support for Swift (with some bridging provided by NSObject derived classes
  written in Objective-C++)

This will replace the current pure-Python implementation, attempting to match
the current Python API as much as possible, so that existing Python programs
that use OTIO should not need to be modified to make the switch.

We will try to make this a smooth transition, by starting with `opentime` and
working out to the rest of the API.

Also, in the future, we will likely provide Boost Python bindings to the C++ API
for applications that already use Boost Python.

---



## Page 37: Opentimelineio.Opentime.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.opentime.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.opentime.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.opentime
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.opentime.rst)


# opentimelineio.opentime[¶](#module-opentimelineio.opentime "Permalink to this heading")

*class* opentimelineio.opentime.RationalTime(*value: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 0*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 1*)[¶](#opentimelineio.opentime.RationalTime "Permalink to this definition")

The RationalTime class represents a measure of time of \(rt.value/rt.rate\)
seconds. It can be rescaled into another
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime")’s rate.

almost\_equal(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *delta: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 0*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.almost_equal "Permalink to this definition")ceil() → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.ceil "Permalink to this definition")*static* duration\_from\_start\_end\_time(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_exclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.duration_from_start_end_time "Permalink to this definition")

Compute the duration of samples from first to last (excluding last). This is not
the same as distance.

For example, the duration of a clip from frame 10 to frame 15 is 5 frames.
Result will be in the rate of start\_time.

*static* duration\_from\_start\_end\_time\_inclusive(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_inclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.duration_from_start_end_time_inclusive "Permalink to this definition")

Compute the duration of samples from first to last (including last). This is not
the same as distance.

For example, the duration of a clip from frame 10 to frame 15 is 6 frames.
Result will be in the rate of start\_time.

floor() → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.floor "Permalink to this definition")*static* from\_frames(*frame: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.from_frames "Permalink to this definition")

Turn a frame number and rate into a
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") object.

*static* from\_seconds(*seconds: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.from_seconds "Permalink to this definition")*static* from\_seconds(*seconds: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")

Overloaded function.

1. from\_seconds(seconds: float, rate: float) ->
   opentimelineio.\_opentime.RationalTime
2. from\_seconds(seconds: float) -> opentimelineio.\_opentime.RationalTime
*static* from\_time\_string(*time\_string: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.from_time_string "Permalink to this definition")

Convert a time with microseconds string (`HH:MM:ss` where `ss` is an integer or
a decimal number) into a [`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime").

*static* from\_timecode(*timecode: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.from_timecode "Permalink to this definition")

Convert a timecode string (`HH:MM:SS;FRAME`) into a
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime").

is\_invalid\_time() → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.is_invalid_time "Permalink to this definition")

Returns true if the time is invalid. The time is considered invalid if the value
or the rate are a NaN value or if the rate is less than or equal to zero.

*static* is\_valid\_timecode\_rate(*rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.is_valid_timecode_rate "Permalink to this definition")

Returns true if the rate is valid for use with timecode.

*static* nearest\_valid\_timecode\_rate(*rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.nearest_valid_timecode_rate "Permalink to this definition")

Returns the first valid timecode rate that has the least difference from the
given value.

*property* rate[¶](#opentimelineio.opentime.RationalTime.rate "Permalink to this definition")rescaled\_to(*new\_rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.rescaled_to "Permalink to this definition")rescaled\_to(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")

Overloaded function.

1. rescaled\_to(new\_rate: float) -> opentimelineio.\_opentime.RationalTime

Returns the time value for time converted to new\_rate.

2. rescaled\_to(other: opentimelineio.\_opentime.RationalTime) ->
   opentimelineio.\_opentime.RationalTime

Returns the time for time converted to new\_rate.

round() → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.RationalTime.round "Permalink to this definition")strictly\_equal(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.strictly_equal "Permalink to this definition")to\_frames() → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.to_frames "Permalink to this definition")to\_frames(*rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.12)")

Overloaded function.

1. to\_frames() -> int

Returns the frame number based on the current rate.

2. to\_frames(rate: float) -> int

Returns the frame number based on the given rate.

to\_nearest\_timecode(*rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*, *drop\_frame: Optional[[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")]*) → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.to_nearest_timecode "Permalink to this definition")to\_nearest\_timecode(*rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")to\_nearest\_timecode() → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")

Overloaded function.

1. to\_nearest\_timecode(rate: float, drop\_frame: Optional[bool]) -> str

Convert to nearest timecode (`HH:MM:SS;FRAME`)

2. to\_nearest\_timecode(rate: float) -> str
3. to\_nearest\_timecode() -> str
to\_seconds() → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.to_seconds "Permalink to this definition")to\_time\_string() → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.to_time_string "Permalink to this definition")to\_timecode(*rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*, *drop\_frame: Optional[[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")]*) → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.to_timecode "Permalink to this definition")to\_timecode(*rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")to\_timecode() → [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")

Overloaded function.

1. to\_timecode(rate: float, drop\_frame: Optional[bool]) -> str

Convert to timecode (`HH:MM:SS;FRAME`)

2. to\_timecode(rate: float) -> str
3. to\_timecode() -> str
*property* value[¶](#opentimelineio.opentime.RationalTime.value "Permalink to this definition")value\_rescaled\_to(*new\_rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")[¶](#opentimelineio.opentime.RationalTime.value_rescaled_to "Permalink to this definition")value\_rescaled\_to(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")

Overloaded function.

1. value\_rescaled\_to(new\_rate: float) -> float

Returns the time value for “self” converted to new\_rate.

2. value\_rescaled\_to(other: opentimelineio.\_opentime.RationalTime) -> float
*class* opentimelineio.opentime.TimeRange(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime") = None*, *duration: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime") = None*)[¶](#opentimelineio.opentime.TimeRange "Permalink to this definition")

The TimeRange class represents a range in time. It encodes the start time and
the duration, meaning that
[`end_time_inclusive()`](#opentimelineio.opentime.TimeRange.end_time_inclusive

"opentimelineio.opentime.TimeRange.end_time_inclusive") (last portion of a
sample in the time range) and
[`end_time_exclusive()`](#opentimelineio.opentime.TimeRange.end_time_exclusive

"opentimelineio.opentime.TimeRange.end_time_exclusive") can be computed.

before(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.TimeRange.before "Permalink to this definition")before(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")

Overloaded function.

1. before(other: opentimelineio.\_opentime.RationalTime, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The end of this strictly precedes other by a value >= epsilon\_s.

```
          other
            ↓
[ this ]    *

```

2. before(other: opentimelineio.\_opentime.TimeRange, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The end of this strictly equals the start of other and the start of this
strictly equals the end of other.

```
[this][other]

```

The converse would be `other.meets(this)`

begins(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.TimeRange.begins "Permalink to this definition")begins(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")

Overloaded function.

1. begins(other: opentimelineio.\_opentime.RationalTime, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The start of this strictly equals other.

```
other
  ↓
  *
  [ this ]

```

2. begins(other: opentimelineio.\_opentime.TimeRange, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The start of this strictly equals the start of other. The end of this strictly
precedes the end of other by a value >= epsilon\_s.

```
[ this ]
[    other    ]

```

The converse would be `other.begins(this)`

clamped(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.TimeRange.clamped "Permalink to this definition")clamped(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")

Overloaded function.

1. clamped(other: opentimelineio.\_opentime.RationalTime) ->
   opentimelineio.\_opentime.RationalTime

Clamp ‘other’ ([`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime")) according to
[`start_time`](#opentimelineio.opentime.TimeRange.start_time

"opentimelineio.opentime.TimeRange.start_time")/[`end_time_exclusive`](#opentimelineio.opentime.TimeRange.end_time_exclusive

"opentimelineio.opentime.TimeRange.end_time_exclusive") and bound arguments.

2. clamped(other: opentimelineio.\_opentime.TimeRange) ->
   opentimelineio.\_opentime.TimeRange

Clamp ‘other’ ([`TimeRange`](#opentimelineio.opentime.TimeRange

"opentimelineio.opentime.TimeRange")) according to
[`start_time`](#opentimelineio.opentime.TimeRange.start_time

"opentimelineio.opentime.TimeRange.start_time")/[`end_time_exclusive`](#opentimelineio.opentime.TimeRange.end_time_exclusive

"opentimelineio.opentime.TimeRange.end_time_exclusive") and bound arguments.

contains(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.TimeRange.contains "Permalink to this definition")contains(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")

Overloaded function.

1. contains(other: opentimelineio.\_opentime.RationalTime) -> bool

The start of this precedes other. other precedes the end of this.

```
      other
        ↓
        *
[      this      ]

```

2. contains(other: opentimelineio.\_opentime.TimeRange, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The start of this precedes start of other. The end of this antecedes end of
other.

```
     [ other ]
[      this      ]

```

The converse would be `other.contains(this)`

*property* duration[¶](#opentimelineio.opentime.TimeRange.duration "Permalink to this definition")duration\_extended\_by(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.opentime.TimeRange.duration_extended_by "Permalink to this definition")end\_time\_exclusive() → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.TimeRange.end_time_exclusive "Permalink to this definition")

Time of the first sample outside the time range.

If start frame is 10 and duration is 5, then end\_time\_exclusive is 15, because
the last time with data in this range is 14.

If start frame is 10 and duration is 5.5, then end\_time\_exclusive is 15.5,
because the last time with data in this range is 15.

end\_time\_inclusive() → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.TimeRange.end_time_inclusive "Permalink to this definition")

The time of the last sample containing data in the time range.

If the time range starts at (0, 24) with duration (10, 24), this will be (9, 24)

If the time range starts at (0, 24) with duration (10.5, 24): (10, 24)

In other words, the last frame with data, even if the last frame is fractional.

extended\_by(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.opentime.TimeRange.extended_by "Permalink to this definition")

Construct a new [`TimeRange`](#opentimelineio.opentime.TimeRange

"opentimelineio.opentime.TimeRange") that is this one extended by other.

finishes(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.TimeRange.finishes "Permalink to this definition")finishes(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")

Overloaded function.

1. finishes(other: opentimelineio.\_opentime.RationalTime, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The end of this strictly equals other.

```
     other
       ↓
       *
[ this ]

```

2. finishes(other: opentimelineio.\_opentime.TimeRange, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The start of this strictly antecedes the start of other by a value >=
epsilon\_s. The end of this strictly equals the end of other.

```
        [ this ]
[     other    ]

```

The converse would be `other.finishes(this)`

intersects(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.TimeRange.intersects "Permalink to this definition")

The start of this precedes or equals the end of other by a value >= epsilon\_s.
The end of this antecedes or equals the start of other by a value >= epsilon\_s.

```
[    this    ]           OR      [    other    ]
     [     other    ]                    [     this    ]

```

The converse would be `other.finishes(this)`

meets(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.TimeRange.meets "Permalink to this definition")

The end of this strictly equals the start of other and the start of this
strictly equals the end of other.

```
[this][other]

```

The converse would be `other.meets(this)`

overlaps(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")[¶](#opentimelineio.opentime.TimeRange.overlaps "Permalink to this definition")overlaps(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*, *epsilon\_s: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 2.6041666666666666e-06*) → [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.12)")

Overloaded function.

1. overlaps(other: opentimelineio.\_opentime.RationalTime) -> bool

this contains other.

```
     other
      ↓
      *
[    this    ]

```

2. overlaps(other: opentimelineio.\_opentime.TimeRange, epsilon\_s: float =
   2.6041666666666666e-06) -> bool

The start of this strictly precedes end of other by a value >= epsilon\_s. The
end of this strictly antecedes start of other by a value >= epsilon\_s.

```
[ this ]
    [ other ]

```

The converse would be `other.overlaps(this)`

*static* range\_from\_start\_end\_time(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_exclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.opentime.TimeRange.range_from_start_end_time "Permalink to this definition")

Creates a [`TimeRange`](#opentimelineio.opentime.TimeRange

"opentimelineio.opentime.TimeRange") from start and end
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime")s (exclusive).

For example, if start\_time is 1 and end\_time is 10, the returned will have a
duration of 9.

*static* range\_from\_start\_end\_time\_inclusive(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_inclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.opentime.TimeRange.range_from_start_end_time_inclusive "Permalink to this definition")

Creates a [`TimeRange`](#opentimelineio.opentime.TimeRange

"opentimelineio.opentime.TimeRange") from start and end
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime")s (inclusive).

For example, if start\_time is 1 and end\_time is 10, the returned will have a
duration of 10.

*property* start\_time[¶](#opentimelineio.opentime.TimeRange.start_time "Permalink to this definition")*class* opentimelineio.opentime.TimeTransform(*offset: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime") = otio.opentime.RationalTime(value=0, rate=1)*, *scale: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = 1*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") = -1*)[¶](#opentimelineio.opentime.TimeTransform "Permalink to this definition")

1D transform for [`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime"). Has offset and scale.

applied\_to(*other: [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.opentime.TimeTransform.applied_to "Permalink to this definition")applied\_to(*other: [opentimelineio.\_opentime.TimeTransform](#opentimelineio.opentime.TimeTransform "opentimelineio._opentime.TimeTransform")*) → [opentimelineio.\_opentime.TimeTransform](#opentimelineio.opentime.TimeTransform "opentimelineio._opentime.TimeTransform")applied\_to(*other: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")

Overloaded function.

1. applied\_to(other: opentimelineio.\_opentime.TimeRange) ->
   opentimelineio.\_opentime.TimeRange
2. applied\_to(other: opentimelineio.\_opentime.TimeTransform) ->
   opentimelineio.\_opentime.TimeTransform
3. applied\_to(other: opentimelineio.\_opentime.RationalTime) ->
   opentimelineio.\_opentime.RationalTime
*property* offset[¶](#opentimelineio.opentime.TimeTransform.offset "Permalink to this definition")*property* rate[¶](#opentimelineio.opentime.TimeTransform.rate "Permalink to this definition")*property* scale[¶](#opentimelineio.opentime.TimeTransform.scale "Permalink to this definition")opentimelineio.opentime.duration\_from\_start\_end\_time(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_exclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.duration_from_start_end_time "Permalink to this definition")

Compute the duration of samples from first to last (excluding last). This is not
the same as distance.

For example, the duration of a clip from frame 10 to frame 15 is 5 frames.
Result will be in the rate of start\_time.

opentimelineio.opentime.duration\_from\_start\_end\_time\_inclusive(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_inclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.duration_from_start_end_time_inclusive "Permalink to this definition")

Compute the duration of samples from first to last (including last). This is not
the same as distance.

For example, the duration of a clip from frame 10 to frame 15 is 6 frames.
Result will be in the rate of start\_time.

opentimelineio.opentime.from\_frames(*frame: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.from_frames "Permalink to this definition")

Turn a frame number and rate into a
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") object.

opentimelineio.opentime.from\_seconds(*seconds: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.from_seconds "Permalink to this definition")opentimelineio.opentime.from\_seconds(*seconds: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")

Overloaded function.

1. from\_seconds(seconds: float, rate: float) ->
   opentimelineio.\_opentime.RationalTime
2. from\_seconds(seconds: float) -> opentimelineio.\_opentime.RationalTime
opentimelineio.opentime.from\_time\_string(*time\_string: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.from_time_string "Permalink to this definition")

Convert a time with microseconds string (`HH:MM:ss` where `ss` is an integer or
a decimal number) into a [`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime").

opentimelineio.opentime.from\_timecode(*timecode: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.12)")*, *rate: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)")*) → [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")[¶](#opentimelineio.opentime.from_timecode "Permalink to this definition")

Convert a timecode string (`HH:MM:SS;FRAME`) into a
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime").

opentimelineio.opentime.range\_from\_start\_end\_time(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_exclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.opentime.range_from_start_end_time "Permalink to this definition")

Creates a [`TimeRange`](#opentimelineio.opentime.TimeRange

"opentimelineio.opentime.TimeRange") from start and end
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime")s (exclusive).

For example, if start\_time is 1 and end\_time is 10, the returned will have a
duration of 9.

opentimelineio.opentime.range\_from\_start\_end\_time\_inclusive(*start\_time: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*, *end\_time\_inclusive: [opentimelineio.\_opentime.RationalTime](#opentimelineio.opentime.RationalTime "opentimelineio._opentime.RationalTime")*) → [opentimelineio.\_opentime.TimeRange](#opentimelineio.opentime.TimeRange "opentimelineio._opentime.TimeRange")[¶](#opentimelineio.opentime.range_from_start_end_time_inclusive "Permalink to this definition")

Creates a [`TimeRange`](#opentimelineio.opentime.TimeRange

"opentimelineio.opentime.TimeRange") from start and end
[`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime")s (inclusive).

For example, if start\_time is 1 and end\_time is 10, the returned will have a
duration of 10.

opentimelineio.opentime.to\_frames(*rt*, *rate=None*)[¶](#opentimelineio.opentime.to_frames "Permalink to this definition")

Turn a [`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") into a frame number.

opentimelineio.opentime.to\_nearest\_timecode(*rt*, *rate=None*, *drop\_frame=None*)[¶](#opentimelineio.opentime.to_nearest_timecode "Permalink to this definition")

Convert a [`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") into a timecode string.

opentimelineio.opentime.to\_seconds(*rt*)[¶](#opentimelineio.opentime.to_seconds "Permalink to this definition")

Convert a [`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") into float seconds

opentimelineio.opentime.to\_time\_string(*rt*)[¶](#opentimelineio.opentime.to_time_string "Permalink to this definition")

Convert this timecode to time as used by ffmpeg, formatted as `hh:mm:ss` where
ss is an integer or decimal number.

opentimelineio.opentime.to\_timecode(*rt*, *rate=None*, *drop\_frame=None*)[¶](#opentimelineio.opentime.to_timecode "Permalink to this definition")

Convert a [`RationalTime`](#opentimelineio.opentime.RationalTime

"opentimelineio.opentime.RationalTime") into a timecode string.

---



## Page 38: Architecture.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/architecture.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/architecture.html)

* Architecture
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/architecture.md)


# Architecture[¶](#architecture "Permalink to this heading")


## Overview[¶](#overview "Permalink to this heading")

OpenTimelineIO is an open source library for the interchange of editorial
information. This document describes the structure of the python library.

To import the library into python: `import opentimelineio as otio`


## Canonical Structure[¶](#canonical-structure "Permalink to this heading")

Although you can compose your OTIO files differently if you wish, the canonical
OTIO structure is as follows:

* root: `otio.schema.Timeline` This file contains information about the root of a
  timeline, including a `global_start_time` and a top level container, `tracks`
* `timeline.tracks`: This member is a `otio.schema.Stack` which contains
  `otio.schema.Track` objects
* `timeline.tracks[i]`: The `otio.schema.Track` contained by a `timeline.tracks`
  object contains the clips, transitions and subcontainers that compose the rest
  of the editorial data


## Modules[¶](#modules "Permalink to this heading")

The most interesting pieces of OTIO to a developer integrating OTIO into another
application or workflow are:

* `otio.schema`: The classes that describe the in-memory OTIO representation
* `otio.opentime`: Classes and utility functions for representing time, time
  ranges and time transforms
* `otio.adapters`: Modules that can read/write to or from an on-disk format and
  the in-memory OTIO representation

Additionally, for developers integrating OTIO into a studio pipeline:

* `otio.media_linker`: Plugin system for writing studio or workflow specific media
  linkers that run after adapters read files

The in-memory OTIO representation data model is rooted at an
`otio.schema.Timeline` which has a member `tracks` which is a
`otio.schema.Stack` of `otio.schema.Track`, which contain a list of items such
as:

* `otio.schema.Clip`
* `otio.schema.Gap`
* `otio.schema.Stack`
* `otio.schema.Track`
* `otio.schema.Transition`

The `otio.schema.Clip` objects can reference media through a
`otio.schema.ExternalReference` or indicate that they are missing a reference to
real media with a `otio.schema.MissingReference`. All objects have a metadata
dictionary for blind data.

Schema composition objects (`otio.schema.Stack` and `otio.schema.Track`)
implement the python mutable sequence API. A simple script that prints out each
shot might look like:

```
import opentimelineio as otio


# read the timeline into memory

tl = otio.adapters.read_from_file("my_file.otio")

for each_seq in tl.tracks:
    for each_item in each_seq:
        if isinstance(each_item, otio.schema.Clip):
            print each_item.media_reference

```

Or, in the case of a nested composition, like this:

```
import opentimelineio as otio


# read the timeline into memory

tl = otio.adapters.read_from_file("my_file.otio")

for clip in tl.each_clip():
    print clip.media_reference

```


## Time on otio.schema.Clip[¶](#time-on-otio-schema-clip "Permalink to this heading")

A clip may set its timing information (which is used to compute its `duration()`
or its `trimmed_range()`) by configuring either its:

* `media_reference.available_range` This is the range of the available media that
  can be cut in. So for example, frames 10-100 have been rendered and prepared for
  editorial.
* `source_range` The range of media that is cut into the sequence, in the space of
  the available range (if it is set). In other words, it further truncates the
  available\_range.

A clip must have at least one set or else its duration is not computable:

```
cl.duration()

# raises: opentimelineio._otio.CannotComputeAvailableRangeError: Cannot compute available range: No available_range set on media reference on clip: Clip("", ExternalReference("file:///example.mov"), None, {})

```

You may query the `available_range` and `trimmed_range` via accessors on the
`Clip()` itself, for example:

```
cl.trimmed_range()
cl.available_range() # == cl.media_reference.available_range

```

Generally, if you want to know the range of a clip, we recommend using the
`trimmed_range()` method, since this takes both the
`media_reference.available_range` and the `source_range` into consideration.


## Time On Clips in Containers[¶](#time-on-clips-in-containers "Permalink to this heading")

Additionally, if you want to know the time of a clip in the context of a
container, you can use the local: `trimmed_range_in_parent()` method, or a
parent’s `trimmed_range_of_child()`. These will additionally take into
consideration the `source_range` of the parent container, if it is set. They
return a range in the space of the specified parent container.


## otio.opentime[¶](#otio-opentime "Permalink to this heading")

Opentime encodes timing related information.


### RationalTime[¶](#rationaltime "Permalink to this heading")

A point in time at `rt.value*(1/rt.rate)` seconds. Can be rescaled into another
RationalTime’s rate.


### TimeRange[¶](#timerange "Permalink to this heading")

A range in time. Encodes the start time and the duration, meaning that
end\_time\_inclusive (last portion of a sample in the time range) and
end\_time\_exclusive can be computed.


## otio.adapters[¶](#otio-adapters "Permalink to this heading")

OpenTimelineIO includes several adapters for reading and writing from other file
formats. The `otio.adapters` module has convenience functions that will
auto-detect which adapter to use, or you can specify the one you want.

Adapters can be added to the system (outside of the distribution) via JSON files
that can be placed on the
[OTIO\_PLUGIN\_MANIFEST\_PATH](otio-env-variables.html#term-OTIO_PLUGIN_MANIFEST_PATH)

environment variable to be made available to OTIO.

Most common usage only cares about:

* `timeline = otio.adapters.read_from_file(filepath)`
* `timeline = otio.adapters.read_from_string(rawtext, adapter_name)`
* `otio.adapters.write_to_file(timeline, filepath)`
* `rawtext = otio.adapters.write_to_string(timeline, adapter_name)`

The native format serialization (`.otio` files) is handled via the “otio\_json”
adapter, `otio.adapters.otio_json`.

In most cases you don’t need to worry about adapter names, just use
`otio.adapters.read_from_file()` and `otio.adapters.write_to_file` and it will
figure out which one to use based on the filename extension.

For more information, see [How To Write An OpenTimelineIO
Adapter](write-an-adapter.html).


## otio.media\_linkers[¶](#otio-media-linkers "Permalink to this heading")

Media linkers run on the otio file after an adapter calls `.read_from_file()` or
`.read_from_string()`. They are intended to replace media references that exist
after the adapter runs (which depending on the adapter are likely to be
`MissingReference`) with ones that point to valid files in the local system.
Since media linkers are plugins, they can use proprietary knowledge or context
and do not need to be part of OTIO itself.

You may also specify a media linker to be run after the adapter, either via the
`media_linker_name` argument to `.read_from_file()` or `.read_from_string()` or
via the
[OTIO\_DEFAULT\_MEDIA\_LINKER](otio-env-variables.html#term-OTIO_DEFAULT_MEDIA_LINKER)

environment variable. You can also turn the media linker off completely by
setting the `media_linker_name` argument to
`otio.media_linker.MediaLinkingPolicy.DoNotLinkMedia`.

For more information about writing media linkers, see [How To Write An
OpenTimelineIO Media Linker](write-a-media-linker.html).


## Example Scripts[¶](#example-scripts "Permalink to this heading")

Example scripts are located in the [examples
subdirectory](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/tree/main/examples).

---



## Page 39: Quickstart.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/quickstart.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/quickstart.html)

* Quickstart
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/quickstart.md)


# Quickstart[¶](#quickstart "Permalink to this heading")

This is for users who wish to get started using the “OTIOView” application to
inspect the contents of editorial timelines.

**Note** This guide assumes that you are working inside a
[virtualenv](https://virtualenv.pypa.io/en/latest/).


## Install Prerequisites[¶](#install-prerequisites "Permalink to this heading")

OTIOView has an additional prerequisite to OTIO:

* Try `python -m pip install PySide2` or `python -m pip install PySide6`
* If difficulties are encountered, please file an issue on OpenTimelineIO’s github
  for assistance.


## Install OTIO[¶](#install-otio "Permalink to this heading")

* `python -m pip install opentimelineio`


## Setup Any Additional Adapters You May Want[¶](#setup-any-additional-adapters-you-may-want "Permalink to this heading")

A default OTIO installation includes only the “Core” adapters, which include the
native OTIO JSON format (`.otio`), OpenTimelineIO directory bundles (`.otiod`),
and OpenTimelineIO ZIP bundles (`.otiod`).

A curated list of adapters for popular file formats like EDL, AAF, ALE, and FCP
XML can be installed using the [OpenTimelineIO Plugins package in
PyPI](https://pypi.org/project/OpenTimelineIO-Plugins/). These plugins can also
be individually installed from their PyPI packages.

For mor information, see the [Adapters](adapters.html) section.


## Run OTIOView[¶](#run-otioview "Permalink to this heading")

Once you have pip installed OpenTimelineIO, you should be able to run:

* `otioview path/to/your/file.edl`


# Developer Quickstart[¶](#developer-quickstart "Permalink to this heading")

Get the source and submodules:

* `git clone git@github.com:AcademySoftwareFoundation/OpenTimelineIO.git`

Before reading further, it is good to note that there is two parts to the C++
code: the OTIO C++ library that you can use in your C++ projects, and the C++
Python bindings that makes the C++ library available in Python.


## To build OTIO for C++ development:[¶](#to-build-otio-for-c-development "Permalink to this heading")


### Linux/Mac[¶](#linux-mac "Permalink to this heading")

```
    mkdir build
    cd build
    cmake .. { options }
    make install

```


### Windows - in an “x64 Native Tools Command Prompt” for Visual Studio[¶](#windows-in-an-x64-native-tools-command-prompt-for-visual-studio "Permalink to this heading")

```
    mkdir build
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX={path/to/install/location} { options }
    cmake --build . --target install --config Release

```

The `CMAKE_INSTALL_PREFIX` variable must be set to a path with no spaces in it,
because CMake’s default install location is in `C:\Program Files`, which won’t
work with OpenTimelineIO due to spaces in the path.


## To build OTIO for Python development:[¶](#to-build-otio-for-python-development "Permalink to this heading")

* `python -m pip install -e .`


## To build OTIO for both C++ and Python development:[¶](#to-build-otio-for-both-c-and-python-development "Permalink to this heading")

The Python package is a mix of pure python and C++ code. Therefore, it is
recommended to use the python tooling (`python -m pip`) to develop both the C++
binding and the pure python code. We use `setuptools` as our python build
backend, which means `pip` will call the `setup.py` in the root of the directory
to build both the pure python and the C++ bindings. `setuptools` will take care
of all the complexity of building a C++ Python extension for you.

The first time `setup.py` is run, cmake scripts will be created, and the headers
and libraries will be installed where you specify. If the C++ or Python sources
are subsequently modified, running this command again will build and update
everything appropriately.

**Note** Any CMake arguments can be passed through `pip` by using the
`CMAKE_ARGS` environment variable when building from source. \*nix Example:

```
env CMAKE_ARGS="-DCMAKE_VAR=VALUE1 -DCMAKE_VAR_2=VALUE2" python -m pip install .

```

`python -m pip install .` adds some overhead that might be annoying or unwanted
when developing the python bindings. For that reason (and only that reason), if
you want a faster iteration process, you can use `setuptools` commands. For
example you can use `python setup.py build_ext` to only run the compilation
step. Be aware that calling `setup.py` directly is highly discouraged and should
only be used when no of the other options are viable. See
https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html.

To compile your own C++ file referencing the OTIO headers from your C++ build
using gcc or clang, add the following -I flags:

* `c++ -c source.cpp -I/home/someone/cxx-otio-root/include
  -I/home/someone/cxx-otio-root/include/opentimelineio/deps`

To link your own program against your OTIO build using gcc or clang, add the
following -L/-l flags:

* `c++ ... -L/home/someone/cxx-otio-root/lib -lopentimelineio`

To use opentime without opentimelineio, link with -lopentime instead, and
compile with:

* `c++ -c source.cpp -I/home/someone/cxx-otio-root/include`


# Debugging Quickstart[¶](#debugging-quickstart "Permalink to this heading")


## Linux / GDB / LLDB[¶](#linux-gdb-lldb "Permalink to this heading")

To compile in debug mode, set the `OTIO_CXX_DEBUG_BUILD` environment variable to
any value and then `python -m pip install`.

You can then attach GDB to python and run your program:

* `gdb --args python script_you_want_to_debug.py`

Or LLDB:

* `lldb -- python script_you_want_to_debug.py`

One handy tip is that you can trigger a breakpoint in gdb by inserting a SIGINT:

```
        #include <csignal>

        // ...
        std::raise(SIGINT);

```

GDB will automatically break when it hits the SIGINT line.


# How to Generate the C++ Documentation:[¶](#how-to-generate-the-c-documentation "Permalink to this heading")


## Mac / Linux[¶](#mac-linux "Permalink to this heading")

The doxygen docs can be generated with the following commands:

```
cd doxygen ; doxygen config/dox_config ; cd ..

```

Another option is to trigger the make target:

```
make doc-cpp

```

---



## Page 40: Opentimelineio.Url Utils.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.url_utils.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.url_utils.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* opentimelineio.url\_utils
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.url_utils.rst)


# opentimelineio.url\_utils[¶](#module-opentimelineio.url_utils "Permalink to this heading")

Utilities for conversion between urls and file paths

opentimelineio.url\_utils.filepath\_from\_url(*urlstr*)[¶](#opentimelineio.url_utils.filepath_from_url "Permalink to this definition")

Take an url and return a filepath.

URLs can either be encoded according to the [RFC
3986](https://tools.ietf.org/html/rfc3986#section-2.1) standard or not.

Additionally, Windows mapped drive letter and UNC paths need to be accounted for
when processing URL(s); however, there are [ongoing
discussions](https://discuss.python.org/t/file-uris-in-python/15600) about how
to best handle this within Python developer community. This function is meant to
cover these scenarios in the interim.

opentimelineio.url\_utils.url\_from\_filepath(*fpath*)[¶](#opentimelineio.url_utils.url_from_filepath "Permalink to this definition")

Convert a filesystem path to an url in a portable way using / path sep

---



## Page 41: Otio Filebundles.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-filebundles.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/otio-filebundles.html)

* File Bundles
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/otio-filebundles.md)


# File Bundles[¶](#file-bundles "Permalink to this heading")


## Overview[¶](#overview "Permalink to this heading")

This document describes OpenTimelineIO’s file bundle formats, otiod and otioz.
The intent is that they make it easier to package and send or archive
OpenTimelineIO data and associated media.


## Source Timeline[¶](#source-timeline "Permalink to this heading")

For creating otio bundles, an OTIO file is used as input, whose media references
are composed only of `ExternalReference` that have a target\_url field pointing
at a media file with a unique basename, because file bundles have a flat
namespace for media. For example, if there are media references that point at:

`/project_a/academy_leader.mov`

and:

`/project_b/academy_leader.mov`

Because the basename of both files is `academy_leader.mov`, this will be an
error. The adapters have different policies for how to handle media references.
See below for more information.


### URL Format[¶](#url-format "Permalink to this heading")

The file bundle adapters expect the `target_url` field of the `media_reference`
to be in one of two forms (as produced by python’s urlparse library):

* absolute path: “file:///path/to/some/file” (encodes “/path/to/some/file”)
* relative path: “path/to/some/file” (assumes the path is relative to the current
  working directory when invoking the adapter).


## Structure[¶](#structure "Permalink to this heading")

File bundles, regardless of how they’re encoded, have a consistent structure:

```
something.otioz
├── content.otio
├── version
└── media
    ├── media1
    ├── media2
    └── media3

```


### content.otio file[¶](#content-otio-file "Permalink to this heading")

This is a normal OpenTimelineIO whose media references are either
ExternalReferences with relative target\_urls pointing into the `media`
directory or `MissingReference`.


### version.txt file[¶](#version-txt-file "Permalink to this heading")

This file encodes the otioz version of the file, in the form 1.0.0.


### Media Directory[¶](#media-directory "Permalink to this heading")

The media directory contains all the media files in a flat structure. They must
have unique basenames, but can be encoded in whichever codec/container the user
wishes (otio is unable to decode or encode the media files).


## Read Behavior[¶](#read-behavior "Permalink to this heading")

When a bundle is read from disk, the `content.otio` file is extracted from the
bundle and returned. For example, to view the timeline (not the media) of an
otioz file in `otioview`, you can run:

`otioview sommething.otioz`

This will *only* read the `content.otio` from the bundle, so is usually a fast
operation to run.


## MediaReferencePolicy[¶](#mediareferencepolicy "Permalink to this heading")

When building a file bundle using the OTIOZ/OTIOD adapters, you can set the
‘media reference policy’, which is described by an enum in the
file\_bundle\_utils module. The policies can be:

* (default) ErrorIfNotFile: will raise an exception if a media reference is found
  that is of type `ExternalReference` but that does not point at a `target_url`.
* MissingIfNotFile: will replace any media references that meet the above
  condition with a `MissingReference`, preserving the original media reference in
  the metadata of the new `MissingReference`.
* AllMissing: will replace all media references with `MissingReference`,
  preserving the original media reference in metadata on the new object.

When running in `AllMissing` mode, no media will be put into the bundle.


## OTIOD[¶](#otiod "Permalink to this heading")

The OTIOD adapter will build a bundle in a directory stucture on disk. The
adapter will gather up all the files it can and copy them to the destination
directory, and then build the `.otio` file with local relative path references
into that directory.


## OTIOZ[¶](#otioz "Permalink to this heading")

The OTIOZ adapter will build a bundle into a zipfile (using the zipfile
library). The adapter will write media into the zip file uncompressed and the
content.otio with compression.


### Optional Arguments:[¶](#optional-arguments "Permalink to this heading")

* Read:

  + extract\_to\_directory: if a value other than `None` is passed in, will extract
    the contents of the bundle into the directory at the path passed into the
    `extract_to_directory` argument.


## Example usage in otioconvert[¶](#example-usage-in-otioconvert "Permalink to this heading")


### Convert an otio into a zip bundle[¶](#convert-an-otio-into-a-zip-bundle "Permalink to this heading")

`otioconvert -i somefile.otio -o /var/tmp/somefile.otioz`


### Extract the contents of the bundle and convert to an rv playlist[¶](#extract-the-contents-of-the-bundle-and-convert-to-an-rv-playlist "Permalink to this heading")

`otioconvert -i /var/tmp/somefile.otioz -a
extract_to_directory=/var/tmp/somefile -o /var/tmp/somefile/somefile.rv`

---



## Page 42: Write An Adapter.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/write-an-adapter.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/write-an-adapter.html)

* Writing an OTIO Adapter
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/write-an-adapter.md)


# Writing an OTIO Adapter[¶](#writing-an-otio-adapter "Permalink to this heading")

OpenTimelineIO Adapters are plugins that allow OTIO to read and/or write other
timeline formats.

Users of OTIO can read and write files like this:

```

#/usr/bin/env python

import opentimelineio as otio
mytimeline = otio.adapters.read_from_file("something.edl")
otio.adapters.write_to_file(mytimeline, "something.otio")

```

The otio.adapters module will look at the file extension (in this case “.edl” or
“.otio”) and pick the right adapter to convert to or from the appropriate
format.

Note that the OTIO JSON format is treated like an adapter as well. The “.otio”
format is the only format that is lossless. It can store and retrieve all of the
objects, metadata and features available in OpenTimelineIO. Other formats are
lossy - they will only store and retrieve features that are supported by that
format (and by the adapter implementation). Some adapters may choose to put
extra information, not supported by OTIO, into metadata on any OTIO object.


## Sharing an Adapter You’ve Written With the Community[¶](#sharing-an-adapter-youve-written-with-the-community "Permalink to this heading")

If you’ve written an adapter that might be useful to others, please contact the
[OpenTimelineIO
team](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) so we can add
it to the list of [Tools and Projects Using
OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/wiki/Tools-and-Projects-Using-OpenTimelineIO).
If the adapter is of broad enough interest to adopt as an OTIO community
supported adapter, we can discuss transitioning it to the [OpenTimelineIO GitHub
Organization](https://github.com/OpenTimelineIO/). Keep in mind, code should be
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) or
[MIT](https://opensource.org/licenses/MIT) licensed if it is intended to
transition to the OpenTimelineIO project.


### Packaging and Sharing Custom Adapters[¶](#packaging-and-sharing-custom-adapters "Permalink to this heading")

Adapters may also be organized into their own independent Python project for
subsequent
[packaging](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives),

[distribution](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)

and
[installation](https://packaging.python.org/tutorials/packaging-projects/#installing-your-newly-uploaded-package)

by [`pip`](https://packaging.python.org/key_projects/#pip).

The easist way is to [otio-plugin-template
repo](https://github.com/OpenTimelineIO/otio-plugin-template) and click “Use
this template”. This will get you started with plugin boilerplate and allow you
to develop the adapter in your own GitHub account.

If you’d like to work from scratch, we recommend you organize your project like
so:

```
.
├── setup.py
└── opentimelineio_mystudio
    ├── __init__.py
    ├── plugin_manifest.json
    ├── adapters
    │   ├── __init__.py
    │   ├── my_adapter_x.py
    │   └── my_adapter_y.py
    └── operations
        ├── __init__.py
        └── my_linker.py

```

With a `setup.py` containing this minimum entry set:

```
from setuptools import setup

setup(
    name='OpenTimelineMyStudioAdapters',
    entry_points={
        'opentimelineio.plugins': 'opentimelineio_mystudio = opentimelineio_mystudio'
    },
    package_data={
        'opentimelineio_mystudio': [
            'plugin_manifest.json',
        ],
    },
    version='0.0.1',
    packages=[
        'opentimelineio_mystudio',
        'opentimelineio_mystudio.adapters',
        'opentimelineio_mystudio.operations',
    ],
)

```

And a `plugin_manifest.json` like:

```
{
    "OTIO_SCHEMA" : "PluginManifest.1",
    "adapters" : [
        {
            "OTIO_SCHEMA" : "Adapter.1",
            "name" : "adapter_x",
            "filepath" : "adapters/my_adapter_x.py",
            "suffixes" : ["xxx"]
        },
        {
            "OTIO_SCHEMA" : "Adapter.1",
            "name" : "adapter_y",
            "filepath" : "adapters/my_adapter_y.py",
            "suffixes" : ["yyy", "why"]
        }
    ],
    "media_linkers" : [
        {
            "OTIO_SCHEMA" : "MediaLinker.1",
            "name" : "my_studios_media_linker",
            "filepath" : "operations/my_linker.py"
        }
    ]
}

```


### Custom Adapters[¶](#custom-adapters "Permalink to this heading")

Alternately, if you are creating a site specific adapter that you do *not*
intend to share with the community, you can create your `myadapter.py` file
anywhere. In this case, you must create a `mysite.plugin_manifest.json` (with an
entry like the below example that points at `myadapter.py`) and then put the
path to your `mysite.plugin_manifest.json` on your
[OTIO\_PLUGIN\_MANIFEST\_PATH](otio-env-variables.html#term-OTIO_PLUGIN_MANIFEST_PATH)

environment variable.

For example, to register `myadapter.py` that supports files with a `.myext` file
extension:

```
{
    "OTIO_SCHEMA" : "Adapter.1",
    "name" : "myadapter",
    "filepath" : "myadapter.py",
    "suffixes" : ["myext"]
}

```


## Required Functions[¶](#required-functions "Permalink to this heading")

Each adapter must implement at least one of these functions:

```
def read_from_file(filepath):
    # ...

    return timeline

def read_from_string(input_str):
    # ...

    return timeline

def write_to_string(input_otio):
    # ...

    return text

def write_to_file(input_otio, filepath):
    # ...

    return

```

If your format is text-based, then we recommend that you implement
`read_from_string` and `write_to_string`. The adapter module will automatically
wrap these and allow users to call `read_from_file` and `write_to_file`.


## Constructing a Timeline[¶](#constructing-a-timeline "Permalink to this heading")

To construct a Timeline in the `read_from_string` or `read_from_file` functions,
you can use the API like this:

```
timeline = otio.schema.Timeline()
timeline.name = "Example Timeline"
track = otio.schema.Track()
track.name = "V1"
timeline.tracks.append(track)
clip = otio.schema.Clip()
clip.name = "Wedding Video"
track.append(clip)

```


### Metadata[¶](#metadata "Permalink to this heading")

If your timeline, tracks, clips or other objects have format-specific,
application-specific or studio-specific metadata, then you can add metadata to
any of the OTIO schema objects like this:

```
timeline.metadata["mystudio"] = {
    "showID": "zz"
}
clip.metadata["mystudio"] = {
    "shotID": "zz1234",
    "takeNumber": 17,
    "department": "animation",
    "artist": "hanna"
}

```

Note that all metadata should be nested inside a sub-dictionary (in this example
“mystudio”) so that metadata from other applications, pipeline steps, etc. can
be kept separate. OTIO carries this metadata along blindly, so you can put
whatever you want in there (within reason). Very large data should probably not
go in there.


### Media References[¶](#media-references "Permalink to this heading")

Clip media (if known) should be linked like this:

```
clip.media_reference = otio.schema.ExternalReference(
    target_url="file://example/movie.mov"
)

```

Some formats don’t support direct links to media, but focus on metadata instead.
It is fine to leave the media\_reference empty (‘None’) if your adapter doesn’t
know a real file path or URL for the media.


### Source Range vs Available Range[¶](#source-range-vs-available-range "Permalink to this heading")

To specify the range of media used in the Clip, you must set the Clip’s
source\_range like this:

```
clip.source_range = otio.opentime.TimeRange(
    start_time=otio.opentime.RationalTime(150, 24), # frame 150 @ 24fps

    duration=otio.opentime.RationalTime(200, 24) # 200 frames @ 24fps

)

```

Note that the source\_range of the clip is not necessarily the same as the
available\_range of the media reference. You may have a clip that uses only a
portion of a longer piece of media, or you might have some media that is too
short for the desired clip length. Both of these are fine in OTIO. Also, clips
can be relinked to different media, in which case the source\_range of the clip
stays the same, but the media\_reference (and its available\_range) will change
after the relink. For example, you might relink from an old render to a newer
render which has been extended to cover the source\_range references by the
clip.

If you know the range of media available at that Media Reference’s URL, then you
can specify it like this:

```
clip.media_reference = otio.schema.ExternalReference(
  target_url="file://example/movie.mov",
  available_range=otio.opentime.TimeRange(
      start_time=otio.opentime.RationalTime(100, 24), # frame 100 @ 24fps

      duration=otio.opentime.RationalTime(500, 24) # 500 frames @ 24fps

  )
)

```

It is fine to leave the Media Reference’s available\_range empty if you don’t
know it, but you should always specify a Clip’s source\_range.


## Traversing a Timeline[¶](#traversing-a-timeline "Permalink to this heading")

When exporting a Timeline in the `write_to_string` or `write_to_file` functions,
you will need to traverse the Timeline data structure. Some formats only support
a single track, so a simple adapter might work like this:

```
def write_to_string(input_otio):
    """Turn a single track timeline into a very simple CSV."""
    result = "Clip,Start,Duration\n"
    if len(input_otio.tracks) != 1:
        raise Exception("This adapter does not support multiple tracks.")
    for item in input_otio.each_clip():
        start = otio.opentime.to_seconds(item.source_range.start_time)
        duration = otio.opentime.to_seconds(item.source_range.duration)
        result += ",".join([item.name, start, duration]) + "\n"
    return result

```

More complex timelines will contain multiple tracks and nested stacks. OTIO
supports nesting via the abstract Composition class, with two concrete
subclasses, Track and Stack. In general a Composition has children, each of
which is an Item. Since Composition is also a subclass of Item, they can be
nested arbitrarily.

In typical usage, you are likely to find that a Timeline has a Stack (the
property called ‘tracks’), and each item within that Stack is a Track. Each item
within a Track will usually be a Clip, Transition or Gap. If you don’t support
Transitions, you can just skip them and the overall timing of the Track should
still work.

If the format your adapter supports allows arbitrary nesting, then you should
traverse the composition in a general way, like this:

```
def export_otio_item(item):
    result = MyThing(item)
    if isinstance(item, otio.core.Composition):
        result.children = map(export_otio_item, item.children)
    return result

```

If the format your adapter supports has strict expectations about the structure,
then you should validate that the input has the expected structure and then
traverse it based on those expectations, like this:

```
def export_timeline(timeline):
    result = MyTimeline(timeline.name)
    for track in timeline.tracks:
        if not isinstance(track, otio.schema.Track):
            raise Exception("This adapter requires each top-level item to be a track, not a "+typeof(track))
      t = result.AddTrack(track.name)
      for clip in track.each_clip():
          c = result.AddClip(clip.name)
    return result

```


## Examples[¶](#examples "Permalink to this heading")

OTIO includes a number of “core” (supported by the core team) adapters in
`opentimelineio/adapters` as well as a number of community supported adapters in
`opentimelineio_contrib/adapters`.

---



## Page 43: Write A Hookscript.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/write-a-hookscript.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/write-a-hookscript.html)

* Writing a Hook Script
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/write-a-hookscript.md)


# Writing a Hook Script[¶](#writing-a-hook-script "Permalink to this heading")

OpenTimelineIO Hook Scripts are plugins that run at predefined points during the
execution of various OTIO functions, for example after an adapter has read a
file into memory but before the media linker has run.

To write a new hook script, you create a python source file that defines a
function named `hook_function` with signature: `hook_function ::
otio.schema.Timeline, Dict => otio.schema.Timeline`

The first argument is the timeline to process, and the second one is a
dictionary of arguments that can be passed to it by the adapter or media linker.
Only one hook function can be defined per python file.

For example:

```
def hook_function(tl, argument_map=None):
    for cl in tl.each_clip():
        cl.metadata['example_hook_function_was_here'] = True
    return tl

```

This will insert some extra metadata into each clip.

This plugin can then be registered with the system by configuring a plugin
manifest.


## Registering Your Hook Script[¶](#registering-your-hook-script "Permalink to this heading")

To create a new OTIO hook script, you need to create a file myhooks.py. Then add
a manifest that points at that python file:

```
{
    "OTIO_SCHEMA" : "PluginManifest.1",
    "hook_scripts" : [
        {
            "OTIO_SCHEMA" : "HookScript.1",
            "name" : "example hook",
            "filepath" : "myhooks.py"
        }
    ],
    "hooks" : {
        "pre_adapter_write" : ["example hook"],
        "post_adapter_read" : [],
        "post_adapter_write" : [],
        "post_media_linker" : []
    }
}

```

The `hook_scripts` section will register the plugin with the system, and the
`hooks` section will attach the scripts to hooks.

Then you need to add this manifest to your
[OTIO\_PLUGIN\_MANIFEST\_PATH](otio-env-variables.html#term-OTIO_PLUGIN_MANIFEST_PATH)

environment variable. You may also define media linkers and adapters via the
same manifest.


## Running a Hook Script[¶](#running-a-hook-script "Permalink to this heading")

If you would like to call a hook script from a plugin, the hooks need not be one
of the ones that OTIO pre-defines. You can have a plugin adapter or media
linker, for example, that defines its own hooks and calls your own custom studio
specific hook scripts. To run a hook script from your custom code, you can call:

```
otio.hooks.run("some_hook", some_timeline, optional_argument_dict)

```

This will call the `some_hook` hook script and pass in `some_timeline` and
`optional_argument_dict`.


## Order of Hook Scripts[¶](#order-of-hook-scripts "Permalink to this heading")

To query which hook scripts are attached to a given hook, you can call:

```
import opentimelineio as otio
hook_list = otio.hooks.scripts_attached_to("some_hook")

```

Note that `hook_list` will be in order of execution. You can rearrange this
list, or edit it to change which scripts will run (or not run) and in which
order.

To Edit the order, change the order in the list:

```
hook_list[0], hook_list[2] = hook_list[2], hook_list[0]
print hook_list # ['c','b','a']

```

Now c will run, then b, then a.

To delete a function in the list:

```
del hook_list[1]

```


## Example Hooks[¶](#example-hooks "Permalink to this heading")


### Replacing part of a path for drive mapping[¶](#replacing-part-of-a-path-for-drive-mapping "Permalink to this heading")

An example use-case would be to create a pre-write adapter hook that checks the
argument map for a style being identified as nucoda and then preforms a path
replacement on the reference url:

```
def hook_function(in_timeline,argument_map=None):
    adapter_args = argument_map.get('adapter_arguments')
    if adapter_args and adapter_args.get('style') == 'nucoda':
        for in_clip in in_timeline.each_clip():
            ''' Change the Path to use windows drive letters ( Nucoda is not otherwise forward slash sensative ) '''
            if in_clip.media_reference:
                in_clip.media_reference.target_url = in_clip.media_reference.target_url.replace(r'/linux/media/path','S:')

```


### Add an incremental copy of otio file to backup folder[¶](#add-an-incremental-copy-of-otio-file-to-backup-folder "Permalink to this heading")

Example of a post adapter write hook that creates a timestamped copy of newly
written file in a hidden “incremental” folder:

```
import os
import time
import shutil

def hook_function(in_timeline, argument_map=None):
    # Adapter will add "_filepath" to argument_map

    filepath = argument_map.get('_filepath')

    backup_name = "{filename}.{time}".format(
        filename=os.path.basename(filepath),
        time=time.time()
    )
    incrpath = os.path.join(
        os.path.dirname(filepath),
        '.incremental',
        backup_name
    )
    shutil.copyfile(filepath, incrpath)

    return in_timeline

```

Please note that if a “post adapter write hook” changes `in_timeline` in any
way, the api will not automatically update the already serialized file. The
changes will only exist in the in-memory object, because the hook runs *after*
the file is serialized to disk.

---



## Page 44: Spatial Coordinates.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/tutorials/spatial-coordinates.html](https://opentimelineio.readthedocs.io/en/stable/tutorials/spatial-coordinates.html)

* OTIO Spatial Coordinate System
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/tutorials/spatial-coordinates.md)


# OTIO Spatial Coordinate System[¶](#otio-spatial-coordinate-system "Permalink to this heading")

This document describes a proposed coordinate system for OpenTimelineIO. It
focuses mainly on the Bounds object, which is a rectangular area represented
through a 2D box within that coordinate system.


## Coordinate System[¶](#coordinate-system "Permalink to this heading")

The proposed spatial coordinate system is unit-less. It allows decoupling clip
layouts from pixel density. It has a single origin (X=0.0, Y=0.0) and is used as
a unique canvas across the whole Timeline. Y-Axis-Up convention is used.

We propose in the OTIO spatial coordinate system that we use planes that are
unique in the continuous domain in order to make it analogous to the existing
temporal implementation. Currently in a Composition of Items a RationalTime’s
value (usually a frame) index is seen as belonging to the Item that appears
later in time. For example, if we have two Items ranging from value 1 to value 2
and from value 2 to value 3, value 2 will belong to the second Item. Or in other
words, we are using exclusive temporal bounds such that the temporal spans are
[1,2) and [2,3).

In order to preserve the same logic in the spatial domain we require a plane
that is unique in the continuous domain. To use a similar example given a 2
dimensional bound from (0, 1), and another from (1, 2), we require that a sample
at the value 1 falls strictly into one bound or the other, in particular, it
should fall into the higher value bound (1,2) and not into (0, 1).


## Bounds[¶](#bounds "Permalink to this heading")

A Bounds object is a 2D box that defines a spatial area in the unit-less
coordinate system. Here is an example of Bounds defining a
first-quadrant-snapped rectangle with a width of 16 and a height of 9. Note
that, since Bounds are serializable object, they have a metadata member.

```
"available_image_bounds": {
  "OTIO_SCHEMA": "Box2d.1",
  "min": {
    "OTIO_SCHEMA":"V2d.1",
    "x": 0.0,
    "y": 0.0
  },
  "max": {
    "OTIO_SCHEMA":"V2d.1",
    "x": 16.0,
    "y": 9.0
  }
}

```

Here is another example of Bounds defining an origin-centered rectangle with a
width of 16 and a height of 9.

```
"available_image_bounds": {
  "OTIO_SCHEMA": "Box2d.1",
  "min": {
    "OTIO_SCHEMA":"V2d.1",
    "x": -8.0,
    "y": -4.5
  },
  "max": {
    "OTIO_SCHEMA":"V2d.1",
    "x": 8.0,
    "y": 4.5
  }
}

```

When multiple clips are being rendered, either through a transition or through
the presence of a multi-tracks timeline, all clips share the same coordinate
system.

For instance, if we add an origin-centered square clip on top of the previous
one, here is what we get.

Since each clip has its own bounds properties, clips can be arranged into
complex layouts.

This can be used in several contexts, for instance:

* Side-by-side comparison
* Picture-In-Picture
* Complex spatial layouts for notes (collage)

Example of a Picture-In-Picture layout added on top of the previous 2-clips
layout:


## Bounds and Clips[¶](#bounds-and-clips "Permalink to this heading")

Currently, we use the Bounds object at the ***Clip.media\_reference.bounds***
level. This allows support for different bounds when changing the
media-representation of a given Clip. For instance, a Clip could have 2
media-representations (a set of High-Res 16:9 OpenEXR files and a Low-Res 4:3
MP4 file). Those 2 media-representations might not cover the same spatial area,
therefore it makes sense for them to have their individual Bounds region.


## Non-Bounds representations[¶](#non-bounds-representations "Permalink to this heading")

The coordinate system can also be used to describe non-rectangular coordinates.
For instance, effects that have spatial-based parameters that need to be
expressed in a resolution-independent way could use the same system.

Examples of potential usage for this coordinate system:

* Blur amount
* Annotation position
* Wipe bar position (angular mask)

---



## Page 45: Index.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/index.html](https://opentimelineio.readthedocs.io/en/stable/index.html)

* Welcome to OpenTimelineIO’s documentation!
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/index.rst)


# Welcome to OpenTimelineIO’s documentation![¶](#welcome-to-opentimelineio-s-documentation "Permalink to this heading")


## Overview[¶](#overview "Permalink to this heading")

OpenTimelineIO (OTIO) is an API and interchange format for editorial cut
information. You can think of it as a modern Edit Decision List (EDL) that also
includes an API for reading, writing, and manipulating editorial data. It also
includes a plugin system for translating to/from existing editorial formats as
well as a plugin system for linking to proprietary media storage schemas.

OTIO supports clips, timing, tracks, transitions, markers, metadata, etc. but
not embedded video or audio. Video and audio media are referenced externally. We
encourage 3rd party vendors, animation studios and visual effects studios to
work together as a community to provide adaptors for each video editing tool and
pipeline.


## Links[¶](#links "Permalink to this heading")

[OpenTimelineIO Home Page](http://opentimeline.io/)

[OpenTimelineIO Discussion Group](https://lists.aswf.io/g/otio-discussion)


## Quick Start[¶](#quick-start "Permalink to this heading")

Quick Start

* [Quickstart](tutorials/quickstart.html)
  + [Install Prerequisites](tutorials/quickstart.html#install-prerequisites)

  + [Install OTIO](tutorials/quickstart.html#install-otio)

  + [Setup Any Additional Adapters You May Want](tutorials/quickstart.html#setup-any-additional-adapters-you-may-want)

  + [Run OTIOView](tutorials/quickstart.html#run-otioview)

* [Developer Quickstart](tutorials/quickstart.html#developer-quickstart)

  + [To build OTIO for C++ development:](tutorials/quickstart.html#to-build-otio-for-c-development)

  + [To build OTIO for Python development:](tutorials/quickstart.html#to-build-otio-for-python-development)

  + [To build OTIO for both C++ and Python development:](tutorials/quickstart.html#to-build-otio-for-both-c-and-python-development)

* [Debugging Quickstart](tutorials/quickstart.html#debugging-quickstart)

  + [Linux / GDB / LLDB](tutorials/quickstart.html#linux-gdb-lldb)

* [How to Generate the C++ Documentation:](tutorials/quickstart.html#how-to-generate-the-c-documentation)

  + [Mac / Linux](tutorials/quickstart.html#mac-linux)

* [Environment Variables](tutorials/otio-env-variables.html)
  + [Plugin Configuration](tutorials/otio-env-variables.html#plugin-configuration)

  + [Unit tests](tutorials/otio-env-variables.html#unit-tests)


## Tutorials[¶](#tutorials "Permalink to this heading")

Tutorials

* [Adapters](tutorials/adapters.html)
  + [Built-In Adapters](tutorials/adapters.html#built-in-adapters)

  + [Batteries-Included Adapters](tutorials/adapters.html#batteries-included-adapters)

  + [Additional Adapters](tutorials/adapters.html#additional-adapters)

  + [Custom Adapters](tutorials/adapters.html#custom-adapters)

* [Architecture](tutorials/architecture.html)
  + [Overview](tutorials/architecture.html#overview)

  + [Canonical Structure](tutorials/architecture.html#canonical-structure)

  + [Modules](tutorials/architecture.html#modules)

  + [Time on otio.schema.Clip](tutorials/architecture.html#time-on-otio-schema-clip)

  + [Time On Clips in Containers](tutorials/architecture.html#time-on-clips-in-containers)

  + [otio.opentime](tutorials/architecture.html#otio-opentime)

  + [otio.adapters](tutorials/architecture.html#otio-adapters)

  + [otio.media\_linkers](tutorials/architecture.html#otio-media-linkers)

  + [Example Scripts](tutorials/architecture.html#example-scripts)

* [Contributing](tutorials/contributing.html)
  + [Contributor License Agreement](tutorials/contributing.html#contributor-license-agreement)

  + [Coding Conventions](tutorials/contributing.html#coding-conventions)

  + [Platform Support Policy](tutorials/contributing.html#platform-support-policy)

  + [Git Workflow](tutorials/contributing.html#git-workflow)

* [Feature Matrix](tutorials/feature-matrix.html)
* [Timeline Structure](tutorials/otio-timeline-structure.html)
  + [Rendering](tutorials/otio-timeline-structure.html#rendering)

  + [Simple Cut List](tutorials/otio-timeline-structure.html#simple-cut-list)

  + [Transitions](tutorials/otio-timeline-structure.html#transitions)

  + [Multiple Tracks](tutorials/otio-timeline-structure.html#multiple-tracks)

  + [Nested Compositions](tutorials/otio-timeline-structure.html#nested-compositions)

* [Time Ranges](tutorials/time-ranges.html)
  + [Overview](tutorials/time-ranges.html#overview)

  + [Clips](tutorials/time-ranges.html#clips)

  + [Tracks](tutorials/time-ranges.html#tracks)

  + [Markers](tutorials/time-ranges.html#markers)

  + [Transitions](tutorials/time-ranges.html#transitions)

  + [Gaps](tutorials/time-ranges.html#gaps)

  + [Stacks](tutorials/time-ranges.html#stacks)

  + [Timelines](tutorials/time-ranges.html#timelines)

* [File Bundles](tutorials/otio-filebundles.html)
  + [Overview](tutorials/otio-filebundles.html#overview)

  + [Source Timeline](tutorials/otio-filebundles.html#source-timeline)

  + [Structure](tutorials/otio-filebundles.html#structure)

  + [Read Behavior](tutorials/otio-filebundles.html#read-behavior)

  + [MediaReferencePolicy](tutorials/otio-filebundles.html#mediareferencepolicy)

  + [OTIOD](tutorials/otio-filebundles.html#otiod)

  + [OTIOZ](tutorials/otio-filebundles.html#otioz)

  + [Example usage in otioconvert](tutorials/otio-filebundles.html#example-usage-in-otioconvert)

* [Writing an OTIO Adapter](tutorials/write-an-adapter.html)
  + [Sharing an Adapter You’ve Written With the Community](tutorials/write-an-adapter.html#sharing-an-adapter-youve-written-with-the-community)

  + [Required Functions](tutorials/write-an-adapter.html#required-functions)

  + [Constructing a Timeline](tutorials/write-an-adapter.html#constructing-a-timeline)

  + [Traversing a Timeline](tutorials/write-an-adapter.html#traversing-a-timeline)

  + [Examples](tutorials/write-an-adapter.html#examples)

* [Writing an OTIO Media Linker](tutorials/write-a-media-linker.html)
  + [Registering Your Media Linker](tutorials/write-a-media-linker.html#registering-your-media-linker)

  + [Writing a Media Linker](tutorials/write-a-media-linker.html#writing-a-media-linker)

  + [For Testing](tutorials/write-a-media-linker.html#for-testing)

* [Writing a Hook Script](tutorials/write-a-hookscript.html)
  + [Registering Your Hook Script](tutorials/write-a-hookscript.html#registering-your-hook-script)

  + [Running a Hook Script](tutorials/write-a-hookscript.html#running-a-hook-script)

  + [Order of Hook Scripts](tutorials/write-a-hookscript.html#order-of-hook-scripts)

  + [Example Hooks](tutorials/write-a-hookscript.html#example-hooks)

* [Writing an OTIO SchemaDef Plugin](tutorials/write-a-schemadef.html)
  + [Registering Your SchemaDef Plugin](tutorials/write-a-schemadef.html#registering-your-schemadef-plugin)

  + [Using the New Schema in Your Code](tutorials/write-a-schemadef.html#using-the-new-schema-in-your-code)

* [OTIO Spatial Coordinate System](tutorials/spatial-coordinates.html)
  + [Coordinate System](tutorials/spatial-coordinates.html#coordinate-system)

  + [Bounds](tutorials/spatial-coordinates.html#bounds)

  + [Bounds and Clips](tutorials/spatial-coordinates.html#bounds-and-clips)

  + [Non-Bounds representations](tutorials/spatial-coordinates.html#non-bounds-representations)

* [Schema Proposal and Development Workflow](tutorials/developing-a-new-schema.html)
  + [Introduction](tutorials/developing-a-new-schema.html#introduction)

  + [Examples](tutorials/developing-a-new-schema.html#examples)

  + [Core schema or Plugin?](tutorials/developing-a-new-schema.html#core-schema-or-plugin)

  + [Proposal](tutorials/developing-a-new-schema.html#proposal)

  + [Implementing and Iterating on a branch](tutorials/developing-a-new-schema.html#implementing-and-iterating-on-a-branch)

  + [Demo Adapter](tutorials/developing-a-new-schema.html#demo-adapter)

  + [Incrementing Other Schemas](tutorials/developing-a-new-schema.html#incrementing-other-schemas)

  + [Conclusion](tutorials/developing-a-new-schema.html#conclusion)

* [Versioning Schemas](tutorials/versioning-schemas.html)
  + [Overview](tutorials/versioning-schemas.html#overview)

  + [Schema/Version Introduction](tutorials/versioning-schemas.html#schema-version-introduction)

  + [Schema Upgrading](tutorials/versioning-schemas.html#schema-upgrading)

  + [Schema Downgrading](tutorials/versioning-schemas.html#schema-downgrading)

  + [Downgrading at Runtime](tutorials/versioning-schemas.html#downgrading-at-runtime)

  + [For Developers](tutorials/versioning-schemas.html#for-developers)


## Use Cases[¶](#use-cases "Permalink to this heading")

Use Cases

* [Animation Shot Frame Ranges Changed](use-cases/animation-shot-frame-ranges.html)
  + [Summary](use-cases/animation-shot-frame-ranges.html#summary)

  + [Example](use-cases/animation-shot-frame-ranges.html#example)

  + [Features Needed in OTIO](use-cases/animation-shot-frame-ranges.html#features-needed-in-otio)

  + [Features of Python Script](use-cases/animation-shot-frame-ranges.html#features-of-python-script)

* [Conform New Renders Into The Cut](use-cases/conform-new-renders-into-cut.html)
  + [Summary](use-cases/conform-new-renders-into-cut.html#summary)

  + [Workflow](use-cases/conform-new-renders-into-cut.html#workflow)

* [Shots Added or Removed From The Cut](use-cases/shots-added-removed-from-cut.html)
  + [Summary](use-cases/shots-added-removed-from-cut.html#summary)

  + [Example](use-cases/shots-added-removed-from-cut.html#example)

  + [Features Needed in OTIO](use-cases/shots-added-removed-from-cut.html#features-needed-in-otio)

  + [Features of Python Script](use-cases/shots-added-removed-from-cut.html#features-of-python-script)


## API References[¶](#api-references "Permalink to this heading")

API References

* [Python](python_reference.html)
  + [opentimelineio](api/python/opentimelineio.html)
    - [opentimelineio.adapters](api/python/opentimelineio.adapters.html)
    - [opentimelineio.algorithms](api/python/opentimelineio.algorithms.html)
    - [opentimelineio.console](api/python/opentimelineio.console.html)
    - [opentimelineio.core](api/python/opentimelineio.core.html)
    - [opentimelineio.exceptions](api/python/opentimelineio.exceptions.html)
    - [opentimelineio.hooks](api/python/opentimelineio.hooks.html)
    - [opentimelineio.media\_linker](api/python/opentimelineio.media_linker.html)
    - [opentimelineio.opentime](api/python/opentimelineio.opentime.html)
    - [opentimelineio.plugins](api/python/opentimelineio.plugins.html)
    - [opentimelineio.schema](api/python/opentimelineio.schema.html)
    - [opentimelineio.schemadef](api/python/opentimelineio.schemadef.html)
    - [opentimelineio.test\_utils](api/python/opentimelineio.test_utils.html)
    - [opentimelineio.url\_utils](api/python/opentimelineio.url_utils.html)
    - [opentimelineio.versioning](api/python/opentimelineio.versioning.html)
* [Language Bridges](cxx/bridges.html)
  + [Python](cxx/bridges.html#python)

  + [Swift](cxx/bridges.html#swift)

  + [Bridging to C (and other languages)](cxx/bridges.html#bridging-to-c-and-other-languages)

* [C++ Implementation Details](cxx/cxx.html)
  + [Dependencies](cxx/cxx.html#dependencies)

  + [Starting Examples](cxx/cxx.html#starting-examples)

    - [Defining a Schema](cxx/cxx.html#defining-a-schema)

    - [Reading/Writing Properties](cxx/cxx.html#reading-writing-properties)

  + [Using Schemas](cxx/cxx.html#using-schemas)

  + [Serializable Data](cxx/cxx.html#serializable-data)

  + [C++ Properties](cxx/cxx.html#c-properties)

  + [Object Graphs and Serialization](cxx/cxx.html#object-graphs-and-serialization)

  + [Memory Management](cxx/cxx.html#memory-management)

    - [Examples](cxx/cxx.html#examples)

  + [Error Handling](cxx/cxx.html#error-handling)

  + [Thread Safety](cxx/cxx.html#thread-safety)

  + [Proposed OTIO C++ Header Files](cxx/cxx.html#proposed-otio-c-header-files)

  + [Extended Memory Management Discussion](cxx/cxx.html#extended-memory-management-discussion)

* [Writing OTIO in C, C++ or Python (June 2018)](cxx/older.html)
  + [Python C-API](cxx/older.html#python-c-api)

  + [Boost-Python](cxx/older.html#boost-python)

  + [PyBind11](cxx/older.html#pybind11)

  + [Conclusion](cxx/older.html#conclusion)


## Schema Reference[¶](#schema-reference "Permalink to this heading")

Schema Reference

* [File Format Specification](tutorials/otio-file-format-specification.html)
  + [Version](tutorials/otio-file-format-specification.html#version)

  + [Note](tutorials/otio-file-format-specification.html#note)

  + [Naming](tutorials/otio-file-format-specification.html#naming)

  + [Contents](tutorials/otio-file-format-specification.html#contents)

  + [Structure](tutorials/otio-file-format-specification.html#structure)

  + [Nesting](tutorials/otio-file-format-specification.html#nesting)

  + [Metadata](tutorials/otio-file-format-specification.html#metadata)

  + [Example:](tutorials/otio-file-format-specification.html#example)

  + [Schema Specification](tutorials/otio-file-format-specification.html#schema-specification)

* [Serialized Data Documentation](tutorials/otio-serialized-schema.html)
* [Class Documentation](tutorials/otio-serialized-schema.html#class-documentation)

  + [Module: opentimelineio.adapters](tutorials/otio-serialized-schema.html#module-opentimelineio-adapters)

  + [Module: opentimelineio.core](tutorials/otio-serialized-schema.html#module-opentimelineio-core)

  + [Module: opentimelineio.hooks](tutorials/otio-serialized-schema.html#module-opentimelineio-hooks)

  + [Module: opentimelineio.media\_linker](tutorials/otio-serialized-schema.html#module-opentimelineio-media-linker)

  + [Module: opentimelineio.opentime](tutorials/otio-serialized-schema.html#module-opentimelineio-opentime)

  + [Module: opentimelineio.plugins](tutorials/otio-serialized-schema.html#module-opentimelineio-plugins)

  + [Module: opentimelineio.schema](tutorials/otio-serialized-schema.html#module-opentimelineio-schema)

* [Serialized Data (Fields Only)](tutorials/otio-serialized-schema-only-fields.html)
* [Classes](tutorials/otio-serialized-schema-only-fields.html#classes)

  + [Module: opentimelineio.adapters](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-adapters)

  + [Module: opentimelineio.core](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-core)

  + [Module: opentimelineio.hooks](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-hooks)

  + [Module: opentimelineio.media\_linker](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-media-linker)

  + [Module: opentimelineio.opentime](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-opentime)

  + [Module: opentimelineio.plugins](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-plugins)

  + [Module: opentimelineio.schema](tutorials/otio-serialized-schema-only-fields.html#module-opentimelineio-schema)


## Autogenerated Plugin Reference[¶](#autogenerated-plugin-reference "Permalink to this heading")

Plugins Reference

* [Plugin Documentation](tutorials/otio-plugins.html)
* [Manifests](tutorials/otio-plugins.html#manifests)

* [Core Plugins](tutorials/otio-plugins.html#core-plugins)

  + [Adapter Plugins](tutorials/otio-plugins.html#adapter-plugins)

  + [Media Linkers](tutorials/otio-plugins.html#media-linkers)

  + [SchemaDefs](tutorials/otio-plugins.html#schemadefs)

  + [HookScripts](tutorials/otio-plugins.html#hookscripts)

  + [Hooks](tutorials/otio-plugins.html#hooks)


## Indices and tables[¶](#indices-and-tables "Permalink to this heading")

* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)

---



## Page 46: Opentimelineio.Console.Otioconvert.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otioconvert.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otioconvert.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.otioconvert
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.otioconvert.rst)


# opentimelineio.console.otioconvert[¶](#module-opentimelineio.console.otioconvert "Permalink to this heading")

Python wrapper around OTIO to convert timeline files between formats.

Available adapters: [‘otio\_json’, ‘otioz’, ‘otiod’]

opentimelineio.console.otioconvert.main()[¶](#opentimelineio.console.otioconvert.main "Permalink to this definition")

Parse arguments and convert the files.

---



## Page 47: Opentimelineio.Console.Otiopluginfo.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiopluginfo.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiopluginfo.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.otiopluginfo
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.otiopluginfo.rst)


# opentimelineio.console.otiopluginfo[¶](#module-opentimelineio.console.otiopluginfo "Permalink to this heading")

Print information about the OTIO plugin ecosystem.

opentimelineio.console.otiopluginfo.main()[¶](#opentimelineio.console.otiopluginfo.main "Permalink to this definition")

main entry point

---



## Page 48: Opentimelineio.Console.Autogen Version Map.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.autogen_version_map.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.autogen_version_map.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.autogen\_version\_map
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.autogen_version_map.rst)


# opentimelineio.console.autogen\_version\_map[¶](#module-opentimelineio.console.autogen_version_map "Permalink to this heading")

Generate the CORE\_VERSION\_MAP for this version of OTIO

opentimelineio.console.autogen\_version\_map.generate\_core\_version\_map(*src\_text*, *label*, *version\_map*)[¶](#opentimelineio.console.autogen_version_map.generate_core_version_map "Permalink to this definition")opentimelineio.console.autogen\_version\_map.main()[¶](#opentimelineio.console.autogen_version_map.main "Permalink to this definition")

---



## Page 49: Opentimelineio.Console.Autogen Plugin Documentation.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.autogen_plugin_documentation.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.autogen_plugin_documentation.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.autogen\_plugin\_documentation
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.autogen_plugin_documentation.rst)


# opentimelineio.console.autogen\_plugin\_documentation[¶](#module-opentimelineio.console.autogen_plugin_documentation "Permalink to this heading")

Generates documentation of all the built in plugins for OpenTimelineIO

opentimelineio.console.autogen\_plugin\_documentation.generate\_and\_write\_documentation\_plugins(*public\_only=False*, *sanitized\_paths=False*)[¶](#opentimelineio.console.autogen_plugin_documentation.generate_and_write_documentation_plugins "Permalink to this definition")opentimelineio.console.autogen\_plugin\_documentation.main()[¶](#opentimelineio.console.autogen_plugin_documentation.main "Permalink to this definition")

main entry point

---



## Page 50: Opentimelineio.Console.Otiocat.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiocat.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiocat.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.otiocat
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.otiocat.rst)


# opentimelineio.console.otiocat[¶](#module-opentimelineio.console.otiocat "Permalink to this heading")

Print the contents of an OTIO file to stdout.

opentimelineio.console.otiocat.main()[¶](#opentimelineio.console.otiocat.main "Permalink to this definition")

Parse arguments and call \_otio\_compatible\_file\_to\_json\_string.

---



## Page 51: Opentimelineio.Console.Otiotool.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiotool.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiotool.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.otiotool
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.otiotool.rst)


# opentimelineio.console.otiotool[¶](#module-opentimelineio.console.otiotool "Permalink to this heading")

otiotool is a multipurpose command line tool for inspecting, modifying,
combining, and splitting OTIO files.

Each of the many operations it can perform is provided by a small, simple
utility function. These functions also serve as concise examples of how OTIO can
be used to perform common workflow tasks.

opentimelineio.console.otiotool.concatenate\_timelines(*timelines*)[¶](#opentimelineio.console.otiotool.concatenate_timelines "Permalink to this definition")

Return a single timeline with all of the input timelines concatenated
end-to-end. The resulting timeline should be as long as the sum of the durations
of the input timelines.

opentimelineio.console.otiotool.copy\_media(*url*, *destination\_path*)[¶](#opentimelineio.console.otiotool.copy_media "Permalink to this definition")opentimelineio.console.otiotool.copy\_media\_to\_folder(*timeline*, *folder*)[¶](#opentimelineio.console.otiotool.copy_media_to_folder "Permalink to this definition")

Copy or download all referenced media to this folder, and relink media
references to the copies.

opentimelineio.console.otiotool.filter\_clips(*only\_clips\_with\_name*, *only\_clips\_with\_name\_regex*, *timelines*)[¶](#opentimelineio.console.otiotool.filter_clips "Permalink to this definition")

Return a copy of the input timelines with only clips with names that match
either the given list of names, or regular expression patterns.

opentimelineio.console.otiotool.filter\_tracks(*only\_tracks\_with\_name*, *only\_tracks\_with\_index*, *timelines*)[¶](#opentimelineio.console.otiotool.filter_tracks "Permalink to this definition")

Return a copy of the input timelines with only tracks that match either the list
of names given, or the list of track indexes given.

opentimelineio.console.otiotool.filter\_transitions(*timelines*)[¶](#opentimelineio.console.otiotool.filter_transitions "Permalink to this definition")

Return a copy of the input timelines with all transitions removed. The overall
duration of the timelines should not be affected.

opentimelineio.console.otiotool.flatten\_timeline(*timeline*, *which\_tracks='video'*, *keep=False*)[¶](#opentimelineio.console.otiotool.flatten_timeline "Permalink to this definition")

Replace the tracks of this timeline with a single track by flattening. If
which\_tracks is specified, you may choose ‘video’, ‘audio’, or ‘all’. If keep
is True, then the old tracks are retained and the new one is added above them
instead of replacing them. This can be useful to see and understand how
flattening works.

opentimelineio.console.otiotool.inspect\_timelines(*name\_regex*, *timeline*)[¶](#opentimelineio.console.otiotool.inspect_timelines "Permalink to this definition")

Print some detailed information about the item(s) in the timeline with names
that match the given regular expression.

opentimelineio.console.otiotool.keep\_only\_audio\_tracks(*timeline*)[¶](#opentimelineio.console.otiotool.keep_only_audio_tracks "Permalink to this definition")

Remove all tracks except for audio tracks from a timeline.

opentimelineio.console.otiotool.keep\_only\_video\_tracks(*timeline*)[¶](#opentimelineio.console.otiotool.keep_only_video_tracks "Permalink to this definition")

Remove all tracks except for video tracks from a timeline.

opentimelineio.console.otiotool.main()[¶](#opentimelineio.console.otiotool.main "Permalink to this definition")

otiotool main program. This function is resposible for executing the steps
specified by all of the command line arguments in the right order.

opentimelineio.console.otiotool.parse\_arguments()[¶](#opentimelineio.console.otiotool.parse_arguments "Permalink to this definition")opentimelineio.console.otiotool.print\_timeline\_stats(*timeline*)[¶](#opentimelineio.console.otiotool.print_timeline_stats "Permalink to this definition")

Print some statistics about the given timeline.

opentimelineio.console.otiotool.read\_inputs(*input\_paths*)[¶](#opentimelineio.console.otiotool.read_inputs "Permalink to this definition")

Read one or more timlines from the list of file paths given. If a file path is
‘-’ then a timeline is read from stdin.

opentimelineio.console.otiotool.redact\_timeline(*timeline*)[¶](#opentimelineio.console.otiotool.redact_timeline "Permalink to this definition")

Remove all metadata, names, or other identifying information from this timeline.
Only the structure, schema and timing will remain.

opentimelineio.console.otiotool.relink\_by\_name(*timeline*, *path*)[¶](#opentimelineio.console.otiotool.relink_by_name "Permalink to this definition")

Relink clips in the timeline to media files discovered at the given folder path.

opentimelineio.console.otiotool.remove\_metadata\_key(*timeline*, *key*)[¶](#opentimelineio.console.otiotool.remove_metadata_key "Permalink to this definition")opentimelineio.console.otiotool.stack\_timelines(*timelines*)[¶](#opentimelineio.console.otiotool.stack_timelines "Permalink to this definition")

Return a single timeline with all of the tracks from all of the input timelines
stacked on top of each other. The resulting timeline should be as long as the
longest input timeline.

opentimelineio.console.otiotool.summarize\_timeline(*list\_tracks*, *list\_clips*, *list\_media*, *verify\_media*, *list\_markers*, *timeline*)[¶](#opentimelineio.console.otiotool.summarize_timeline "Permalink to this definition")

Print a summary of a timeline, optionally listing the tracks, clips, media,
and/or markers inside it.

opentimelineio.console.otiotool.time\_from\_string(*text*, *rate*)[¶](#opentimelineio.console.otiotool.time_from_string "Permalink to this definition")

This helper function turns a string into a RationalTime. It accepts either a
timecode string (e.g. “HH:MM:SS:FF”) or a string with a floating point value
measured in seconds. The second argument to this function specifies the rate for
the returned RationalTime.

opentimelineio.console.otiotool.trim\_timeline(*start*, *end*, *timeline*)[¶](#opentimelineio.console.otiotool.trim_timeline "Permalink to this definition")

Return a copy of the input timeline trimmed to the start and end times given.
Each of the start and end times can be specified as either a timecode string
(e.g. “HH:MM:SS:FF”) or a string with a floating point value measured in
seconds.

opentimelineio.console.otiotool.write\_output(*output\_path*, *output*)[¶](#opentimelineio.console.otiotool.write_output "Permalink to this definition")

Write the given OTIO object to a file path. If the file path given is the string
‘-’ then the output is written to stdout instead.

---



## Page 52: Opentimelineio.Console.Autogen Serialized Datamodel.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.autogen_serialized_datamodel.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.autogen_serialized_datamodel.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.autogen\_serialized\_datamodel
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.autogen_serialized_datamodel.rst)


# opentimelineio.console.autogen\_serialized\_datamodel[¶](#module-opentimelineio.console.autogen_serialized_datamodel "Permalink to this heading")

Generates documentation of the serialized data model for OpenTimelineIO.

opentimelineio.console.autogen\_serialized\_datamodel.generate\_and\_write\_documentation()[¶](#opentimelineio.console.autogen_serialized_datamodel.generate_and_write_documentation "Permalink to this definition")opentimelineio.console.autogen\_serialized\_datamodel.main()[¶](#opentimelineio.console.autogen_serialized_datamodel.main "Permalink to this definition")

main entry point

---



## Page 53: Opentimelineio.Console.Console Utils.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.console_utils.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.console_utils.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.console\_utils
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.console_utils.rst)


# opentimelineio.console.console\_utils[¶](#module-opentimelineio.console.console_utils "Permalink to this heading")

opentimelineio.console.console\_utils.arg\_list\_to\_map(*arg\_list*, *label*)[¶](#opentimelineio.console.console_utils.arg_list_to_map "Permalink to this definition")

Convert an argument of the form -A foo=bar from the parsed result to a map.

opentimelineio.console.console\_utils.media\_linker\_name(*ml\_name\_arg*)[¶](#opentimelineio.console.console_utils.media_linker_name "Permalink to this definition")

Parse commandline arguments for the media linker, which can be not set (fall
back to default), “” or “none” (don’t link media) or the name of a media linker
to use.

---



## Page 54: Opentimelineio.Algorithms.Track Algo.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.track_algo.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.track_algo.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.algorithms](opentimelineio.algorithms.html)
* opentimelineio.algorithms.track\_algo
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.algorithms.track_algo.rst)


# opentimelineio.algorithms.track\_algo[¶](#module-opentimelineio.algorithms.track_algo "Permalink to this heading")

Algorithms for track objects.

opentimelineio.algorithms.track\_algo.track\_trimmed\_to\_range(*in\_track*, *trim\_range*)[¶](#opentimelineio.algorithms.track_algo.track_trimmed_to_range "Permalink to this definition")

Returns a new track that is a copy of the in\_track, but with items outside the
trim\_range removed and items on the ends trimmed to the trim\_range.

Note

The track is never expanded, only shortened.

Please note that you could do nearly the same thing non-destructively by just
setting the [`Track`](opentimelineio.core.html#opentimelineio.core.Track

"opentimelineio.core.Track")’s source\_range but sometimes you want to really
cut away the stuff outside and that’s what this function is meant for.

Parameters:

* **in\_track** ([*Track*](opentimelineio.core.html#opentimelineio.core.Track

  "opentimelineio.core.Track")) – Track to trim
* **trim\_range**
  ([*TimeRange*](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange

  "opentimelineio.opentime.TimeRange")) –
Returns:

New trimmed track

Return type:

[Track](opentimelineio.core.html#opentimelineio.core.Track

"opentimelineio.core.Track")

opentimelineio.algorithms.track\_algo.track\_with\_expanded\_transitions(*in\_track*)[¶](#opentimelineio.algorithms.track_algo.track_with_expanded_transitions "Permalink to this definition")

Expands transitions such that neighboring clips are trimmed into regions of
overlap.

For example, if your track is:

```
Clip1, T, Clip2

```

will return:

```
Clip1', (Clip1_t, T, Clip2_t), Clip2'

```

Where `Clip1'` is the part of `Clip1` not in the transition, `Clip1_t` is the
part inside the transition and so on.

Note

The items used in a transition are encapsulated in tuples.

Parameters:

**in\_track** ([*Track*](opentimelineio.core.html#opentimelineio.core.Track

"opentimelineio.core.Track")) – Track to expand

Returns:

Track

Return type:

[list](https://docs.python.org/3/library/stdtypes.html#list "(in Python

v3.12)")[[Track](opentimelineio.core.html#opentimelineio.core.Track

"opentimelineio.core.Track")]

---



## Page 55: Opentimelineio.Console.Otiostat.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiostat.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.console.otiostat.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.console](opentimelineio.console.html)
* opentimelineio.console.otiostat
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.console.otiostat.rst)


# opentimelineio.console.otiostat[¶](#module-opentimelineio.console.otiostat "Permalink to this heading")

Print statistics about the otio file, including validation information.

opentimelineio.console.otiostat.main()[¶](#opentimelineio.console.otiostat.main "Permalink to this definition")

main entry point

opentimelineio.console.otiostat.stat\_check(*name*)[¶](#opentimelineio.console.otiostat.stat_check "Permalink to this definition")

---



## Page 56: Opentimelineio.Adapters.Otio Json.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.otio_json.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.otio_json.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.adapters](opentimelineio.adapters.html)
* opentimelineio.adapters.otio\_json
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.adapters.otio_json.rst)


# opentimelineio.adapters.otio\_json[¶](#module-opentimelineio.adapters.otio_json "Permalink to this heading")

Adapter for reading and writing native .otio json files.

opentimelineio.adapters.otio\_json.read\_from\_file(*filepath*)[¶](#opentimelineio.adapters.otio_json.read_from_file "Permalink to this definition")

De-serializes an OpenTimelineIO object from a file

Args:

filepath (str): The path to an otio file to read from

Returns:

OpenTimeline: An OpenTimeline object

opentimelineio.adapters.otio\_json.read\_from\_string(*input\_str*)[¶](#opentimelineio.adapters.otio_json.read_from_string "Permalink to this definition")

De-serializes an OpenTimelineIO object from a json string

Args:

input\_str (str): A string containing json serialized otio contents

Returns:

OpenTimeline: An OpenTimeline object

opentimelineio.adapters.otio\_json.write\_to\_file(*input\_otio*, *filepath*, *target\_schema\_versions=None*, *indent=4*)[¶](#opentimelineio.adapters.otio_json.write_to_file "Permalink to this definition")

Serializes an OpenTimelineIO object into a file

Args:

> input\_otio (OpenTimeline): An OpenTimeline object filepath (str): The name of
> an otio file to write to indent (int): number of spaces for each json
> indentation level. Use -1 for no indentation or newlines.

If target\_schema\_versions is None and the environment variable
“OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL” is set, will read a map out of
that for downgrade target. The variable should be of the form FAMILY:LABEL, for
example “MYSTUDIO:JUNE2022”.

Returns:

bool: Write success

Raises:

ValueError: on write error otio.exceptions.InvalidEnvironmentVariableError: if
there is a problem with the default environment variable
“OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL”.

opentimelineio.adapters.otio\_json.write\_to\_string(*input\_otio*, *target\_schema\_versions=None*, *indent=4*)[¶](#opentimelineio.adapters.otio_json.write_to_string "Permalink to this definition")

Serializes an OpenTimelineIO object into a string

Args:

input\_otio (OpenTimeline): An OpenTimeline object indent (int): number of
spaces for each json indentation level. Use -1 for no indentation or newlines.

If target\_schema\_versions is None and the environment variable
“OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL” is set, will read a map out of
that for downgrade target. The variable should be of the form FAMILY:LABEL, for
example “MYSTUDIO:JUNE2022”.

Returns:

str: A json serialized string representation

Raises:

otio.exceptions.InvalidEnvironmentVariableError: if there is a problem with the
default environment variable “OTIO\_DEFAULT\_TARGET\_VERSION\_FAMILY\_LABEL”.

---



## Page 57: Opentimelineio.Adapters.File Bundle Utils.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.file_bundle_utils.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.file_bundle_utils.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.adapters](opentimelineio.adapters.html)
* opentimelineio.adapters.file\_bundle\_utils
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.adapters.file_bundle_utils.rst)


# opentimelineio.adapters.file\_bundle\_utils[¶](#module-opentimelineio.adapters.file_bundle_utils "Permalink to this heading")

Common utilities used by the file bundle adapters (otiod and otioz).

*class* opentimelineio.adapters.file\_bundle\_utils.MediaReferencePolicy[¶](#opentimelineio.adapters.file_bundle_utils.MediaReferencePolicy "Permalink to this definition")AllMissing *= 'AllMissing'*[¶](#opentimelineio.adapters.file_bundle_utils.MediaReferencePolicy.AllMissing "Permalink to this definition")ErrorIfNotFile *= 'ErrorIfNotFile'*[¶](#opentimelineio.adapters.file_bundle_utils.MediaReferencePolicy.ErrorIfNotFile "Permalink to this definition")MissingIfNotFile *= 'MissingIfNotFile'*[¶](#opentimelineio.adapters.file_bundle_utils.MediaReferencePolicy.MissingIfNotFile "Permalink to this definition")*exception* opentimelineio.adapters.file\_bundle\_utils.NotAFileOnDisk[¶](#opentimelineio.adapters.file_bundle_utils.NotAFileOnDisk "Permalink to this definition")opentimelineio.adapters.file\_bundle\_utils.reference\_cloned\_and\_missing(*orig\_mr*, *reason\_missing*)[¶](#opentimelineio.adapters.file_bundle_utils.reference_cloned_and_missing "Permalink to this definition")

Replace orig\_mr with a missing reference with the same metadata.

Also adds original\_target\_url and missing\_reference\_because fields.

---



## Page 58: Opentimelineio.Adapters.Otioz.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.otioz.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.otioz.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.adapters](opentimelineio.adapters.html)
* opentimelineio.adapters.otioz
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.adapters.otioz.rst)


# opentimelineio.adapters.otioz[¶](#module-opentimelineio.adapters.otioz "Permalink to this heading")

OTIOZ adapter - bundles otio files linked to local media

Takes as input an OTIO file that has media references which are all
ExternalReferences with target\_urls to files with unique basenames that are
accessible through the file system and bundles those files and the otio file
into a single zip file with the suffix .otioz. Can error out if files aren’t
locally referenced or provide missing references

Can also extract the content.otio file from an otioz bundle for processing.

Note that OTIOZ files \_always\_ use the unix style path separator (‘/’). This
ensures that regardless of which platform a bundle was created on, it can be
read on unix and windows platforms.

opentimelineio.adapters.otioz.read\_from\_file(*filepath*, *extract\_to\_directory=None*)[¶](#opentimelineio.adapters.otioz.read_from_file "Permalink to this definition")opentimelineio.adapters.otioz.write\_to\_file(*input\_otio*, *filepath*, *media\_policy='ErrorIfNotFile'*, *dryrun=False*)[¶](#opentimelineio.adapters.otioz.write_to_file "Permalink to this definition")

---



## Page 59: Opentimelineio.Adapters.Otiod.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.otiod.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.otiod.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.adapters](opentimelineio.adapters.html)
* opentimelineio.adapters.otiod
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.adapters.otiod.rst)


# opentimelineio.adapters.otiod[¶](#module-opentimelineio.adapters.otiod "Permalink to this heading")

OTIOD adapter - bundles otio files linked to local media in a directory

Takes as input an OTIO file that has media references which are all
ExternalReferences with target\_urls to files with unique basenames that are
accessible through the file system and bundles those files and the otio file
into a single directory named with a suffix of .otiod.

opentimelineio.adapters.otiod.read\_from\_file(*filepath*, *absolute\_media\_reference\_paths=False*)[¶](#opentimelineio.adapters.otiod.read_from_file "Permalink to this definition")opentimelineio.adapters.otiod.write\_to\_file(*input\_otio*, *filepath*, *media\_policy='ErrorIfNotFile'*, *dryrun=False*)[¶](#opentimelineio.adapters.otiod.write_to_file "Permalink to this definition")

---



## Page 60: Opentimelineio.Adapters.Adapter.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.adapter.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.adapters.adapter.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.adapters](opentimelineio.adapters.html)
* opentimelineio.adapters.adapter
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.adapters.adapter.rst)


# opentimelineio.adapters.adapter[¶](#module-opentimelineio.adapters.adapter "Permalink to this heading")

Implementation of the OTIO internal Adapter system.

For information on writing adapters, please consult:
<https://opentimelineio.readthedocs.io/en/latest/tutorials/write-an-adapter.html>

# noqa

*class* opentimelineio.adapters.adapter.Adapter[¶](#opentimelineio.adapters.adapter.Adapter "Permalink to this definition")

Adapters convert between OTIO and other formats.

Note that this class is not subclassed by adapters. Rather, an adapter is a
python module that implements at least one of the following functions:

```
write_to_string(input_otio)
write_to_file(input_otio, filepath) (optionally inferred)
read_from_string(input_str)
read_from_file(filepath) (optionally inferred)

```

…as well as a small json file that advertises the features of the adapter to
OTIO. This class serves as the wrapper around these modules internal to OTIO.
You should not need to extend this class to create new adapters for OTIO.

For more information:
<https://opentimelineio.readthedocs.io/en/latest/tutorials/write-an-adapter.html>.

# noqa

has\_feature(*feature\_string*)[¶](#opentimelineio.adapters.adapter.Adapter.has_feature "Permalink to this definition")

return true if adapter supports feature\_string, which must be a key of the
\_FEATURE\_MAP dictionary.

Will trigger a call to
[`PythonPlugin.module()`](opentimelineio.plugins.python_plugin.html#opentimelineio.plugins.python_plugin.PythonPlugin.module

"opentimelineio.plugins.python_plugin.PythonPlugin.module"), which imports the
plugin.

plugin\_info\_map()[¶](#opentimelineio.adapters.adapter.Adapter.plugin_info_map "Permalink to this definition")

Adds extra adapter-specific information to call to the parent fn.

read\_from\_file(*filepath*, *media\_linker\_name='\_\_default'*, *media\_linker\_argument\_map=None*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.adapter.Adapter.read_from_file "Permalink to this definition")

Execute the read\_from\_file function on this adapter.

If read\_from\_string exists, but not read\_from\_file, execute that with a
trivial file object wrapper.

read\_from\_string(*input\_str*, *media\_linker\_name='\_\_default'*, *media\_linker\_argument\_map=None*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.adapter.Adapter.read_from_string "Permalink to this definition")

Call the read\_from\_string function on this adapter.

*property* suffixes[¶](#opentimelineio.adapters.adapter.Adapter.suffixes "Permalink to this definition")

File suffixes associated with this adapter.

write\_to\_file(*input\_otio*, *filepath*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.adapter.Adapter.write_to_file "Permalink to this definition")

Execute the write\_to\_file function on this adapter.

If write\_to\_string exists, but not write\_to\_file, execute that with a
trivial file object wrapper.

write\_to\_string(*input\_otio*, *hook\_function\_argument\_map=None*, *\*\*adapter\_argument\_map*)[¶](#opentimelineio.adapters.adapter.Adapter.write_to_string "Permalink to this definition")

Call the write\_to\_string function on this adapter.

---



## Page 61: Opentimelineio.Schema.V2D.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.v2d.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.v2d.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.v2d
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.v2d.rst)


# opentimelineio.schema.v2d[¶](#module-opentimelineio.schema.v2d "Permalink to this heading")

---



## Page 62: Opentimelineio.Core.Mediareference.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.mediaReference.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.mediaReference.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.core](opentimelineio.core.html)
* opentimelineio.core.mediaReference
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.core.mediaReference.rst)


# opentimelineio.core.mediaReference[¶](#module-opentimelineio.core.mediaReference "Permalink to this heading")

---



## Page 63: Opentimelineio.Algorithms.Stack Algo.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.stack_algo.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.stack_algo.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.algorithms](opentimelineio.algorithms.html)
* opentimelineio.algorithms.stack\_algo
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.algorithms.stack_algo.rst)


# opentimelineio.algorithms.stack\_algo[¶](#module-opentimelineio.algorithms.stack_algo "Permalink to this heading")

Algorithms for stack objects.

opentimelineio.algorithms.stack\_algo.top\_clip\_at\_time(*in\_stack*, *t*)[¶](#opentimelineio.algorithms.stack_algo.top_clip_at_time "Permalink to this definition")

Return the topmost visible child that overlaps with time `t`.

Example:

```
tr1: G1, A, G2
tr2: [B------]
G1, and G2 are gaps, A and B are clips.

```

If `t` is within `A`, `A` will be returned. If `t` is within `G1` or `G2`, `B`
will be returned.

Parameters:

* **in\_stack** ([*Stack*](opentimelineio.schema.html#opentimelineio.schema.Stack

  "opentimelineio.schema.Stack")) – Stack
* **t**
  ([*RationalTime*](opentimelineio.opentime.html#opentimelineio.opentime.RationalTime

  "opentimelineio.opentime.RationalTime")) – Time
Returns:

Top clip

Return type:

[Clip](opentimelineio.schema.html#opentimelineio.schema.Clip

"opentimelineio.schema.Clip")

---



## Page 64: Opentimelineio.Algorithms.Filter.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.filter.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.filter.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.algorithms](opentimelineio.algorithms.html)
* opentimelineio.algorithms.filter
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.algorithms.filter.rst)


# opentimelineio.algorithms.filter[¶](#module-opentimelineio.algorithms.filter "Permalink to this heading")

Algorithms for filtering OTIO files.

opentimelineio.algorithms.filter.filtered\_composition(*root*, *unary\_filter\_fn*, *types\_to\_prune=None*)[¶](#opentimelineio.algorithms.filter.filtered_composition "Permalink to this definition")

Filter a deep copy of root (and children) with `unary_filter_fn`.

The `unary_filter_fn` must have this signature:

opentimelineio.algorithms.filter.func(*item: [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.12)")*) → [list](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.12)")[[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.12)")]

1. Make a deep copy of root
2. Starting with root, perform a depth first traversal
3. For each item (including root):

   1. If `types_to_prune` is not None and item is an instance of a type in
      `types_to_prune`, prune it from the copy, continue.
   2. Otherwise, pass the copy to `unary_filter_fn`. If `unary_filter_fn`:

      1. Returns an object: add it to the copy, replacing original
      2. Returns a tuple: insert it into the list, replacing original
      3. Returns None: prune it
4. If an item is pruned, do not traverse its children
5. Return the new deep copy.

Example 1 (filter):

```
If your unary function is:
    def fn(thing):
        if thing.name == B:
            return thing' # some transformation of B

        else:
            return thing

If you have a track: [A,B,C]

filtered_composition(track, fn) => [A,B',C]

```

Example 2 (prune):

```
If your unary function is:
    def fn(thing):
        if thing.name == B:
            return None
        else:
            return thing

filtered_composition(track, fn) => [A,C]

```

Example 3 (expand):

```
If your unary function is:
    def fn(thing):
        if thing.name == B:
            return tuple(B_1,B_2,B_3)
        else:
            return thing

filtered_composition(track, fn) => [A,B_1,B_2,B_3,C]

```

Example 4 (prune gaps):

```
track :: [Gap, A, Gap]
    filtered_composition(
        track, lambda _:_, types_to_prune=(otio.schema.Gap,)) => [A]

```

Parameters:

* **root**
  ([*SerializableObjectWithMetadata*](opentimelineio.core.html#opentimelineio.core.SerializableObjectWithMetadata

  "opentimelineio.core.SerializableObjectWithMetadata")) – Object to filter on
* **unary\_filter\_fn** – Filter function
* **types\_to\_prune**
  ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python

  v3.12)")*(*[*type*](https://docs.python.org/3/library/functions.html#type "(in

  Python v3.12)")*)*) – Types to prune. Example: (otio.schema.Gap,…)
opentimelineio.algorithms.filter.filtered\_with\_sequence\_context(*root*, *reduce\_fn*, *types\_to\_prune=None*)[¶](#opentimelineio.algorithms.filter.filtered_with_sequence_context "Permalink to this definition")

Filter a deep copy of root (and children) with `reduce_fn`.

The `reduce_fn` must have this signature:

\_.func(*previous\_item: [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.12)")*, *current: [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.12)")*, *next\_item: [Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.12)")*) → [list](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.12)")[[Any](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.12)")]

1. Make a deep copy of root
2. Starting with root, perform a depth first traversal
3. For each item (including root):

   1. if types\_to\_prune is not None and item is an instance of a type in
      types\_to\_prune, prune it from the copy, continue.
   2. Otherwise, pass (prev, copy, and next) to reduce\_fn. If `reduce_fn`:

      1. returns an object: add it to the copy, replacing original
      2. returns a tuple: insert it into the list, replacing original
      3. returns None: prune it

      Note

      `reduce_fn` is always passed objects from the original deep copy, not what prior
      calls return. See below for examples
4. If an item is pruned, do not traverse its children
5. Return the new deep copy.

Example 1 (filter):

```
>>> track = [A,B,C]
>>> def fn(prev_item, thing, next_item):
...     if prev_item.name == A:
...         return D # some new clip

...     else:
...         return thing
>>> filtered_with_sequence_context(track, fn) => [A,D,C]

order of calls to fn:
    fn(None, A, B) => A
    fn(A, B, C) => D
    fn(B, C, D) => C # !! note that it was passed B instead of D.

```

Example 2 (prune):

```
>>> track = [A,B,C]
>>> def fn(prev_item, thing, next_item):
...    if prev_item.name == A:
...        return None # prune the clip

...   else:
...        return thing
>>> filtered_with_sequence_context(track, fn) => [A,C]

order of calls to fn:
    fn(None, A, B) => A
    fn(A, B, C) => None
    fn(B, C, D) => C # !! note that it was passed B instead of D.

```

Example 3 (expand):

```
>>> def fn(prev_item, thing, next_item):
...     if prev_item.name == A:
...         return (D, E) # tuple of new clips

...     else:
...         return thing
>>> filtered_with_sequence_context(track, fn) => [A, D, E, C]

 the order of calls to fn will be:
    fn(None, A, B) => A
    fn(A, B, C) => (D, E)
    fn(B, C, D) => C # !! note that it was passed B instead of D.

```

Parameters:

* **root**
  ([*SerializableObjectWithMetadata*](opentimelineio.core.html#opentimelineio.core.SerializableObjectWithMetadata

  "opentimelineio.core.SerializableObjectWithMetadata")) – Object to filter on
* **reduce\_fn** – Filter function
* **types\_to\_prune**
  ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python

  v3.12)")*(*[*type*](https://docs.python.org/3/library/functions.html#type "(in

  Python v3.12)")*)*) – Types to prune. Example: (otio.schema.Gap,…)

---



## Page 65: Opentimelineio.Algorithms.Timeline Algo.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.timeline_algo.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.algorithms.timeline_algo.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.algorithms](opentimelineio.algorithms.html)
* opentimelineio.algorithms.timeline\_algo
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.algorithms.timeline_algo.rst)


# opentimelineio.algorithms.timeline\_algo[¶](#module-opentimelineio.algorithms.timeline_algo "Permalink to this heading")

Algorithms for timeline objects.

opentimelineio.algorithms.timeline\_algo.timeline\_trimmed\_to\_range(*in\_timeline*, *trim\_range*)[¶](#opentimelineio.algorithms.timeline_algo.timeline_trimmed_to_range "Permalink to this definition")

Returns a new timeline that is a copy of the in\_timeline, but with items
outside the trim\_range removed and items on the ends trimmed to the
trim\_range.

Note

the timeline is never expanded, only shortened.

Please note that you could do nearly the same thing non-destructively by just
setting the [`Track`](opentimelineio.core.html#opentimelineio.core.Track

"opentimelineio.core.Track")’s source\_range but sometimes you want to really
cut away the stuff outside and that’s what this function is meant for.

Parameters:

* **in\_timeline**
  ([*Timeline*](opentimelineio.schema.html#opentimelineio.schema.Timeline

  "opentimelineio.schema.Timeline")) – Timeline to trim
* **trim\_range**
  ([*TimeRange*](opentimelineio.opentime.html#opentimelineio.opentime.TimeRange

  "opentimelineio.opentime.TimeRange")) –
Returnd:

New trimmed timeline

Return type:

[Timeline](opentimelineio.schema.html#opentimelineio.schema.Timeline

"opentimelineio.schema.Timeline")

---



## Page 66: Opentimelineio.Plugins.Python Plugin.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.plugins.python_plugin.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.plugins.python_plugin.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.plugins](opentimelineio.plugins.html)
* opentimelineio.plugins.python\_plugin
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.plugins.python_plugin.rst)


# opentimelineio.plugins.python\_plugin[¶](#module-opentimelineio.plugins.python_plugin "Permalink to this heading")

Base class for OTIO plugins that are exposed by manifests.

*class* opentimelineio.plugins.python\_plugin.PythonPlugin[¶](#opentimelineio.plugins.python_plugin.PythonPlugin "Permalink to this definition")

A class of plugin that is encoded in a python module, exposed via a manifest.

*property* filepath[¶](#opentimelineio.plugins.python_plugin.PythonPlugin.filepath "Permalink to this definition")

Absolute path or relative path to adapter module from location of json.

module()[¶](#opentimelineio.plugins.python_plugin.PythonPlugin.module "Permalink to this definition")

Return the module object for this adapter.

module\_abs\_path()[¶](#opentimelineio.plugins.python_plugin.PythonPlugin.module_abs_path "Permalink to this definition")

Return an absolute path to the module implementing this adapter.

*property* name[¶](#opentimelineio.plugins.python_plugin.PythonPlugin.name "Permalink to this definition")

Adapter name.

plugin\_info\_map()[¶](#opentimelineio.plugins.python_plugin.PythonPlugin.plugin_info_map "Permalink to this definition")

Returns a map with information about the plugin.

opentimelineio.plugins.python\_plugin.plugin\_info\_map()[¶](#opentimelineio.plugins.python_plugin.plugin_info_map "Permalink to this definition")

---



## Page 67: Opentimelineio.Plugins.Manifest.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.plugins.manifest.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.plugins.manifest.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.plugins](opentimelineio.plugins.html)
* opentimelineio.plugins.manifest
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.plugins.manifest.rst)


# opentimelineio.plugins.manifest[¶](#module-opentimelineio.plugins.manifest "Permalink to this heading")

OTIO Python Plugin Manifest system: locates plugins to OTIO.

opentimelineio.plugins.manifest.ActiveManifest(*force\_reload=False*)[¶](#opentimelineio.plugins.manifest.ActiveManifest "Permalink to this definition")

Return the fully resolved plugin manifest.

*class* opentimelineio.plugins.manifest.Manifest[¶](#opentimelineio.plugins.manifest.Manifest "Permalink to this definition")

Defines an OTIO plugin Manifest.

This is considered an internal OTIO implementation detail.

A manifest tracks a collection of plugins and enables finding them by name or
other features (in the case of adapters, what file suffixes they advertise
support for).

For more information, consult the documenation.

adapter\_module\_from\_name(*name*)[¶](#opentimelineio.plugins.manifest.Manifest.adapter_module_from_name "Permalink to this definition")

Return the adapter module associated with a given adapter name.

adapter\_module\_from\_suffix(*suffix*)[¶](#opentimelineio.plugins.manifest.Manifest.adapter_module_from_suffix "Permalink to this definition")

Return the adapter module associated with a given file suffix.

*property* adapters[¶](#opentimelineio.plugins.manifest.Manifest.adapters "Permalink to this definition")

Adapters this manifest describes.

extend(*another\_manifest*)[¶](#opentimelineio.plugins.manifest.Manifest.extend "Permalink to this definition")

Aggregate another manifest’s plugins into this one.

During startup, OTIO will deserialize the individual manifest JSON files and use
this function to concatenate them together.

from\_filepath(*suffix*)[¶](#opentimelineio.plugins.manifest.Manifest.from_filepath "Permalink to this definition")

Return the adapter object associated with a given file suffix.

from\_name(*name*, *kind\_list='adapters'*)[¶](#opentimelineio.plugins.manifest.Manifest.from_name "Permalink to this definition")

Return the plugin object associated with a given plugin name.

*property* hook\_scripts[¶](#opentimelineio.plugins.manifest.Manifest.hook_scripts "Permalink to this definition")

Scripts that can be attached to hooks.

*property* hooks[¶](#opentimelineio.plugins.manifest.Manifest.hooks "Permalink to this definition")

Hooks that hooks scripts can be attached to.

*property* media\_linkers[¶](#opentimelineio.plugins.manifest.Manifest.media_linkers "Permalink to this definition")

Media Linkers this manifest describes.

schemadef\_module\_from\_name(*name*)[¶](#opentimelineio.plugins.manifest.Manifest.schemadef_module_from_name "Permalink to this definition")

Return the schemadef module associated with a given schemadef name.

*property* schemadefs[¶](#opentimelineio.plugins.manifest.Manifest.schemadefs "Permalink to this definition")

Schemadefs this manifest describes.

*property* version\_manifests[¶](#opentimelineio.plugins.manifest.Manifest.version_manifests "Permalink to this definition")

Sets of versions to downgrade schemas to.

opentimelineio.plugins.manifest.load\_manifest()[¶](#opentimelineio.plugins.manifest.load_manifest "Permalink to this definition")

Walk the plugin manifest discovery systems and accumulate manifests.

The order of loading (and precedence) is:

> 1. Manifests specified via the
>    [OTIO\_PLUGIN\_MANIFEST\_PATH](../../tutorials/otio-env-variables.html#term-OTIO_PLUGIN_MANIFEST_PATH)

>    variable
> 2. Entrypoint based plugin manifests
> 3. Builtin plugin manifest

opentimelineio.plugins.manifest.manifest\_from\_file(*filepath*)[¶](#opentimelineio.plugins.manifest.manifest_from_file "Permalink to this definition")

Read the .json file at filepath into a
[`Manifest`](#opentimelineio.plugins.manifest.Manifest

"opentimelineio.plugins.manifest.Manifest") object.

opentimelineio.plugins.manifest.manifest\_from\_string(*input\_string*)[¶](#opentimelineio.plugins.manifest.manifest_from_string "Permalink to this definition")

Deserialize the json string into a manifest object.

opentimelineio.plugins.manifest.plugin\_entry\_points()[¶](#opentimelineio.plugins.manifest.plugin_entry_points "Permalink to this definition")

Returns the list of entry points for all available OpenTimelineIO plugins.

---



## Page 68: Opentimelineio.Schema.Box2D.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.box2d.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.box2d.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.box2d
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.box2d.rst)


# opentimelineio.schema.box2d[¶](#module-opentimelineio.schema.box2d "Permalink to this heading")

---



## Page 69: Opentimelineio.Schema.External Reference.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.external_reference.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.external_reference.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.external\_reference
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.external_reference.rst)


# opentimelineio.schema.external\_reference[¶](#module-opentimelineio.schema.external_reference "Permalink to this heading")

---



## Page 70: Opentimelineio.Schema.Schemadef.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.schemadef.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.schemadef.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.schemadef
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.schemadef.rst)


# opentimelineio.schema.schemadef[¶](#module-opentimelineio.schema.schemadef "Permalink to this heading")

*class* opentimelineio.schema.schemadef.SchemaDef[¶](#opentimelineio.schema.schemadef.SchemaDef "Permalink to this definition")module()[¶](#opentimelineio.schema.schemadef.SchemaDef.module "Permalink to this definition")

Return the module object for this schemadef plugin. If the module hasn’t already
been imported, it is imported and injected into the otio.schemadefs namespace as
a side-effect.

Redefines
[`PythonPlugin.module()`](opentimelineio.plugins.python_plugin.html#opentimelineio.plugins.python_plugin.PythonPlugin.module

"opentimelineio.plugins.python_plugin.PythonPlugin.module").

plugin\_info\_map()[¶](#opentimelineio.schema.schemadef.SchemaDef.plugin_info_map "Permalink to this definition")

Adds extra schemadef-specific information to call to the parent fn.

opentimelineio.schema.schemadef.available\_schemadef\_names()[¶](#opentimelineio.schema.schemadef.available_schemadef_names "Permalink to this definition")

Return a string list of the available schemadefs.

opentimelineio.schema.schemadef.from\_name(*name*)[¶](#opentimelineio.schema.schemadef.from_name "Permalink to this definition")

Fetch the schemadef plugin object by the name of the schema directly.

opentimelineio.schema.schemadef.module\_from\_name(*name*)[¶](#opentimelineio.schema.schemadef.module_from_name "Permalink to this definition")

Fetch the plugin’s module by the name of the schemadef.

Will load the plugin if it has not already been loaded. Reading a file that
contains the schemadef will also trigger a load of the plugin.

---



## Page 71: Opentimelineio.Schema.Transition.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.transition.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.transition.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.transition
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.transition.rst)


# opentimelineio.schema.transition[¶](#module-opentimelineio.schema.transition "Permalink to this heading")

---



## Page 72: Opentimelineio.Schema.Serializable Collection.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.serializable_collection.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.serializable_collection.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.serializable\_collection
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.serializable_collection.rst)


# opentimelineio.schema.serializable\_collection[¶](#module-opentimelineio.schema.serializable_collection "Permalink to this heading")

---



## Page 73: Opentimelineio.Schema.Clip.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.clip.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.clip.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.clip
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.clip.rst)


# opentimelineio.schema.clip[¶](#module-opentimelineio.schema.clip "Permalink to this heading")

---



## Page 74: Opentimelineio.Schema.Timeline.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.timeline.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.timeline.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.timeline
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.timeline.rst)


# opentimelineio.schema.timeline[¶](#module-opentimelineio.schema.timeline "Permalink to this heading")

---



## Page 75: Opentimelineio.Schema.Marker.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.marker.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.marker.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.marker
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.marker.rst)


# opentimelineio.schema.marker[¶](#module-opentimelineio.schema.marker "Permalink to this heading")

---



## Page 76: Opentimelineio.Schema.Generator Reference.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.generator_reference.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.generator_reference.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.generator\_reference
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.generator_reference.rst)


# opentimelineio.schema.generator\_reference[¶](#module-opentimelineio.schema.generator_reference "Permalink to this heading")

---



## Page 77: Opentimelineio.Schema.Image Sequence Reference.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.image_sequence_reference.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.image_sequence_reference.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.image\_sequence\_reference
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.image_sequence_reference.rst)


# opentimelineio.schema.image\_sequence\_reference[¶](#module-opentimelineio.schema.image_sequence_reference "Permalink to this heading")

---



## Page 78: Opentimelineio.Schema.Effect.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.effect.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.schema.effect.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.schema](opentimelineio.schema.html)
* opentimelineio.schema.effect
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.schema.effect.rst)


# opentimelineio.schema.effect[¶](#module-opentimelineio.schema.effect "Permalink to this heading")

---



## Page 79: Opentimelineio.Core.Composable.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.composable.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.composable.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.core](opentimelineio.core.html)
* opentimelineio.core.composable
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.core.composable.rst)


# opentimelineio.core.composable[¶](#module-opentimelineio.core.composable "Permalink to this heading")

---



## Page 80: Opentimelineio.Core.Composition.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.composition.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.composition.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.core](opentimelineio.core.html)
* opentimelineio.core.composition
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.core.composition.rst)


# opentimelineio.core.composition[¶](#module-opentimelineio.core.composition "Permalink to this heading")

---



## Page 81: Opentimelineio.Core.Item.Html

**Source:** [https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.item.html](https://opentimelineio.readthedocs.io/en/stable/api/python/opentimelineio.core.item.html)

* [Python](../../python_reference.html)
* [opentimelineio](opentimelineio.html)
* [opentimelineio.core](opentimelineio.core.html)
* opentimelineio.core.item
* [Edit on GitHub](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/4440afaa27b16f81cdf81215ce4d0b08e1424148/docs/api/python/opentimelineio.core.item.rst)


# opentimelineio.core.item[¶](#module-opentimelineio.core.item "Permalink to this heading")

---

