# Job Crawler


Job Crawler is a project crawling job information for the job website


source code is made available under the [Apache 2.0 license](https://github.com/SeleniumHQ/selenium/blob/master/LICENSE).


## Installation

### Install MongoDB

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


### Install python environment

Now, we need to install the python environment and all dependent packages. And all steps to build the environment has been scripted in `install_env`. 

So you can install environment just through runing the script.
```sh
./install_env
```


## Run

you can run code [code/service.py](https://github.com/david-liu/job_crawler/blob/master/code/service.py) to crawling the test job website.

```sh
code/service.py
```
and the crawling results will been printed in the console.

If you want to store the data in MongoDB's database, you can run the commond with `-o` argument

```sh
code/service.py -o mongodb
```

and the results will save in the `jobs` collection of `jobs_db` database

## Extension

If you want to crawl another website or another part of a website, you need to define a `RunConfig` in the directory of `code\configs`

the customized config should be the instance of `RunConfig` in [code/core/run_config.py](https://github.com/david-liu/job_crawler/blob/master/code/core/run_config.py).

For more information, please reference [code/configs/qiaobutang_top20.py](https://github.com/david-liu/job_crawler/blob/master/code/configs/qiaobutang_top20.py) and [code/configs/shixiseng.py](https://github.com/david-liu/job_crawler/blob/master/code/configs/shixiseng.py)

