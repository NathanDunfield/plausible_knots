The SnapPy manifold database for plausibly slice knots
======================================================

The PlausibleKnots database consists of those nontrivial prime knots
with at most 19 crossings whose signature is 0 and whose Alexander
polynomial satisfies the Fox-Milnor condition.  To install this Python
module, navigate into this directory in your terminal and do::

To install the latest version of this Python module, you can do::

  python -m pip install plausible_knots

If you are using SageMath, replace this with::

  sage -pip install plausible_knots

Assuming you have installed SnapPy into this Python, you can now start
Python and do::

  >>> import snappy
  >>> import plausible_knots
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
