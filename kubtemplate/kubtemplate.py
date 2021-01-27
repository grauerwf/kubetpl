#!/usr/bin/env python

import argparse
import yaml
import os
from jinja2 import Template


def get_resource_list(resource_map):
    def sub(m, res):
        if type(m) == dict:
            for k, v in m.items():
                yield from sub(v, res+[k])
        elif type(m) == list:
            for v in m:
                yield from sub(v, res)
        else:
            yield str(os.path.sep).join(res+[m])
    yield from sub(resource_map, [])


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--include', dest='include', action='append', help='Resource sets to include explicitly', default=[])
    group.add_argument('-e', '--exclude', dest='exclude', action='append', help='Resource sets to exclude explicitly', default=[])
    parser.add_argument('--var', dest='vars', action='append', help='Provide variables to templates explicitly')
    parser.add_argument('--kubectl', dest='kubectl_path', help='Path to the kubectl binary (default "kubectl")')

    parser.add_argument('command', help='Template resource sets and pass to "kubectl <command>"')
    parser.add_argument('file',  help='Resource Set to templating')

    return parser.parse_args()


def template_resources(resources_list, values):
    templated_resources = ''
    resources_to_template = []
    for resource in resources_list:
        if not os.path.isabs(resource):
            resource = os.path.join(os.getcwd(), resource)
        if os.path.isfile(resource):
            resources_to_template.append(resource)
        elif os.path.isdir(resource):
            resources_to_template.extend([str(os.path.sep).join([resource, file]) for file in os.listdir(resource) if file.endswith(".yml")])
            resources_to_template.extend([str(os.path.sep).join([resource, file]) for file in os.listdir(resource) if file.endswith(".yaml")])
            resources_to_template.extend([str(os.path.sep).join([resource, file]) for file in os.listdir(resource) if file.endswith(".json")])
    for resource in resources_to_template:
        with open(resource) as template_file:
            template = Template(template_file.read())
            templated_resources += template.render(values) + '\n'
    return templated_resources


def main():
    resources_to_template = []
    args = parse_args()
    # if len(args.include) > 0 and len(args.exclude) > 0:
    with open(args.file) as resource_set_file:
        resource_set = yaml.load(resource_set_file.read(), Loader=yaml.SafeLoader)
    resource_set_resources = list(get_resource_list(resource_set['include']))
    if len(args.include) > 0:
        for resource in resource_set_resources:
            if resource in args.include:
                resources_to_template.append(resource)
    elif len(args.exclude) > 0:
        for resource in resource_set_resources:
            if resource not in args.exclude:
                resources_to_template.append(resource)
    else:
        resources_to_template = resource_set_resources
    templated_resources = template_resources(resources_to_template, resource_set['global'])
    if args.command == 'template':
        print(templated_resources)
    else:
        # print('echo {0} | kubectl {1} -f -'.format(templated_resources, args.command))
        os.system('echo "{0}" | kubectl {1} -f -'.format(templated_resources, args.command))


if __name__ == '__main__':
    sys.exit(main())
