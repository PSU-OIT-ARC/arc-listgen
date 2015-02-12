import os
import grp
import re

user_re = re.compile(r'(pdx){1}(\d{5}){1}$')


def listfulldir(directory):
    return [os.path.join(directory, f) + '/' for f in os.listdir(path=directory)]


def group_lookup(path):
    try:
        gid = os.stat(path).st_gid
    except FileNotFoundError:
        print('skipping ' + path)
        return
    group = grp.getgrgid(gid).gr_name
    return group

def get_resgroups(paths):
    exclude = {'other', 'root'}
    resgroups = {group_lookup(path) for path in paths if group_lookup(path)}
    return resgroups - exclude

def members_lookup(path):
    try:
        gid = os.stat(path).st_gid
    except FileNotFoundError:
        print('skipping ' + path)
        return
    return grp.getgrgid(gid).gr_mem

def get_members(paths):
    exclude = {'other', 'root'}
    www_users = set()
    for path in paths:
        members = members_lookup(path)
        if members:
            print('helloworld')
            print(members)
            www_users = www_users | members
    print(www_users)
    return
    #flat_www_users = filter(lambda x:x, list(www_users))
    # www_users = [members_lookup(path) for path in paths if members_lookup(path)]
    # print(www_users)
    # flat_www_users = {user for members in www_users for user in members}

def www_lookup():
    www_path = '/vol/www/'
    www_dirs = listfulldir(www_path)
    www_resgroups = get_resgroups(www_dirs)
    print(www_resgroups)
    get_members(www_dirs)
    return

def www_grplookup():
    return 'hello world'

GROUPS = {
    'www': www_lookup(),
    'wwwgrp': www_grplookup(),
    'shares': 'this is the shares group',
}


def cli(group):
    grouplist = GROUPS.get(group, 'invalid group name')
    print(grouplist)
