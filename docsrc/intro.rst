.. title:: SPIF Overview

==========
Motivation
==========

A variety of binary file formats are used by the manufacturers of Optical Array Probes (OAPs) to transmit and store particle image data. The formats are/were designed around hardware and bandwidth limitations and so may not have a convenient or standard binary structure. This has meant that users must write their own routines for reading image data for processing and analysis. We propose a new file format for OAP raw image data called the Single Particle Image Format (SPIF). The new format will specify a single structure which all imaging probe data formats may be translated into leading to improved accessibility for users and a refinement of (now common) data processing routines. It may be that this format could be adopted by instrument manufacturers so that all raw image data is immediately available in a standard format. The format is also suitable for the long-term archiving of raw data and so has the potential to satisfy usage requirements across the range of usage environments.

==========
Structure
==========

The SPIF file uses the `NetCDF4 format <https://www.unidata.ucar.edu/software/netcdf/>`_. NetCDF4 is a structured binary file format capable of containing large datasets and has automatic compression
utilities. NetCDF4 is widely supported on a variety of platforms and environments.

Data will be contained within **instrument groups** inside the SPIF file. Only data from a single instrument in contained in a single SPIF file however different instrument channels may be stored in different groups and so be kept together. Group attributes allow the specific instrument to be identified along with instrument hardware and software parameters.

In a similar fashion to the `CF (Climate and Forecast) Conventions <http://cfconventions.org/>`_, the SPIF conventions define a minimum structure, in terms of groups, variables, and attributes, for compliance. Any additional data contained within the file is optional but should not conflict with the standards. Any suggested but optional data for inclusion are given in *italics*. Due to the focussed type of data, SPIF conventions are more demanding of variable and attribute names than the CF conventions are. SPIF follows the CF `scoping guidelines <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#groups>`_ in that dimensions are visible to all child groups.