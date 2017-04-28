"""
Router classes 
see: http://www.django-rest-framework.org/api-guide/routers/
"""
from django.conf.urls import url
from rest_framework.routers import SimpleRouter


class PermissionsRouter(SimpleRouter):
    """
    Custom router which may override the permission_classes of the views 
    """

    def __init__(self, trailing_slash=True, default_permissions=None):
        """Initialize PermissionsRouter"""
        if default_permissions is not None and not isinstance(
                default_permissions, tuple):
            raise TypeError('default_permissions must be a tuple or None')
        self.default_permissions = default_permissions
        super(PermissionsRouter, self).__init__(trailing_slash=trailing_slash)

    def register(self, prefix, viewset, base_name=None, permissions=None):
        """Register a new route with the registry"""
        if permissions is not None and not isinstance(permissions, tuple):
            raise TypeError('erpmissions must be a tuple or None')
        if base_name is None:
            base_name = self.get_default_base_name(viewset)
        self.registry.append((prefix, viewset, base_name, permissions))

    def get_urls(self):
        """
        Use the registered viewsets to generate a list of URL patterns.
        """
        ret = []

        for prefix, viewset, basename, permissions in self.registry:
            lookup = self.get_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:

                # Only actions which actually exist on the viewset will be bound
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                # Build the url pattern
                regex = route.url.format(
                    prefix=prefix,
                    lookup=lookup,
                    trailing_slash=self.trailing_slash
                )

                # If there is no prefix, the first part of the url is probably
                #   controlled by project's urls.py and the router is in an app,
                #   so a slash in the beginning will (A) cause Django to give
                #   warnings and (B) generate URLS that will require using '//'.
                if not prefix and regex[:2] == '^/':
                    regex = '^' + regex[2:]

                if self.default_permissions:
                    permissions = self.default_permissions

                route.initkwargs['permission_classes'] = permissions
                view = viewset.as_view(mapping, **route.initkwargs)
                name = route.name.format(basename=basename)
                route_url = url(regex, view, name=name)
                ret.append(route_url)

        return ret
