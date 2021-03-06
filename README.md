# Hiking


Hiking is a job crawler crawling job information from a job website


Source code is made available under the [Apache 2.0 license](https://github.com/SeleniumHQ/selenium/blob/master/LICENSE).


## Installation

### Chrome

Hiking will use Chrome as the driver to crawl web pages, please make sure that Firefox has been installed in your computer.

```
brew install chromedriver
```

### PhantomJS

Hiking also can run without GUI (Firefox), which means it can crawling pages in headless browser mode.

In order to support this, you need to download webkit [PhantomJS](http://phantomjs.org/download.html), and extract it in your computer.

If you extact `PhantomJS` in the `~/phantomjs-2.1.1` directory, please run the command to check it is the right version.

```
~/phantomjs-2.1.1/bin/phantomjs -v
```

> Note: For Ubuntu Server, It however still relies on `Fontconfig` (the package fontconfig or `libfontconfig`, depending on the distribution), please use fellowing commands to install these dependecies


```
sudo apt-get update
sudo apt-get install fontconfig-config
sudo apt-get install fontconfig
```


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
mongoexport --db jobs_db --collection jobs --out jobs_161012.csv --type=csv --fields dummy,dummy,industry,company,location,deadline,dummy,dummy,dummy,job_name,url
```


### Install python environment

Now, we need to install the python environment and all dependent packages. And all steps to build the environment has been scripted in `install_env`.

So you can install environment just through running the script.
```sh
./install_env
```


## Run

You can run sample code [code/job_app.py](https://github.com/david-liu/hiking/blob/dev/code/job_app.py) to crawling the test job website.
```sh
code/job_app.py
```
and the crawling results will been printed in the console.

If you want to store the data in MongoDB's database, you can run the commond with `-o` and `-d` argument.
```sh
code/job_app.py -o mongodb -d jobs_db:jobs
```
and the results will save in the `jobs` collection of `jobs_db` database.


If you want to start the crawler in headless browser model, you can run the command with `--headless` argument to specify the location of the [PhantomJS](http://phantomjs.org/) webkit.
```sh
code/app.py --headless=[the location of the binary package of phantomjs]
```

Try with `-h` argument for more information.

```sh
code/app.py -h
```

## Extension

If you want to crawl another website or another part of a website, you need to define a `RunConfig` in the directory of `code/configs`

the customized config should be the instance of `RunConfig` in [code/hiking/core/run_config.py](https://github.com/david-liu/hiking/blob/dev/code/hiking/core/run_config.py).

For more information, please reference [code/run_configs/qiaobutang_top20.py](https://github.com/david-liu/hiking/blob/dev/code/run_configs/qiaobutang_top20.py) and [code/run_configs/shixiseng.py](https://github.com/david-liu/hiking/blob/dev/code/run_configs/shixiseng.py)

When you create the `RunConfig`, you need to create a new application to run the applcation with the  `RunConfig`, For more information, please reference [code/job_app.py](https://github.com/david-liu/hiking/blob/dev/code/job_app.py).
