"""Cluster Genesis 'gen' command argument parser"""

# Copyright 2017 IBM Corp.
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
from argparse import ArgumentParser, RawTextHelpFormatter

PROJECT = 'Cluster Genesis'
SETUP_CMD = 'setup'
CONFIG_CMD = 'config'
VALIDATE_CMD = 'validate'
DEPLOY_CMD = 'deploy'
SETUP_DESC = 'Setup deployment environment (requires root privileges)'
CONFIG_DESC = 'Configure deployment environment'
VALIDATE_DESC = 'Validate deployment environment'
DEPLOY_DESC = 'Deploy cluster'
GITHUB = 'https://github.com/open-power-ref-design-toolkit/cluster-genesis'
EPILOG = 'home page:\n  %s' % GITHUB
ABSENT = '\u009fabsent\u009c'
LOG_LEVEL_CHOICES = ['nolog', 'debug', 'info', 'warning', 'error', 'critical']
LOG_LEVEL_FILE = ['info']
LOG_LEVEL_PRINT = ['info']


class Cmd(Enum):
    SETUP = SETUP_CMD
    CONFIG = CONFIG_CMD
    VALIDATE = VALIDATE_CMD
    DEPLOY = DEPLOY_CMD


def get_args():
    """Get 'gen' command arguments"""

    parser = ArgumentParser(
        description=PROJECT,
        epilog=EPILOG,
        formatter_class=RawTextHelpFormatter)
    subparsers = parser.add_subparsers()
    common_parser = ArgumentParser(add_help=False)

    # Common arguments
    common_parser.add_argument(
        '-f', '--log-level-file',
        nargs=1,
        default=LOG_LEVEL_FILE,
        choices=LOG_LEVEL_CHOICES,
        metavar='LOG-LEVEL',
        help='Add log to file\nChoices: {}\nDefault: {}'.format(
            ','.join(LOG_LEVEL_CHOICES), LOG_LEVEL_FILE[0]))

    common_parser.add_argument(
        '-p', '--log-level-print',
        nargs=1,
        default=LOG_LEVEL_PRINT,
        choices=LOG_LEVEL_CHOICES,
        metavar='LOG-LEVEL',
        help='Add log to stdout/stderr\nChoices: {}\nDefault: {}'.format(
            ','.join(LOG_LEVEL_CHOICES), LOG_LEVEL_PRINT[0]))

    # Subparsers
    parser_setup = subparsers.add_parser(
        SETUP_CMD,
        description='%s - %s' % (PROJECT, SETUP_DESC),
        help=SETUP_DESC,
        epilog=EPILOG,
        parents=[common_parser],
        formatter_class=RawTextHelpFormatter)

    parser_config = subparsers.add_parser(
        CONFIG_CMD,
        description='%s - %s' % (PROJECT, CONFIG_DESC),
        help=CONFIG_DESC,
        epilog=EPILOG,
        parents=[common_parser],
        formatter_class=RawTextHelpFormatter)

    parser_validate = subparsers.add_parser(
        VALIDATE_CMD,
        description='%s - %s' % (PROJECT, VALIDATE_DESC),
        help=VALIDATE_DESC,
        epilog=EPILOG,
        parents=[common_parser],
        formatter_class=RawTextHelpFormatter)

    parser_deploy = subparsers.add_parser(
        DEPLOY_CMD,
        description='%s - %s' % (PROJECT, DEPLOY_DESC),
        help=DEPLOY_DESC,
        epilog=EPILOG,
        parents=[common_parser],
        formatter_class=RawTextHelpFormatter)

    # 'setup' subcommand arguments
    parser_setup.set_defaults(
        setup=True)

    parser_setup.add_argument(
        '--bridges',
        action='store_true',
        help='Create deployer bridges')

    parser_setup.add_argument(
        '--gateway',
        action='store_true',
        help='Configure PXE network gateway and NAT record')

    parser_setup.add_argument(
        '-a', '--all',
        action='store_true',
        help='TBD')

    # 'config' subcommand arguments
    parser_config.set_defaults(
        config=True)

    parser_config.add_argument(
        '--mgmt-switches',
        action='store_true',
        help='Configure the cluster management switches')

    parser_config.add_argument(
        '--create-container',
        nargs='?',
        default=ABSENT,
        metavar='CONTAINER-NAME',
        help='Create deployer container')

    # 'validate' subcommand arguments
    parser_validate.set_defaults(
        validate=True)

    parser_validate.add_argument(
        '--config-file',
        nargs='?',
        default=ABSENT,
        metavar='CONFIG-FILE',
        help='Schema and logic config file validation')

    parser_validate.add_argument(
        '--cluster-hardware',
        action='store_true',
        help='Cluster hardware discovery and validation')

    # 'deploy' subcommand arguments
    parser_deploy.set_defaults(
        deploy=True)

    parser_deploy.add_argument(
        '-a', '--all',
        action='store_true',
        help='TBD')

    # Check arguments
    args = parser.parse_args()
    try:
        if args.setup:
            _check_setup(args, parser_setup)
    except AttributeError:
        pass
    try:
        if args.config:
            _check_config(args, parser_config)
    except AttributeError:
        pass
    try:
        if args.validate:
            _check_validate(args, parser_validate)
    except AttributeError:
        pass
    try:
        if args.deploy:
            _check_deploy(args, parser_deploy)
    except AttributeError:
        pass

    return parser


def _check_setup(args, subparser):
    if not args.bridges and not args.gateway and not args.all:
        subparser.error(
            'one of the arguments --bridges --gateway -a/--all is required')


def _check_config(args, subparser):
    if not args.mgmt_switches and args.create_container == ABSENT:
        subparser.error(
            'one of the arguments --mgmt-switches --create-container is'
            ' required')


def _check_validate(args, subparser):
    if args.config_file == ABSENT and not args.cluster_hardware:
        subparser.error(
            'one of the arguments --config-file --cluster-hardware is'
            ' required')


def _check_deploy(args, subparser):
    if not args.all:
        subparser.error('one of the arguments -a/--all is required')


def is_arg_present(arg):
    if arg == ABSENT:
        return False
    return True


def get_parsed_args():
    """Get parsed 'gen' command arguments"""

    return get_args().parse_args()