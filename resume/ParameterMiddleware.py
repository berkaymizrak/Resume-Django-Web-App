from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse


class ParameterMiddleware(MiddlewareMixin):
    """
    ParameterMiddleware is set to receive people who come with reference of other users with get parameter of 'ref'
    and saves it into the session. Thus, if user visit other pages of website, all get parameters and 'ref' will stay
    end of the url all the time, on all different links.

    For example:
    1. User comes from:
        https://berkaymizrak.com/?ref=example_user&page=5
    2. User goes to about and then register pages by clicking buttons on page and get parameters stay as they are:
            https://berkaymizrak.com/about/?ref=example_user&page=5
            https://berkaymizrak.com/register/?ref=example_user&page=5

    You can just make it for only 'ref' parameter also:
        https://berkaymizrak.com/?ref=example_user&page=5
        >>
        https://berkaymizrak.com/about/?ref=example_user
        https://berkaymizrak.com/register/?ref=example_user
    """

    def save_ref_to_session(self, request, key='ref'):
        # 'ref' reads from session
        get_ref_from_session = request.session.get(key, None)
        get_ref_from_link = request.GET.get(key, None)

        if get_ref_from_link:
            if get_ref_from_session != get_ref_from_link:
                # if url has 'ref' and the 'ref' not saved in session, then save it to session
                request.session[key] = get_ref_from_link
            # Return None to not get infinite loop.
            return None
        else:
            return get_ref_from_session

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Gets all parameters from url. This is optional, you can remove here if you want to keep only 'ref' or
        # selected any parameter.
        parameters = request.GET.urlencode()
        if parameters:
            parameters = '&' + str(parameters)
        # __All parameters optional until here.__


        get_ref = self.save_ref_to_session(request)

        # Checks;
        #   get_ref: if 'ref' exist in url, save it to session and return None; if 'ref' exist in session but not in url,
        #   then redirect to url with parameter.
        #   not request.user.is_authenticated: runs only for not authenticated users.
        return get_ref and not request.user.is_authenticated and redirect(reverse(view_func) + '?ref=' + get_ref + parameters)
        # if you want to make without all parameters, only for selected parameters:
        # return get_ref and not request.user.is_authenticated and redirect(reverse(view_func) + '?ref=' + get_ref)

