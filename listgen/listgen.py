import os
import grp
import ldap3

#user_re = re.compile(r'(pdx){1}(\d{5}){1}$')

SERVER = ldap3.Server('ldap-login.oit.pdx.edu', tls=None)
CONNETION = ldap3.Connection(SERVER, auto_bind=True, lazy=True)


def ldap_lookup(query):
    with CONNETION:
        result = CONNETION.search(
            attributes=ldap3.ALL_ATTRIBUTES,
            search_base="dc=pdx,dc=edu",
            search_filter=query,
            search_scope=ldap3.SEARCH_SCOPE_WHOLE_SUBTREE,
        )
    if result:
        return CONNETION.response
    return []


def listfulldir(d):
    return [os.path.join(d, f) + '/' for f in os.listdir(path=d)]

EXCLUDE = {'other', 'root', 'sys', 'operator'}


def www_lookup():
    www_path = '/vol/www/'
    www_dirs = listfulldir(www_path)
    www_resgroups = get_resgroups(www_dirs)
    return get_members(www_resgroups)


def group_lookup(path):
    try:
        gid = os.stat(path).st_gid
    except FileNotFoundError:
        return
    group = grp.getgrgid(gid).gr_name
    return group


def get_resgroups(paths):
    exclude = {'other', 'root'}
    resgroups = {group_lookup(path) for path in paths if group_lookup(path)}
    return resgroups - exclude


def get_members(resgroups):
    www_users = set()
    for resgroup in resgroups:
        members = ldap_lookup('(cn={})'.format(resgroup))[0]\
            .get('attributes').get('memberUid')
        if members:
            www_users = www_users | set(members)
    return www_users - EXCLUDE


def www_grplookup():
    www_path = '/vol/www/'
    www_dirs = listfulldir(www_path)
    return get_grpmembers(www_dirs)


def grpmembers_lookup(path):
    try:
        gid = os.stat(path).st_gid
    except FileNotFoundError:
        return
    return grp.getgrgid(gid).gr_mem


def get_grpmembers(paths):
    www_users = set()
    for path in paths:
        members = grpmembers_lookup(path)
        if members:
            www_users = www_users | set(members)
    return www_users - EXCLUDE


def compare():
    return www_lookup() - www_grplookup()

GROUPS = {
    'www': www_lookup,
    'wwwgrp': www_grplookup,
    'compare': compare,
    'shares': 'this is the shares group',
}


def cli(group):
    grouplist = GROUPS.get(group, 'invalid group name')
    print(grouplist())
