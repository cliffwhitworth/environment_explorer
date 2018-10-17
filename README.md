# environment_explorer
Exploring environment data such as the Global Historical Climatology Network-Monthly (GHCN-M) temperature dataset

A Plotly / Dash project with Jupyter Notebooks

## Getting Started

Use the .py and .pkl files in a Python3 environment

Data can be found here:
* https://www.ncdc.noaa.gov/ghcnm/v3.php
* For ID check ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3/README
* https://www.wmo.int/cpdb/volume_a_observing_stations/list_stations

<!--
### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```
-->

The Jupyter Notebook files with a short description follow:
* ghcnm.ipynb: Prepares a 75+ Mb .pkl file of ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3/csv/ghcnm.tavg.v3.3.0.20170710.qca.dat.csv
* create_small_ghcnm_pkl.ipynb: Prepares a smaller .pkl file of just the annual monthly mean temperatures
* ghcnm_pkl.ipynb: Playground for the larger .pkl dataset
* ghcnm_small_pkl.ipynb: Playground for the annual monthly dataset

Note: ghcnm.py is the Plotly / Dash app

<!--
## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```
-->

## Deployment

See app on [HEROKU](https://ghcnm.herokuapp.com/)

## Built With

* Python, Plotly, Dash

<!--
## Contributing

Please read [CONTRIBUTING.md](https://github.com/cliffwhitworth/environment_explorer) for details on our code of conduct, and the process for submitting pull requests to us.
-->

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Cliff Whitworth** - *Initial work* - [cliffwhitworth](https://github.com/cliffwhitworth/studynotes)

<!--
See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
-->

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to Jose Portilla at Udemy
