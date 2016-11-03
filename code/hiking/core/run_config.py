
class ByKeys(object):

    """Standard names for a selector type to locate a element.

    The following standard keys are defined:

    * `ID`:  find an element with the id attribute
    * `NAME`: Use this when you know name attribute of an element. With this strategy, the first element with the name attribute value matching the location will be returned
    * `CSS_SELECTOR`: locate ellement with css selector.
    * `CLASS_NAME`: locate ellement with class name
    * `X_PATH`: locate ellement with xPath
    """

    ID = 'id'
    NAME = 'name'
    CSS_SELECTOR = 'cssSelector'
    CLASS_NAME = 'className'
    X_PATH = 'XPath'

    @classmethod
    def values(cls):
        return [cls.ID, cls.NAME, cls.CSS_SELECTOR, cls.CLASS_NAME, cls.X_PATH]


class FieldTypeKeys(object):

    """Standard names for field type.

    The following standard keys are defined:

    * `STRING`: string type.
    * `INTEGER`: int type.
      * `DATE`: date type.
    """

    STRING = 'string'
    INT = 'int'
    DATE = 'date'

    @classmethod
    def values(cls):
        return [cls.STRING, cls.INT, cls.DATE]


class FieldMultiplicityKeys(object):

    """Standard names for filed mutiplicatity.

    The following standard keys are defined:

    * `ONE`: training mode.
    * `MANY`: evaluation mode.
    """

    ONE = '1'
    MANY = '*'

    @classmethod
    def values(cls):
        return [cls.ONE, cls.MANY]


class ElementSelector(object):

    """ This class define element selector in the page

    """

    def __init__(self,
                 key,
                 by=ByKeys.CSS_SELECTOR,
                 is_primary=False,
                 multi=FieldMultiplicityKeys.ONE,
                 value_type=FieldTypeKeys.STRING):
        """ 
        Constructor:
        Args:
            key: the selector key
            by: selector type to locate a element
            is_primary: whether the field is primary value for data insert or update
            multi: whether the field has one or muti valuse
            value_type: the type of the field value
        """

        self.key = key
        self.by = by
        self.multi = multi
        self.is_primary=is_primary
        self.value_type = value_type


def is_allowed_enumu_value(enumu_cls, value):
    if value not in enumu_cls.values():
        print "% is not a valid value for %s"
    return value


class RunConfig(object):

    """This class specifies the specific configurations for the job crawler."""

    def __init__(self,
                 site_url,
                 field_selectors,
                 list_detail_page_urls_fn,
                 block_selector="body",
                 in_page_jumping_fn=None,
                 field_element_processors=None):
        """Constructor.

        Args:
            site_url: The url of website master. Empty string (the default) for local.
            field_selectors: A dictionary of a job field to its selector in the page.
                The field_selector can be [field name] -> [css selector keys] or [field name] -> [a dictionary with ElementSelector properties], for example:

                {
                'first_name': '#fist_name',
                'first_name': '#lass_name',
                'tags' : {
                    'key' : 'person_tags',
                    'by': ByKeys.ID,
                    'multi' : FieldMultiplicityKeys.MANY,
                    'value_type': FieldTypeKeys.STRING
                    }
                }

            field_element_processors: A element processor list to get the filed value from a dom element. 
            The processor 
            list_detail_page_urls_fn: A functon to aggregate all details page url from the site url.
        """

        self.site_url = site_url
        self.field_selectors = self._convert_to_element_selectors(
            field_selectors)
        self.list_detail_page_urls_fn = list_detail_page_urls_fn
        self.block_selector = block_selector
        self.in_page_jumping_fn = in_page_jumping_fn
        self.field_element_processors = {
        } if field_element_processors is None else field_element_processors

        self.primary_fields = self._get_primary_fields()

    def _get_primary_fields(self):
        primary_fields = []
        for field_name, selector in self.field_selectors.items():
            if selector.is_primary:
                primary_fields.append(field_name)

        return primary_fields if len(primary_fields) > 0 else None

    def _convert_to_element_selectors(self, element_selectors):
        """
        convert a element selectors defined in a ditionary to ElementSelector
        """

        selectors = {}
        for field_name, value in element_selectors.items():
            if field_name in selectors.keys():
                raise ValueError(
                    'The paramter [%s] has been defined' % field_name)

            if isinstance(value, basestring):
                selector = ElementSelector(value)

                selectors[field_name] = selector
            elif isinstance(value, dict):
                by = ByKeys.CSS_SELECTOR
                multi = FieldMultiplicityKeys.ONE
                value_type = FieldTypeKeys.STRING
                is_primary = False

                if 'key' not in value:
                    raise ValueError(
                        'The [key] is a required configration parameter')

                selector_key = value['key']

                if not selector_key:
                    return None

                if 'by' in value and is_allowed_enumu_value(ByKeys, value['by']):
                    by = value['by']
                if 'multi' in value and is_allowed_enumu_value(FieldMultiplicityKeys, value['multi']):
                    multi = value['multi']
                if 'value_type' in value and is_allowed_enumu_value(FieldTypeKeys, value['value_type']):
                    value_type = value['value_type']

                if 'is_primary' in value :
                    is_primary = value['is_primary']

                selector = ElementSelector(key=selector_key,
                                           by=by,
                                           is_primary=is_primary,
                                           multi=multi,
                                           value_type=value_type)

                selectors[field_name] = selector

            else:
                raise ValueError(
                    'The element selector should be a string or a dictionary')

        return selectors
