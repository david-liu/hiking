# Job Crawler


Job Crawler is a project crawling job information from a job website


Source code is made available under the [Apache 2.0 license](https://github.com/SeleniumHQ/selenium/blob/master/LICENSE).


## Installation

### Firefox

The project will use Firefox as the driver to crawl web pages, please make sure that Firefox has been installed in your computer

### PhantomJS

The crawler also can run without GUI (Firefox), which means it can crawling pages in headless browser mode. 

In order to support this, you need to download webkit [PhantomJS](http://phantomjs.org/download.html), and extract it in your computer


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

* Export crawling results
```
mongoexport --db jobs_db --collection jobs --out jobs_160924.csv --type=csv --fields industry,company,job_name,location,deadline,url,updated_date,created_at
```


### Install python environment

Now, we need to install the python environment and all dependent packages. And all steps to build the environment has been scripted in `install_env`.

So you can install environment just through running the script.
```sh
./install_env
```


## Run

You can run code [code/app.py](https://github.com/david-liu/job_crawler/blob/dev/code/app.py) to crawling the test job website.
```sh
code/app.py
```
and the crawling results will been printed in the console.

If you want to store the data in MongoDB's database, you can run the commond with `-o` argument
```sh
code/app.py -o mongodb
```
and the results will save in the `jobs` collection of `jobs_db` database


If you want to start the crawler in headless browser model, you cran run the command with `--headless` argument to specify the location of the [PhantomJS](http://phantomjs.org/) webkit
```sh
code/app.py --headless=[the location of the binary package of phantomjs]
```

Try with `-h` argument for more information

```sh
code/app.py -h
```

## Extension

If you want to crawl another website or another part of a website, you need to define a `RunConfig` in the directory of `code/configs`

the customized config should be the instance of `RunConfig` in [code/core/run_config.py](https://github.com/david-liu/job_crawler/blob/dev/code/core/run_config.py).

For more information, please reference [code/configs/qiaobutang_top20.py](https://github.com/david-liu/job_crawler/blob/master/code/configs/qiaobutang_top20.py) and [code/configs/shixiseng.py](https://github.com/david-liu/job_crawler/blob/dev/code/configs/shixiseng.py)
