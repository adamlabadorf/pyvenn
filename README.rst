
pyvenn
======

A general purpose library for producing 2-D Venn diagram graphics in python

Example::

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

.. image:: https://github.com/adamlabadorf/pyvenn/blob/master/venn.png
