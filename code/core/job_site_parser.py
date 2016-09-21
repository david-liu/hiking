import abc

class JobSiteParser(object):

    def __init__(self, url):
        self._url = url

    @property
    def site_url(self):
        return self._url

    @property
    def list_detail_page_urls_fn(self):
        return self._list_detail_page_urls

    @property
    def field_css_selectors(self):
        return self._get_field_css_selectors()

    @property
    def field_element_processors(self):
        return self._get_field_element_processors()

    @abc.abstractproperty
    def _list_detail_page_urls(self, browser):
        """Method that retrive all details page urls .

        Expected to be overriden by sub-classes that require custom support.

        Args:
          browser: the 'Browser' objects.

        Returns:
          The list of all urls
        """
        pass

    @abc.abstractproperty
    def _get_field_css_selectors(self):
        """Method that get a dictionary of field to its css selector in web page.

        Expected to be overriden by sub-classes that require custom support.

        Args:
          browser: the 'Browser' objects.

        Returns:
          The dict of field to css selector
        """
        pass
        pass        

    def _get_field_element_processors(self):
        return None

