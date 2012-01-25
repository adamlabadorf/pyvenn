.. pyvenn documentation master file, created by
   sphinx-quickstart on Wed Jan 25 15:53:50 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyvenn's documentation!
==================================

This is all the documentation for this module.

Example:

  >>> from pyvenn import do_venn
  >>> from matplotlib.pyplot import show
  >>> do_venn(10, 10, 0)
  >>> do_venn(10, 50, 10)
  >>> do_venn(100, 50, 10)
  >>> do_venn(100, 50, 40)
  >>> show()
  >>> do_venn(100, 50, 40,plot_fn='venn.png')

This example code is at the bottom of pyvenn.py.  Look at venn.png for example
output.

.. image:: venn.png

.. automodule:: pyvenn

This is the function you'll probably want to use:

.. autofunction:: do_venn

These are helper functions that you probably won't need to use but are included
nonetheless:

.. autofunction:: bezier_circle
.. autofunction:: trig_circle
.. autofunction:: quadratic_bezier_curve
.. autofunction:: quadratic_bezier_point
.. autofunction:: cubic_bezier_curve
.. autofunction:: find_best_d


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

