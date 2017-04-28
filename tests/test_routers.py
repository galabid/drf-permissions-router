"""

"""
from collections import namedtuple

from django.db import models
from django.test import TestCase
from rest_framework import permissions
from rest_framework.viewsets import ViewSet

from drf_permissions_router.routers import PermissionsRouter


class Permission(permissions.BasePermission):

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False

QS = namedtuple('Queryset', ['model'])


class AModel(models.Model):
    name = models.CharField(max_length=255)


class AViewSet(ViewSet):
    model = AModel
    queryset = QS(AModel)


class TestPermissionRouter(TestCase):

    def setUp(self):
        self.router = PermissionsRouter(default_permissions=(Permission, ))
        self.router.register('a', AViewSet)
        self.router.register('b', AViewSet, permissions=(Permission, ))

    def test_permission(self):
        urls = self.router.urls
