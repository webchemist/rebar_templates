#!/usr/bin/env python

# Dummy generator of the sync config
# Should be added as a post-compile hook into the make file
import os
import re
import shutil

FILENAME = "sync.config"
TPL = """
[
    {sync, [
        {growl, %(growl)s},
        {log, %(log)s},
        {non_descendants, fix},
        {executable, auto},
        {excluded_modules, [%(excluded_modules)s]}
    ]}
].
"""
# settings
EXCLUDED_APPS = ["cowboy", "cowlib", "ranch", "emysql", "lager", "goldrush", \
                 "sync", "emysql"]
LOG = "all"
GROWL = "all"

modre = re.compile("modules,\[(.*?)\]")

def _expand_app(app_name, app_path):
    app_file = os.path.join(app_path, "ebin/%s.app"%app_name)
    assert os.path.exists(app_file)
    content = ""
    with open(app_file, "r") as f:
        content = re.sub("\s{1,}", "", re.sub("\n","", f.read()))
        modules = modre.findall(content)[0]
        return modules
    raise Exception("Some thing goes wrong :(")


def modules4apps(apps_list):
    
    search_paths = [os.path.abspath(x) for x in ["deps", "apps"]]
    existed_apps = []
    for root in search_paths:
        for app_name in apps_list:
            app_path = os.path.join(root, app_name)
            if os.path.isdir(app_path):
                existed_apps.append((app_name, app_path))
    modules = []
    for app_spec in existed_apps:
        try:
            modules.append(_expand_app(*app_spec))
        except Exception, e:
            print e
    return (", ".join(modules)).strip(",")

def build_config(excluded_modules):
    return TPL % {
        'growl': GROWL,
        'log': LOG,
        'excluded_modules': excluded_modules
    }

def write_config(filename, force=False):
    if os.path.isfile(filename) and not force:
        shutil.copyfile(filename, filename + ".old")
    with open(filename, "w") as f:
        f.write(re.sub(",\s?,", ",", \
                    (build_config(modules4apps(EXCLUDED_APPS))).strip("\n")))

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="filename", default=FILENAME, \
                  help="write config to FILE, defualt is `./sync.config`", \
                  metavar="FILE")
    parser.add_option("-f", "--force", dest="force", default=False, \
                      action="store_true", \
                      help="rewrite a file if exists")

    (options, args) = parser.parse_args()
    write_config(filename=options.filename, force=options.force)
    print "Sync config updated!"
    