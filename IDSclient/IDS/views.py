from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
import datetime

'''
return list of logs in IDS/logs.html
'''
@login_required
def index(request):
    log_list = list(Log.objects.all())
    if log_list:
        context = {'log_list': log_list, 'last_id': log_list[-1].id}
    else:
        context = {'log_list': log_list, 'last_id': 0}
        
    return render(request, 'IDS/logs.html', context)

'''
return json of last minute logs and danger lvl
'''
def upd_logs(request):
    last_log_id = request.GET.get('last_log_id', None)

    log_list = Log.objects.filter(id__gt = int(last_log_id))
    log_list_to_resp = list()
    for log in log_list:
        log_list_to_resp.append(model_to_dict(log))

    current_time = datetime.datetime.now()
    last_logs = Log.objects.filter(timestamp__gt = current_time - datetime.timedelta(minutes=1))
    danger_sum = 0
    for log in last_logs:
        danger_sum += log.danger
    
    return JsonResponse([log_list_to_resp, danger_sum, str(current_time.time())[0:8]], safe = False)