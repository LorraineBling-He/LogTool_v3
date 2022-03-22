import json
from idlelib import window

from django.shortcuts import render, HttpResponse
from django_webssh.tools.tools import unique
from LogTool_v3.settings import TMP_DIR

from django_pandas.io import read_frame

import os


def index(request):
    web_name = get_namelist()
    return render(request, 'index.html', {'list': web_name})

def upload_ssh_key(request):
    if request.method == 'POST':
        pkey = request.FILES.get('pkey')
        ssh_key = pkey.read().decode('utf-8')

        while True:
            filename = unique()
            ssh_key_path = os.path.join(TMP_DIR, filename)
            if not os.path.isfile(ssh_key_path):
                with open(ssh_key_path, 'w') as f:
                    f.write(ssh_key)
                break
            else:
                continue

        return HttpResponse(filename)

def get_namelist():
    from django_webssh import models
    name = models.Serverinfo.objects.values('name')
    # 将查出来的结果<QuerySet [{'name': 'ceshi'}, {'name': '包三-设计工具'}]>转化成列表
    web_name = []
    for i in range(len(name)):
        web_name.append(name[i]['name'])
    return web_name

def is_login(request):
    name=request.POST.get('name')
    if request.method == "POST":
        # 获取数据库中的name
        web_name = get_namelist()
        if name in web_name:
            return HttpResponse("1")
        return HttpResponse("0")
    return render(request,"")

def dele(request):
    from django_webssh import models
    name = request.POST.get('name')
    if request.method == "POST":
        models.Serverinfo.objects.filter(name=name).delete()
        return HttpResponse("1")
    else:
        return HttpResponse("0")
    return render(request, "")

def webssh(request):
    print(request.GET)
    return render(request,'webssh.html')