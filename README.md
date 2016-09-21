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
python code/service.py
```

add the crawling results will been stored in MongoDB's database `jobs_db`, and the collection name is `job`

## Extension

If you want to crawl another website or another part of a website, you need to implement a `Parser` in the directory of `code\parsers`

the customized Parser should be the subclass of `JobSiteParser` in [code/core/job_site_parser.py](https://github.com/david-liu/job_crawler/blob/master/code/core/job_site_parser.py)  and implement two abstract metheds.

* `def _get_field_css_selectors(self)` : Define a dictionary of field name to css selector in the job details page

* `def _list_detail_page_urls(self, browser)`: Crawling the leading page, and collect all job details page's url


For more information, please reference [code/parsers/qiaobutang.py](https://github.com/david-liu/job_crawler/blob/master/code/parsers/qiaobutang.py) and [code/parsers/shixiseng.py](https://github.com/david-liu/job_crawler/blob/master/code/parsers/shixiseng.py)

