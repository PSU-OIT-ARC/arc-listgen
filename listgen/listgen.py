import os
import grp


def listfulldir(d):
    return [os.path.join(d, f) for f in os.listdir(path=d)]


def group_lookup(path):
    group = grp.getgrgid(os.stat(path).st_gid)
    return group


def get_resgroups(paths):
    return [group_lookup for path in paths]


def www_lookup():
    www_path = '/vol/www/'
    www_dirs = os.listdir(www_path)
    www_resgroups = get_resgroups(www_dirs)
    return www_resgroups


groups = {
    'www': www_lookup(),
    'shares': 'this is the shares group',
}


def cli(group):
    grouplist = groups.get(group, 'invalid group name')
    print(grouplist)
