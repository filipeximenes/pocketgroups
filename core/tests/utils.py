

def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to ``reverse()``
    """
    view.request = request
    if not hasattr(view.request, 'session'):
        view.request.session = {}
    view.args = args
    view.kwargs = kwargs
    return view
