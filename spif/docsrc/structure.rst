.. title:: SPIF Structure


*********
Structure
*********

The SPIF file uses the `NetCDF4 format <https://www.unidata.ucar.edu/software/netcdf/>`_. NetCDF4 is a structured binary file format capable of containing large datasets and has automatic compression utilities. NetCDF4 is widely supported on a variety of platforms and environments.

In a similar fashion to the `CF (Climate and Forecast) Conventions <http://cfconventions.org/>`_, the SPIF conventions define a minimum structure, in terms of groups, variables, and attributes, for compliance. Any additional data contained within the file is optional but should not conflict with the standards. Any suggested but optional data for inclusion are given in *italics*. Due to the focussed type of data, SPIF conventions are more demanding of variable and attribute names than the CF conventions are. SPIF follows the CF `scoping guidelines <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#groups>`_ in that dimensions are visible to all child groups.


===================
Instrument Channels
===================

Data is contained within **instrument channel groups** inside the SPIF file. Only data from a single probe is contained in a single SPIF file however some instruments may have more than one channel, for example the `SPEC 2DS <http://www.specinc.com/2d-s-stereo-probe-operation>`_ has vertical and horizontal channels with each detecting particles independently, essentially behaving
as independent instruments. For a probe that is made up of multiple instruments (e.g., 2DS, 3V-CPI, etc) where the particle detection will not be coincident, data is split into different instrument groups but this allows keeping these data together in a single file. The instrument channel group names are not pre-defined but should be self-explainatory and further information is included as attributes of these groups.


.. _image-array-structure:

=========================
Raw Image Array Structure
=========================

Flattened image data is stored in the instrument ``core`` group as a 1-dimensional array. The length of this array is the product of the number of images, given by the dimension ``image_num``, and the width and height of each image. Depending on the type of instrument, the width and/or height may be fixed or variable for each image.

.. note::
    It is (in)conceivable that a future probe may natively produce 3-dimensional images. In this case the 1-dimensional image array would still work perfectly well, just another variable of ``length`` in this new dimension would need to be added. Something for a new version of the convention once/if that ever happens!

In order to reconstruct the 2-dimensional images from the flattened array two variables are provided, ``width`` and ``height``, these are of length ``image_num``.

.. note::
    It is possible that ``width`` is given as a scalar variable instead of an array of length ``image_num``?

More details about this is included in the section on :ref:`core`.


===============================
Mandatory and Optional Contents
===============================

As mentioned above, the SPIF definition is somewhat constrained to ensure that standard-compliant files contain all the information/data required for future processing. SPIF files must contain, as a minimum, a set of mandatory parameters. That is groups, attributes, and (coordinate) variables.

    :doc:`List of Mandatory Parameters <spif_mandatory_params>`

In addition to these mandatory netCDF parameters, a SPIF file can be extended with additional groups, attributes, and (coordinate) variables. It may assist users if these added parameters are familiar and so some suggested optional parameters are listed below.

    :doc:`List of Optional Parameters <spif_optional_params>`