import subprocess
import threading

from django.contrib import admin, messages

from dns_changer.models import DNSSetting, Zone
from dns_changer.tasks import DNSChangerThread


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        'zone_id',
    )

    readonly_fields = (
        'data',
    )

    fields = (
        'zone_id',
        'data',
    )


@admin.register(DNSSetting)
class DNSSettingAdmin(admin.ModelAdmin):
    list_display = (
        'dns_name',
        'current_ip',
        'ip_list',
        'sleep_time',
    )

    readonly_fields = (
        'current_ip',
        'log',
    )

    fields = (
        'zone',
        'record_id',
        'dns_name',
        'dns_record_type',
        'dns_proxied',
        'ip_list',
        'sleep_time',

        'current_ip',
        'log',
    )

    @admin.action(description='اجرای تغییر اتوماتیک dns')
    def auto_dns_changer(self, request, queryset):
        messages.info(request, f'عملیات آغاز شد')
        active_threads = threading.enumerate()
        threads_name_list = []
        for thread in active_threads:
            if thread.is_alive():
                threads_name_list.append(str(thread.name))
        for item in queryset:
            if not f'{item.id}-{item.zone_id}-{item.record_id}' in threads_name_list:
                DNSChangerThread(name=f'{item.id}-{item.zone_id}-{item.record_id}', setting_object=item).start()

    @admin.action(description='لغو عملیات')
    def auto_dns_reset(self, request, queryset):
        RestartGunicornThread().start()
        messages.error(request, f'عملیات لغو شد')

    actions = (auto_dns_changer, auto_dns_reset)


class RestartGunicornThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        subprocess.run(['sudo', 'systemctl', 'restart', 'gunicorn'], check=False)