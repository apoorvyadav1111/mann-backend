# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ActivityConfig(AppConfig):
    name = 'activity'

    def ready(self):
    	import activity.signals