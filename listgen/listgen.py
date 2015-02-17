import os
import grp
import ldap3

# user_re = re.compile(r'(pdx){1}(\d{5}){1}$')

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


def user_looker_upper(path):
    dirs = listfulldir(path)
    resgroups = get_resgroups(dirs)
    members = get_members(resgroups)
    return members


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
    return resgroups - EXCLUDE


def get_members(resgroups):
    www_users = set()
    for resgroup in resgroups:
        members = ldap_lookup('(cn={})'.format(resgroup))[0]\
            .get('attributes').get('memberUid')
        if members:
            www_users = www_users | set(members)
    return www_users - EXCLUDE


GROUPS = {
    'www': '/vol/www',
    'share': '/vol/share',
}


def cli(group):
    path = GROUPS.get(group, 'invalid group name')
    print(user_looker_upper(path))
