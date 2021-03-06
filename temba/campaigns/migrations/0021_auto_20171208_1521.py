# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 15:21
from __future__ import unicode_literals

import six
from temba.utils.languages import iso6392_to_iso6393
from django.db import migrations


def migrate_event_languages(apps, schema_editor):
    from temba.campaigns.models import CampaignEvent

    events = CampaignEvent.objects.filter(event_type='M', is_active=True).select_related('campaign__org')
    total = len(events)
    for idx, event in enumerate(CampaignEvent.objects.filter(event_type='M', is_active=True).select_related('campaign__org')):
        messages = {}
        for lang, message in six.iteritems(event.message):
            if lang != 'base':
                new_lang = iso6392_to_iso6393(lang, country_code=event.campaign.org.get_country_code())
                messages[new_lang] = message
            else:
                messages[lang] = message

        if idx % 1000 == 0:
            print("On event %d of %d" % (idx, total))

        event.message = messages
        event.save(update_fields=('message',))


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0020_auto_20171030_1637'),
    ]

    operations = [
        migrations.RunPython(migrate_event_languages)
    ]
