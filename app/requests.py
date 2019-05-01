
import urllib.request,json

from .models import Quote


base_url=  "http://quotes.stormconsultancy.co.uk/random.json"


def get_quote():
    """
    function to get json responce to our url request
    """
    get_quote_url = base_url

    with urllib.request.urlopen(get_quote_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)
        print(get_quote_response)
        quote_results = None

        if get_quote_response:
            quote_results = get_quote_response

            

return quote_results