.. SPIF documentation master file, created by
   sphinx-quickstart on Wed Mar  3 11:37:48 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. title:: SPIF - Single Particle Image Format

===================================
SPIF - Single Particle Image Format
===================================

----------
Motivation
----------

A variety of binary file formats are used by the manufacturers of Optical Array Probes (OAPs) to transmit and store particle image data. The formats are/were designed around hardware and bandwidth limitations and so may not have a convenient or standard binary structure. This has meant that users must write their own routines for reading image data for processing and analysis. We propose a new file format for OAP raw image data called the Single Particle Image Format (SPIF). The new format will specify a single structure which all imaging probe data formats may be translated into leading to improved accessibility for users and a refinement of (now common) data processing routines. It may be that this format could be adopted by instrument manufacturers so that all raw image data is immediately available in a standard format. The format is also suitable for the long-term archiving of raw data and so has the potential to satisfy usage requirements across the range of usage environments.

OAP images are created by triggering a 1-dimensional array of photodiodes on a nanosecond timescale to create a series of slices as a particle travels through the sample volume. These slices are used to construct a 2-dimensional image of the particle with a set width that corresponds to the number of photodiodes in the 1-dimensional array and a variable length that depends on the size and shape of the particle. True 2-dimensional images produced by a 2-dimensional CCD or similar photodetector can also be stored in the SPIF structure. The dimensions of the produced images may not have a fixed size, for example probes such as the `SPEC 3V-CPI <http://www.specinc.com/3v-cpi-combo>`_ define a region of interest that is constrained by the image size in order to reduce data bandwidth requirements and file size. SPIF files can contain both of these types of images which increases it's flexibility and future-proofs the convention, more details are given in :ref:`image-array-structure`.



--------
Contents
--------

.. toctree::
    :maxdepth: 2

    structure
    definition
    params_mandatory
    Mandatory Parameter List <spif_mandatory_params>
    params_optional
    Optional Parameter List <spif_optional_params>


--------------
Current Status
--------------

    .. tabularcolumns:: |r|l|

    .. list-table::
        :header-rows: 0
        :align: left
        :widths: auto

        * - Project
          - |ProjectTitle|
        * - Description
          - |ProjectDescription|
        * - Project repository
          - `<https://github.com/graemenott/SPIF>`_
        * - Project version
          - |ProjectVersion|
        * - Python version
          - |PythonVersion|
        * - Created
          - Long ago...
        * - Modified
          - |today|



