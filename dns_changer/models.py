import requests
from django.db import models

from cloudflare_dns.settings import CLOUD_FLARE_TOKEN

DNS_RECORD_TYPE = (('A', 'A'), ('NS', 'NS'), ('MX', 'MX'), ('CNAME', 'CNAME'))


class Zone(models.Model):
    zone_id = models.CharField(max_length=255, null=False, blank=False, verbose_name='domain zone id')
    data = models.TextField(null=True, blank=True, editable=False, verbose_name='داده ها')

    def __str__(self):
        return f'zone_id: {self.zone_id}'

    class Meta:
        verbose_name = 'زون'
        verbose_name_plural = 'زون ها'

    def save(self, *args, **kwargs):
        headers = {
            'Authorization': f"Bearer {CLOUD_FLARE_TOKEN}",
            'Content-Type': 'application/json',
        }
        zone_id = f'{self.zone_id}'

        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

        try:
            response = requests.get(url, headers=headers)
            self.data = response.json()
        except Exception as e:
            self.data = str(e)
        super().save(*args, **kwargs)


class DNSSetting(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=False, blank=False, verbose_name='zone')
    record_id = models.CharField(max_length=255, null=False, blank=False, verbose_name='record id')
    dns_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='dns name', help_text='sample: app.dnsforyou.xyz')
    dns_record_type = models.CharField(max_length=255, choices=DNS_RECORD_TYPE, null=False, blank=False, verbose_name='dns record type')
    dns_proxied = models.BooleanField(default=False, verbose_name='proxied')
    current_ip = models.CharField(max_length=255, null=False, blank=False, verbose_name='current ip')
    ip_list = models.TextField(null=False, blank=False, verbose_name='لیست ایپی ها', help_text='sample: 0.0.0.0,1.1.1.1,...')
    sleep_time = models.PositiveIntegerField(default=60, null=False, blank=False, verbose_name='زمان انتظار')
    log = models.TextField(null=True, blank=True, editable=False, verbose_name='لاگ')

    def __str__(self):
        return f'zone_id: {self.zone.zone_id} | record_id: {self.record_id}'

    class Meta:
        unique_together = ('zone', 'record_id')
        verbose_name = 'تنظیم dns'
        verbose_name_plural = 'تنظیم dns ها'


def get_settings(setting_id):
    try:
        setting = DNSSetting.objects.get(id=setting_id)
        return setting
    except:
        return False
