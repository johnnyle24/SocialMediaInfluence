# Social Media Influence

Various heuristics for maximizing influence in social networks

## Getting started

### Installation
This project requires Snap
(which only works with python 2.7, and is not available via pip),
[install it here](https://snap.stanford.edu/snappy/)

It also requires networkx-metis (for which the pip install does not work),
[install it here](https://snap.stanford.edu/snappy/)

Then, install the requirements using `pip install -r requirements.txt`

### How to run
The following files will run various heuristics, and output the influence
of the best found set.  The input parameter *k* corresponds to the size
of the initial set of activated nodes.
```
python greedy.py [k]
python partition.py [k]
```

## Authors
* **Kyle Pierson** - [Github](https://github.com/kyledpierson)
* **Johnny Le** - [Github](https://github.com/johnnyle24)
* **Pierce Darragh** - [Github](https://github.com/pdarragh)

## License
This project is licensed under the MIT License -
see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Aditya Bhaskara
