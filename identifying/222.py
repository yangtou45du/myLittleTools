#!/usr/bin/env python
# -*- coding: cp936 -*-
from os.path import dirname, abspath
import os
import re
from datetime import datetime
from fabric.api import *

'''
��������:
lcd(dir): ���뱾��ĳĿ¼
local(cmd): ������ִ������
cd(dir): ���������ĳĿ¼
run(cmd):��������ִ������
'''
# �������б�
#env.hosts = ['user@server1','user2@server2']


BASE_DIR = dirname(abspath(__file__))


def compress():
    datetime_json_name = datetime.now().strftime('%Y%m%d_%H%M%S.json')
    reg = re.compile(r'''COMPRESS_OFFLINE_MANIFEST ?= ?(?:'|").+?(?:'|")''')

    with lcd(BASE_DIR):
        with open(os.path.join(BASE_DIR, 'zqxt', 'settings.py'), 'r+') as f:
            content = f.read()
            content = reg.sub(
                r'COMPRESS_OFFLINE_MANIFEST = "%s"' % datetime_json_name,
                content)
            f.seek(0)
            f.truncate()
            f.write(content)

        local('python manage.py compress --force')


def push_only():
    with lcd(BASE_DIR):
        local('git push')


def push():
    compress()
    with lcd(BASE_DIR):
        local('git add -A')
        local('git status')
        local('git commit -m "%s"' % raw_input('input commit reason:'))
        local('git push')