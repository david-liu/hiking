"""Run Config."""


class RunConfig(object):
  """This class specifies the specific configurations for the job crawler."""

  def __init__(self,
               site_url,
               field_css_selectors,
               list_detail_page_urls_fn,
               field_element_processors=None):
    """Constructor.

    Args:
      site_url: The url of website master. Empty string (the default) for local.
      field_css_selectors: A dictionary of a job field to its css selector in the page
      field_element_processors: A element processor list to get the filed value from a dom element. 
      The processor 
      list_detail_page_urls_fn: A functon to aggregate all details page url from the site url.
    """

    self.site_url = site_url
    self.field_css_selectors = field_css_selectors
    self.list_detail_page_urls_fn = list_detail_page_urls_fn
    self.field_element_processors = {} if field_element_processors is None else field_element_processors
