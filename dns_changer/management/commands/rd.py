import os
import time

import requests
from django.core.management import BaseCommand

from dns_changer.models import get_settings, DNSSetting


class Command(BaseCommand):
    def handle(self, *args, **options):
        dns_changer()


def record_id():
    headers = {
        'Authorization': "Bearer wiah4IS62c-W_WR_6ZsDuQ_wvfHkvQiVB9cmcfaD",
        'Content-Type': 'application/json',
    }
    zone_id = '379bae18defd6f5d6dda71270426bd3c'

    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

    try:
        response = requests.get(url, headers=headers)
        print(response.json())
    except Exception as e:
        print(str(e))


def record_change_check():
    headers = {
        'Authorization': "Bearer wiah4IS62c-W_WR_6ZsDuQ_wvfHkvQiVB9cmcfaD",
        'Content-Type': 'application/json',
    }
    zone_id = '379bae18defd6f5d6dda71270426bd3c'
    record_id = 'e16df8b60a249722e9150195cd06d7d5'
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'

    try:
        response = requests.get(url, headers=headers)
        print(response.json())
    except Exception as e:
        print(str(e))


def dns_changer():
    setting_object = DNSSetting.objects.filter().latest('id')
    headers = {
        'Authorization': 'Bearer wiah4IS62c-W_WR_6ZsDuQ_wvfHkvQiVB9cmcfaD',
        'Content-Type': 'application/json',
    }
    while True:
        setting = get_settings(setting_object.id)
        if not setting:
            return
        url = f'https://api.cloudflare.com/client/v4/zones/{setting.zone.zone_id}/dns_records/{setting.record_id}'

        ip_list_from_settings = setting.ip_list
        ip_list = ip_list_from_settings.replace('    ', '').replace('   ', '').replace('  ', '').replace(' ', '').replace('-', ',').replace('/', ',').split(
            ',')

        for ip in ip_list:
            setting = get_settings(setting_object.id)
            if not setting:
                return
            if setting.ip_list != ip_list_from_settings:
                break
            data = {
                'type': setting.dns_record_type,
                'proxied': setting.dns_proxied,
                'name': setting.dns_name,
                'content': ip,
            }
            try:
                response = requests.put(url, headers=headers, json=data)
                print(response.json())
                setting.current_ip = ip
                setting.log = response.json()
                setting.save()
            except Exception as e:
                print(str(e))
                setting.current_ip = 'not changed'
                setting.log = str(e)
                setting.save()
            print(f'now waiting for {setting.sleep_time} seconds')
            time.sleep(setting.sleep_time)
        print(f'now waiting for {setting.sleep_time} seconds')
        time.sleep(setting.sleep_time)