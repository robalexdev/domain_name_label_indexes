=========================
Domain Name Label Indexes
=========================


.. image:: https://img.shields.io/pypi/v/domain_name_label_indexes.svg
        :target: https://pypi.python.org/pypi/domain_name_label_indexes

.. image:: https://img.shields.io/travis/ralexander-phi/domain_name_label_indexes.svg
        :target: https://travis-ci.com/ralexander-phi/domain_name_label_indexes

.. image:: https://readthedocs.org/projects/domain-name-label-indexes/badge/?version=latest
        :target: https://domain-name-label-indexes.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

This library helps generate minimal domain name labels in an ordered fashion.
The following rules apply:

* The label can contain only 0-9, a-z, and hyphen (-)
* The label cannot begin or end with a hyphen
* The label cannot contain two hyphens in a row
* The label must be between 1 and 63 characters long

Note:

* Unicode / Punycode are not considered (I.E., domains starting with `xn--` will not be generated).
* Binary labels are not considered

Specifically, this library defines an ordering to domains such that they may be looked up by index.
Domains are orders such that shorter domains occur earlier and domains of the same length occur in sorted order.
The ordering begins as:

    0    -> "0"

    1    -> "1"

    ...

    10   -> "a"

    ...

    35   -> "z"

    36   -> "00"

    ...

    72   -> "10"

    ...

    1331 -> "zz"

    1332 -> "0-0"

* Free software: MIT license


Features
--------


Given an index, compute the corresposing domain name.

    generate_domain_name_label(index: int)

For example:

    generate_domain_name_label(0) => "0"

    generate_domain_name_label(37) => "01"



Given an index, compute the length of the domain name.

    compute_domain_length(index: int)

For example:

    compute_domain_length(0) => 1

    compute_domain_length(36) => 2


Find the first index that produces a domain of a given length.

    first_index_with_domain_length(length: int)

For example:

    first_index_with_domain_length(1) => 0

    first_index_with_domain_length(2) => 36



Compute the number of domains that have a given length.

    count_domains_with_length(length: int)

For example:

    count_domains_with_length(1) => 36

    count_domains_with_length(2) => 1296

Compute the index for a domain name label.

    index_of_domain_name_label(label: str)

For example:

    index_of_domain_name_label("google") => 1191294986

    index_of_domain_name_label("yahoo")  =>   64297428


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
