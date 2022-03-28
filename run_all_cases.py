# -*- coding:utf-8 -*- #
import os
import string
import sys
import yaml

import click
import pytest

from util.util import get_yaml_content, write_yaml_content

root_dir = os.path.dirname(__file__)
sys.path.append(root_dir)


# root_dir = os.path.abspath(os.path.dirname(__file__))
# default_conf_yml_dir = f'{root_dir}/conf/conf.default.yml'
# conf_yml_dir = f'{root_dir}/conf/conf.yml'


@click.command()
# @click.option(
#     "-u",
#     "--url",
#     required=True,
#     type=click.STRING,
#     help="test env",
# )
# @click.option(
#     "-p",
#     "--project_id",
#     required=True,
#     type=click.STRING,
#     help="project id",
# )
@click.option(
    "-m",
    "--mark",
    required=False,
    type=click.STRING,
    help="testcase of tag",
)
def main(mark=None):
    # 未指定标签，执行所有用例
    if mark is None or mark == '':
        pytest.main(["./testcase"])
    else:
        # 执行标记tag的用例
        pytest.main(["-m", f"{mark}"])


if __name__ == '__main__':
    # get_param()
    # set_param('http://uat-gdp.growingio.com', 'WlGk4Daj')
    # set_param()
    # pytest.main(["-m", "platform_group"])
    # print('end')
    main()


