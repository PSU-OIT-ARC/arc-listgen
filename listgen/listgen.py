import os
import grp


def listfulldir(d):
    return [os.path.join(d, f) + '/' for f in os.listdir(path=d)]


def group_lookup(path):
    print(path)
    gid = os.stat(path).st_gid
    print(gid)
    group = grp.getgrgid(gid)
    return group

def get_resgroups(paths):
    return [group_lookup(path) for path in paths]

def members_lookup(path):
    members = grp.getgrgid(os.stat(path).st_gid).gr_mem

def get_members(paths):
    return [members_lookup for path in paths]

def www_lookup():
    print('hi')
    www_path = '/vol/www/'
    www_dirs = listfulldir(www_path)
    www_resgroups = get_resgroups(www_dirs)
    return "list of users"


groups = {
    'www': www_lookup(),
    'shares': 'this is the shares group',
}


def cli(group):
    grouplist = groups.get(group, 'invalid group name')
    print(grouplist)
