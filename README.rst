The SnapPy manifold database for plausibly slice knots
======================================================

The PlausibleKnots database consists of those nontrivial prime knots
with at most 19 crossings whose signature is 0 and whose Alexander
polynomial satisfies the Fox-Milnor condition.  The data on these 3.9
million knots takes up about 1.1G of disk space.

To install the latest version of this Python module, you can do::

  python -m pip install plausible_knots

If you are using SageMath, replace this with::

  sage -pip install plausible_knots

Please note this will take about a minute as it's downloading 1.1G of
raw data as part of the ``build_wheel`` step.

Assuming you have installed SnapPy into this Python, you can now start
Python and do::

  >>> import snappy
  >>> import plausible_knots      # Skip if using Python 3.3.2 or newer.
  >>> len(snappy.PlausibleKnots)
  3869541
  >>> K = snappy.PlausibleKnots[100000]; K
  17nh_1645806(0,0)
  >>> K.volume()
  24.3340174921580
  >>> M = snappy.PlausibleKnots['19nh_045358315']
  >>> M.identify()
  [19nh_045358315(0,0)]

The raw data is available on the `GitHub repository
<https://github.com/NathanDunfield/plausible_knots>`_ and archived on
the `Dataverse <https://doi.org/10.7910/DVN/YBDTBT>`_.
