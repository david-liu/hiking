from furl import furl

def build_url(base_url, queries):
	return furl(base_url).add(queries).url