import os
import grp
import re
import ldap3

SERVER = ldap3.Server('ldap-login.oit.pdx.edu', tls=None)
CONNECTION = ldap3.Connection(SERVER, auto_bind=True, lazy=True)
EXCLUDE = {'other', 'root', 'sys', 'operator'}  # Users to exclude

# Cli

GROUPS = {
    'www': '/vol/www',
    'share': '/vol/share',
    'compute': '/home',
}


def cli(group):
    """This is the cli function"""
    path = GROUPS.get(group, None)
    if path:
        print(users_in_group(path))
    else:
        print('invalid group name')

# Primary Functions


def users_in_group(path):
    """Returns a set of users of all the folders in the path"""
    dirs = listfulldir(path)
    resgroups = get_resgroups(dirs)
    members = get_members(resgroups)
    filtered = filter_pdx_users(members)
    #           user_re = re.compile(r'(pdx){1}(\d{5}){1}$')
    # eduPersonAffiliation: SYSTEM/SERVICE
    # mailRoutingAddress: bcomnes@pdx.edu
    print('Skipped: ')
    print(members - filtered)
    return filtered


def add_to_group(users):
    # TODO:  Figure out how to add users to groups
    # https://developers.google.com/admin-sdk/directory/v1/guides/manage-group-members
    return

    # Speacalty Functions


def group_lookup(path):
    """look up the gid, skipping the weird errors"""
    try:
        stat = os.stat(path)
        gid = stat.st_gid
        #print(stat.st_atime, stat.st_mtime, stat.st_ctime)
    except FileNotFoundError:
        return
    try:
        group = grp.getgrgid(gid).gr_name
    except KeyError:
        return
    return group


def get_resgroups(paths):
    """apply group_lookup to all the dirs in path"""
    resgroups = {group_lookup(path) for path in paths if group_lookup(path)}
    return resgroups - EXCLUDE


def get_members(resgroups):
    """queries ldap with resgroup names and get a set of all users"""
    users = set()
    for resgroup in resgroups:
        members = ldap_lookup('(cn={})'.format(resgroup))[0]\
            .get('attributes').get('memberUid')
        # Note, this can also be acheived with just grp
        # see grp.getgrgid(gid).gr_mem @ aa4dc12
        if members:
            users = users | set(members)
    return users

def filter_pdx_users(users):
    """Cleans up the user listing in our highly specific way"""
    pdx = re.compile(r'^pdx\d{5}$') # Match pdx00000 users
    clean = {user for user in users - EXCLUDE if (not pdx.match(user))\
        and ldap_check(user)}
    return clean

def filter_system_service(uid):
    return
    # (NOT IMPLEMENTED) Filter eduPersonAffiliation: SYSTEM or 
    # eduPersonAffiliation: SERVICE from LDAP


def ldap_check(uid):
    """
    Makes sure all users have a mail mailRoutingAddress.  This seems to clean
    up duplicate mail aliases.
    """
    #print(uid)
    try:
        results = ldap_lookup('(uid={})'.format(uid))[0]
        email = results.get('attributes').get('mailRoutingAddress')
        affiliation = set(results.get('attributes').get('eduPersonAffiliation'))
        if 'SYSTEM' in affiliation or 'SERVICE' in affiliation:
            # Skip system and service accounts
            return
        # only return if there is a mail routing address
        return email
    except IndexError:
        # When the name does not have a complete ldap entry
        #print('uid={} has no ldap entry'.format(uid))
        return

# Utility Functions


def ldap_lookup(query):
    """Query ldap and return the results"""
    with CONNECTION:
        result = CONNECTION.search(
            attributes=ldap3.ALL_ATTRIBUTES,
            search_base="dc=pdx,dc=edu",
            search_filter=query,
            search_scope=ldap3.SEARCH_SCOPE_WHOLE_SUBTREE,
        )
    if result:
        return CONNECTION.response
    return []


def listfulldir(d):
    """Special directory lister that makes the nfs jump"""
    return [os.path.join(d, f) + '/' for f in os.listdir(path=d)]
