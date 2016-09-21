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

you can run code `code/service.py` to crawling the test job website.

```sh
python code/service.py
```

add the crawling results will been stored in the `job` collection of database 'jobs_db'

## Extension

If you want to crawl another website or another part of a website, you need to implement a `Parser` in the directory of `code\parsers`

the customized Parser need to been the subclass of `JobSiteParser` and override two abstract metheds.

* `def _get_field_css_selectors(self)` 

Define a dictionary of field name to css selector in the job details page

* `def _list_detail_page_urls(self, browser)`

Parse the specified page, and collect all job details page's url


