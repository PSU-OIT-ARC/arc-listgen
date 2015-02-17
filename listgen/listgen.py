import os
import grp
import ldap3

# Cli

GROUPS = {
    'www': '/vol/www',
    'share': '/vol/share',
}


def cli(group):
    """This is the cli function"""
    path = GROUPS.get(group, 'invalid group name')
    print(user_looker_upper(path))

# Primary Functions


def user_looker_upper(path):
    """Returns a set of users of all the folders in the path"""
    dirs = listfulldir(path)
    resgroups = get_resgroups(dirs)
    members = get_members(resgroups)
    # TODO: Filter inactive users... if they are there.
    # TODO: Decide what to do about pdxXXXXX users
    #           user_re = re.compile(r'(pdx){1}(\d{5}){1}$')
    return members


def add_to_group(users):
    # TODO:  Figure out how to add users to groups
    # https://developers.google.com/admin-sdk/directory/v1/guides/manage-group-members
    return

    # Speacalty Functions


def group_lookup(path):
    """look up the gid, skipping the weird errors"""
    try:
        gid = os.stat(path).st_gid
    except FileNotFoundError:
        return
    group = grp.getgrgid(gid).gr_name
    return group


def get_resgroups(paths):
    """apply group_lookup to all the dirs in path"""
    resgroups = {group_lookup(path) for path in paths if group_lookup(path)}
    return resgroups - EXCLUDE


def get_members(resgroups):
    """queries ldap with resgroup names and get a set of all users"""
    www_users = set()
    for resgroup in resgroups:
        members = ldap_lookup('(cn={})'.format(resgroup))[0]\
            .get('attributes').get('memberUid')
        # Note, this can also be acheived with just grp
        # see grp.getgrgid(gid).gr_mem @ aa4dc12
        if members:
            www_users = www_users | set(members)
    return www_users - EXCLUDE

# Utility Functions

SERVER = ldap3.Server('ldap-login.oit.pdx.edu', tls=None)
CONNETION = ldap3.Connection(SERVER, auto_bind=True, lazy=True)


def ldap_lookup(query):
    """Query ldap and return the results"""
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
    """Special directory lister that makes the nfs jump"""
    return [os.path.join(d, f) + '/' for f in os.listdir(path=d)]

EXCLUDE = {'other', 'root', 'sys', 'operator'}
