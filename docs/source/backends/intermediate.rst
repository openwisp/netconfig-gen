.. _airos-intermediate-representation:

Intermediate representation
---------------------------

The intermediate representation is the output of the a **converter**,
it is backend specific and is built as a tree structure made from python
builtins values.

A tree is a *acyclic, directional graph* with an element called *root*.

The root of our tree is stored in the first element of a tuple, along with
the root's direct sons as a list:

.. code-block:: python

    tree = (root, direct_sons)

As an example here we present the tree `('spam', ['eggs', 'snakes'])`

.. graphviz::

   digraph tree {
        spam -> eggs;
        spam -> snakes;
   }

As a son may be a carrier of a value so we store it in a dictionary instead of adding a *leaf*
with another level of recursion.

As an example here we present the tree `('spam', [ { 'eggs': 2 }, { 'snakes' : { 'loved' : 'python' }}])`:

.. graphviz::

   digraph tree {
        
        eggs[label="{ eggs : 2 }"];
        loved[label="{ loved : python }"];

        spam -> eggs;
        spam -> snakes -> loved;

   }

This tree could be tranlated to a configuration file for AirOS that looks like this:

.. code-block:: ini

   spam.eggs=2
   spam.snakes.loved=python


So our tree representation is based on the simple assumption that a *leaf* is a dictionary
without nested values and nested values in a dictionary creates a father-son relationship.

Instead when the configuration requires that the son values must be prefixed from a number,
e.g. `vlan.1.devname=eth0` we store a list of dictionaries.

.. code-block:: python

   (
        'spam',
        [
            {
                'eggs' : 2,
            },
            {
                'snakes' : {
                    'loved' : [
                        {
                            'python2' : True,
                        },
                        {
                            'python3' : True,
                        },
                        {
                            'ipython' : True,
                        }
                     ],
                 },
            }
        ]
   )

And the resulting tree is:

.. graphviz::

   digraph tree {
        
        eggs[label="{ eggs : 2 }"];
        loved;

        python2[label="{ python2 : True }"];
        python3[label="{ python3 : True }"];
        ipython[label="{ ipython : True }"];

        spam -> eggs;
        spam -> snakes -> loved;

        loved -> {1};
        loved -> {2};
        loved -> {3};

        1 -> python2;
        2 -> python3;
        3 -> ipython;

   }

And the configuration is:

.. code-block:: ini

    spam.eggs=2
    spam.snakes.loved.1.python2=true
    spam.snakes.loved.2.python3=true
    spam.snakes.loved.2.ipython=true

The process by which we can go from the intermediate representation from
the output configuration is called flattening, you can find more in the next section.

Flattening
----------

To avoid at all cost a recursive logic in the template we flatten the intermediate
representation to something that has a *namespace* a *key* and a *value*.

The objective is to go from a python :ref:`configuration_dictionary` that we get from loading a NetJSON to the AirOS configuration.

An input :ref:`configuration_dictionary` is just a python dictionary, e.g.:


.. code-block:: python

   #python
   {
        'interfaces' : [
            {
                'name' : 'eth0.1',
                'type' : 'ethernet',
                'comment' : 'management vlan'
                'comment' : 'management'
            },
            {
                'name' : 'eth0.2',
                'type' : 'ethernet',
                'comment' : 'traffic'
            }
        ]
   }


And this must be converted to an appropiate AirOS configuration which looks like this:

.. code-block:: ini

   vlan.1.comment=management
   vlan.1.devname=eth0
   vlan.1.id=1
   vlan.1.status=enabled
   vlan.2.comment=management
   vlan.2.devname=eth0
   vlan.2.id=2
   vlan.2.status=enabled
   vlan.status=enabled

To do this we must convert the :ref:`configuration_dictionary` into something that
resembles the target text, the output configuration.

.. code-block:: python

   (
        # namespace
        'vlan',
        #options
        [
            {
                # key : value
                '1.devname' : 'eth0',
                '1.id' : '1'
                '1.status' : 'enabled',
                '1.comment' : 'management'
            },
            {
                '2.devname' : 'eth0',
                '2.id' : '2'
                '2.status' : 'enabled',
                '2.comment' : 'traffic'
            }
        ]
   )

And to do that we get rid of the multiple indentation levels by flattening the tree structure.

The tree associated with the previous NetJSON example is this:

.. graphviz::

   digraph tree {
        vlan -> 1;
        vlan -> 2;
        devname1        [label="devname=eth0"];
        devname2        [label="devname=eth0"];

        id1             [label="id=1"];
        id2             [label="id=2"];

        status1         [label="status=enabled"];
        status2         [label="status=enabled"];

        comment1        [label="comment=management"];
        comment2        [label="comment=traffic"];

        1 -> devname1;
        1 -> id1;
        1 -> status1;
        1 -> comment1;
        2 -> devname2;
        2 -> id2;
        2 -> status2;
        2 -> comment2;
   }

And by exploring depth first we get to read a line of the configuration at a time.

E.g. following the blue line from the `vlan` root to the first `leaf` we have the 
configuration `vlan.1.devname=eth0`

.. graphviz::

   digraph tree {
        vlan -> 1       [color="blue"];
        devname1        [label="devname=eth0"];

        id1             [label="id=1"];

        status1         [label="status=enabled"];

        comment1        [label="comment=management"];

        1 -> devname1 [color="blue"];
        1 -> id1;
        1 -> status1;
        1 -> comment1;
   }
