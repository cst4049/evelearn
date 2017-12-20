from bson import ObjectId

from ms.resources.unit import Chinese_Num_Map


class BurTree:
    pass

class BurTreeNode:
    pass


def flatten_burtree_by_recursion(items, list):
    """
    将传入bokt 扁平化, 将其转为一个一个的节点存入数组
    author: 琛
    :param items:
    :param list:
    :return 返回一个数组 该数组包含bokt的所有节点:
    """
    if type(items) == type({}):
            item_sub = items
            if "son" in item_sub:
                subs = item_sub.pop("son")
                if type(subs) != type(None):
                    #为册添加科目名
                    if item_sub['koLyro'] == 'discipline':
                        for son_item in subs:
                            son_item.update(discipline=item_sub['name'])
                    index = []
                    #如果存在objectId 则使用. 否则生成一个作为_id
                    if "_id" not in item_sub:
                        origin_id = ObjectId()
                        item_sub.update(_id=origin_id)
                    else:
                        origin_id  = item_sub['_id']

                    #给子类添加 父_id 并把子类_id 存在父_id的son数组里
                    for sub in subs:
                        _id = ObjectId()
                        index.append(_id)
                        sub.update(_id=_id, dad=origin_id)
                        sub.update(edition=item_sub['edition'])
                        item_sub.update(son=index)

                    for item in subs:
                        flatten_burtree_by_recursion(item, list)
            list.append(item_sub)

    if type(items) ==type([]):
        for item_sub in items:
            if "son" in item_sub:
                subs = item_sub.pop("son")
                if type(subs) != type(None):

                    #为册添加科目名
                    if item_sub['koLyro'] == 'discipline':
                        for son_item in subs:
                            son_item.update(discipline=item_sub['name'])
                    index = []
                    #如果存在objectId 则使用. 否则生成一个作为_id
                    if "_id" not in item_sub:
                        origin_id = ObjectId()
                        item_sub.update(_id=origin_id)
                    else:
                        origin_id  = item_sub['_id']

                    #给子类添加 父_id 并把子类_id 存在父_id的son数组里
                    for sub in subs:
                        _id = ObjectId()
                        index.append(_id)
                        sub.update(_id=_id, dad=origin_id)
                        sub.update(edition=item_sub['edition'])
                        item_sub.update(son=index)


                    for item in subs:
                        flatten_burtree_by_recursion(item, list)
            list.append(item_sub)

def flatten_burtree_by_recursion_burtree(items, list):
    """
    将树拆成表存入数据库中
    author: 琛
    :param items:
    :param list:
    :return 返回一个数组 该数组包含bokt的所有节点:
    """
    if type(items) == type({}):
            item_sub = items
            if "son" in item_sub:
                subs = item_sub.pop("son")
                if type(subs) != type(None):
                    #为册添加科目名

                    index = []
                    #如果存在objectId 则使用. 否则生成一个作为_id
                    if "_id" not in item_sub:
                        origin_id = ObjectId()
                        item_sub.update(_id=origin_id)
                    else:
                        origin_id  = item_sub['_id']

                    #给子类添加 父_id 并把子类_id 存在父_id的son数组里
                    for sub in subs:
                        _id = ObjectId()
                        index.append(_id)
                        sub.update(_id=_id, dad=origin_id)
                        sub.update(edition=item_sub['edition'])
                        item_sub.update(son=index)

                    for item in subs:
                        flatten_burtree_by_recursion_burtree(item, list)
            list.append(item_sub)

    if type(items) ==type([]):
        for item_sub in items:
            if "son" in item_sub:
                subs = item_sub.pop("son")
                if type(subs) != type(None):


                    index = []
                    #如果存在objectId 则使用. 否则生成一个作为_id
                    if "_id" not in item_sub:
                        origin_id = ObjectId()
                        item_sub.update(_id=origin_id)
                    else:
                        origin_id  = item_sub['_id']

                    #给子类添加 父_id 并把子类_id 存在父_id的son数组里
                    for sub in subs:
                        _id = ObjectId()
                        index.append(_id)
                        sub.update(_id=_id, dad=origin_id)
                        sub.update(edition=item_sub['edition'])
                        item_sub.update(son=index)


                    for item in subs:
                        flatten_burtree_by_recursion_burtree(item, list)
            list.append(item_sub)

def flattern_convertTo_tree(list
                            ):
    """
    将 list列表 组装成树
    :param list:
    :return:
    """
    dadList=[]
    sonList =[]
    for item in list:
        if 'son' in item :
            # if sonList.count(item['son'])
            if type(item['son']) == type(list):
                for son_item in item['son']:
                    sonList.append(son_item)
# ##################################
#             else:
#                 sonList.append(item['son'])
# ##################################
        if 'dad' in item :
            dadList.append(item['dad'])

    for dad_item  in dadList:
        if dad_item not in sonList:
             root_dad_id = dad_item

    root = []
    for i in list:
        if root_dad_id == i['dad']:
            root.append(i)
    if type(root) == type([]):
        for root_item in root:
            if 'son' in root_item:
                    #调用 将该节点下所有son节点都找到的方法
                root_son_node = flattern_convertTo_tree_recursion(root_item['son'],list)
                root_item.update(son=root_son_node)
# ##################################
#     else:
#         root = flattern_convertTo_tree_recursion(root,list)
# ##################################
    return root


def flattern_convertTo_tree_recursion(obj_id_list, node_list):
    """
    botn 列表 转换为 tree的方法.一般不直接调用. 通常调用 flattern_convertTo_tree
    :param obj_id_list:
    :param node_list:
    :return:
    """
    """
    1.将obj_id 变成obj对象
    2.判断obj是否有 son节点
        有. 调用自身
        否. obj 替换 obj_id ,存到数组中.
        返回
    """
    for id_list_index in range(len(obj_id_list )):
        #1.将其转化为 对象
        for node_item in node_list:
            if node_item['_id'] == obj_id_list[id_list_index]:
                #2. 找到该对象 判断是否有son 节点 ,有 则递归. 否 则替换list对象
                obj_id_obj = node_item
                if 'son' in obj_id_obj:
                    flattern_convertTo_tree_recursion(obj_id_obj['son'],node_list)
                son_list = obj_id_obj.get("son")
                if type(son_list) == type([]):
                    son_list = sorted(son_list,key= lambda item : Chinese_Num_Map.chinese_num_mapping(item.get("name")))
                    obj_id_obj['son'] = son_list
                obj_id_list[id_list_index] = obj_id_obj
    return obj_id_list




