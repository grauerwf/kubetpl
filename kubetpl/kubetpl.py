#!/usr/bin/env python

import argparse
import yaml
import os
import sys
from jinja2 import Template
from jinja2 import exceptions


required_resources_parameters = ['name', 'path', 'include']


def get_resource_list(resource_list):
    def sub(parent, cur_resource_list):
        for resource in cur_resource_list:
            if 'name' not in resource and 'path' not in resource:
                print("Malformed resources set in cluster config, "
                      "at least one 'name' or 'path' is required")
            else:
                if 'path' in resource:
                    cur_path = os.path.join(parent, resource['path'])
                else:
                    cur_path = os.path.join(parent, resource['name'])
                if 'include' in resource:
                    yield from sub(cur_path, resource['include'])
                else:
                    yield cur_path
    yield from sub('', resource_list)


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i',
                       '--include',
                       dest='include',
                       action='append',
                       help='Resource sets to include explicitly',
                       default=[])
    group.add_argument('-e',
                       '--exclude',
                       dest='exclude',
                       action='append',
                       help='Resource sets to exclude explicitly',
                       default=[])
    parser.add_argument('--var',
                        dest='vars',
                        action='append',
                        help='Provide variables to templates explicitly',
                        default=[])
    parser.add_argument('--kubectl',
                        dest='kubectl_path',
                        help='Path to the kubectl binary (default "kubectl")',
                        default='kubectl')

    parser.add_argument('command',
                        help='Template resourceset'
                             ' and pass to "kubectl <command>"')
    parser.add_argument('file',
                        help='Resource Set to templating')

    return parser.parse_args()


def find_resource_location(resource_path):
    if os.path.isabs(resource_path):
        return resource_path
    if os.path.exists(os.path.join(os.getcwd(), resource_path)):
        return os.path.join(os.getcwd(), resource_path)
    if os.path.exists(os.path.join(os.path.dirname(args.file), resource_path)):
        return os.path.join(os.path.dirname(args.file), resource_path)
    print("Cannot find resource {}, exiting...".format(resource_path))
    exit(1)


def template_resources(resources_list, values):
    templated_resources = ''
    resources_to_template = []
    for resource in resources_list:
        resource_location = find_resource_location(resource)
        if os.path.isfile(resource_location):
            resources_to_template.append(resource_location)
        elif os.path.isdir(resource_location):
            resources_to_template.extend(
                [str(os.path.sep).join([resource_location, file])
                 for file in os.listdir(resource_location)
                 if file.endswith(".yml")
                 or file.endswith(".yaml")
                 or file.endswith(".json")])
    for resource in resources_to_template:
        with open(resource) as template_file:
            try:
                template = Template(template_file.read())
                templated_resources += template.render(values) + '\n'
            except exceptions.TemplateSyntaxError as exc:
                print("Error templating resource {0}, {1}".format(resource, exc.message))
                exit(1)
    return templated_resources


args = parse_args()


def main():
    resources_to_template = []
    with open(args.file) as resource_set_file:
        resource_set = yaml.load(resource_set_file.read(),
                                 Loader=yaml.SafeLoader)
    tpl_vars = resource_set['global']
    resource_set_resources = list(get_resource_list(resource_set['include']))

    if len(args.include) > 0:
        for resource in resource_set_resources:
            for include in args.include:
                if resource.startswith(include):
                    resources_to_template.append(resource)
    elif len(args.exclude) > 0:
        for resource in resource_set_resources:
            for include in args.exclude:
                if not resource.startswith(include):
                    resources_to_template.append(resource)

    else:
        resources_to_template = resource_set_resources
    if len(args.vars) > 0:
        for var in args.vars:
            (var_key, var_value) = var.split('=')
            tpl_vars[var_key] = var_value
    templated_resources = template_resources(resources_to_template, tpl_vars)
    if args.command == 'template':
        print(templated_resources)
    else:
        kubectl_command_tpl = 'echo "{0}" | {1} {2} --context {3} -f -'
        os.system(kubectl_command_tpl.format(templated_resources,
                                             args.kubectl_path,
                                             args.command,
                                             resource_set['context']))


if __name__ == '__main__':
    sys.exit(main())
