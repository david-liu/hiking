# Job Crawler


Job Crawler is a probect crawling job information for the job website


source code is made available under the [Apache 2.0 license](https://github.com/SeleniumHQ/selenium/blob/master/LICENSE).


## Installation

### install mongodb

* Update Homebrew’s package database
```sh
brew update
```

* Install MongoDB
```sh
brew install mongodb
```

* Start MongoDB
```sh
brew services start mongodb
```


### install python environment

Now, we will need install the python environment and dependent packages. All steps to build the environment has been scripted in `install_env`. So you can install environment through runing the script.
```sh
./install_env
```


## Run

you can run code `code/service.py` to crawling the test job website.

```sh
python code/service.py
```

add the crawling results will been stored in the `job` collection of database 'jobs_db'
