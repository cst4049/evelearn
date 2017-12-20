#!/usr/bin/env python

# = 科算的cli接口，包括
# =   为指定的数据库的指定的题目集合，添加 simhash字段（具体可能能是4个字段，名为simhash，simhashS0,S1,S2,S3
# =     其中simhashS0指的是64bit simhash值的头16位
# =   列出指定题目集合的相似组
# =   给定一个题目内容，以及作为基准的重复查询集合，给出按照simhash相似的题目。
# =   给定一个题目内容，以及作为基准的重复查询集合，给出按照编辑距离相似的题目。

#

import click
import sys
sys.path.append("../../")
from sc.cli import addhash
from sc.question_similarity.similar_check import get_similar
from sc.question_analize.cluster import question_cluster
from sc.question_fingerprint import db


@click.group()
def cli():
    pass

@cli.command()
@click.argument('collection')
@click.argument('scope',default={})
def resimhash(collection,scope):
    """

    :param collection: 题目集合（可以指定多个），类似mongo://host:port/base/collection?where={"name":"bb"}
    :return:
    """
    print("you specified collection:", collection,scope)
    addhash.addcode(collection,scope)


@cli.command()
@click.option('--layer', type=click.Choice(['0','infinite']), help='''构成相似关系的次数''')
@click.option('--target', type=click.Path(writable=True), help='''输出到文件而不是控制台''')
@click.argument('collection', nargs=1)
def group(collection, target, layer=0):
    """

    :param collection: 题目集合，类似mongo://host:port/base/collection?where={"name":"bb"}

    输出按照simhash构成的重复题目组合，凡是simhash的hamming距离小于等于3的，视为相似题目，传递闭包构成相似组。

    输出相似组信息

    :param target:
    :return:
    """

    pass




@cli.command()
@click.option('--content', help='''题目内容文本''')
@click.option('--by', type=click.Choice(['simhash', 'levenshtein']), help='''选择类型''')
@click.argument('collection', nargs=1)
def similar(collection, content,by):
    """


    """
    data = get_similar(content)


@cli.command()
@click.argument('collection',default="questions")
@click.option('--max_depth', help='''海明距''',default=4)
@click.option('--format',default="grouped")
def find_sim(collection, format,max_depth):
    """

    """
    ques_col = db[collection]
    questions = list(ques_col.find({"simhash": {"$exists": True}}, {"simhash": 1, "contOfQuery": 1}))
    question_cluster(questions,format=format,max_d=max_depth)


if __name__ == '__main__':
    cli()