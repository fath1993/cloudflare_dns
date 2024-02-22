import threading
import time
import requests

from cloudflare_dns.settings import CLOUD_FLARE_TOKEN
from dns_changer.models import get_settings


def dns_changer(setting_object):
    headers = {
        'Authorization': f'Bearer {CLOUD_FLARE_TOKEN}',
        'Content-Type': 'application/json',
    }
    while True:
        setting = get_settings(setting_object.id)
        if not setting:
            return
        url = f'https://api.cloudflare.com/client/v4/zones/{setting.zone.zone_id}/dns_records/{setting.record_id}'

        ip_list_from_settings = setting.ip_list
        ip_list = ip_list_from_settings.replace(' ', '').replace('-', ',').replace('/', ',').split(',')

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
                setting.current_ip = ip
                setting.log = response.json()
                setting.save()
            except Exception as e:
                setting.current_ip = 'not changed'
                setting.log = str(e)
                setting.save()
            time.sleep(setting.sleep_time)
        time.sleep(setting.sleep_time)


class DNSChangerThread(threading.Thread):
    def __init__(self, name, setting_object):
        super().__init__()
        self._name = name
        self.setting_object = setting_object

    def run(self):
        dns_changer(self.setting_object)



