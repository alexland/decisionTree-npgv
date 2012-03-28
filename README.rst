===============
decisionTree-ngpv
===============

recursive descent parser based on C4.5, implemented using python + numpy (computation engine) and graphviz (tree layout + rendering)

<img src="http://alexland.github.com/decisionTree-npgv/images/dTree-image1.png" alt="decision tree image" title="sample output" />
<br />



Requirements
============

* `Python <http://www.python.org>` _ 2.6 or higher
* `NumPy <http://numpy.scipy.org/>` _ 1.5 or higher
* `Flask <http://flask.pocoo.org/>`_ 0.8 or higher
* `PyGraphviz <http://networkx.lanl.gov/pygraphviz/>`_ 1.0 or higher


Installation
============



License
=======

``npgv-decisionTree`` is licensed under the MIT license

Configuration
=============


Usage
=====

Basic
-----

    import numpy as NP
    import dTree as DT
    
    tree = DT.dtree(sample_data)
    tree.render_tree()



Test application
----------------




Bugs, feature requests?
=======================

If you find a bug in ``npgv-decisionTree`` i would like to know about it; so please add new issue to this Project's `GitHub issues
<https://github.com/alexland/npgv-decisionTree/issues>`_.
