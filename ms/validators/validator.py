from datetime import datetime
from uuid import UUID
import arrow
from bson.objectid import ObjectId
from eve.io.mongo import Validator

from ms.models.BOK import BOKNode


#### 提供 coerce  normalize 正规化

class MyValidator(Validator):
    """
    提供一些normalize（正规化，在验证前对doc进行预处理）用的coerce处理函数
        _normalize_coerce_xxxxxx
    提供一些validate（验证化）用的type验证函数
        _validate_type_xxxxxx

    """

    #* 似乎不应该加__init__了??
    def __init__(self, *args, **kwargs):
        super(MyValidator, self).__init__(*args, **kwargs)

        ## 配合 _normalize_coerce_multiply 所使用的参数
        self.multiplier = kwargs.get('multiplier', 2)


    """ _validate_<rulename>
    ################################################################
    """

    def _validate_description(self, description, field, value):
        """ 在schema中可以定义属性的时候可以有description描述，这是一个假的validate rule

        The rule's arguments are validated against this schema:
        {'type': 'string'}

        """
        if False :
            self._error(field, "")

    def _validate_isDerived(self,field,value):
        """
        推导属性 设置为True，表示为推导属性，不存数据库
        ，以此属性查询时需要处理后查询，
        查询该属性时需要计算得出
        :param field:
        :param value:
        :return:

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        pass

    def _validate_enum(self, enum, field, value):
        """ 在schema中可以定义属性的时候可以有description描述，这是一个假的validate rule

        The rule's arguments are validated against this schema:
        {'type': 'string'}

        """

        # TODO: 查询enum数据库中名字为此处
        if( False ):
            self._error( field, "value '%s' are not the valid, maybe you use the wrong name of literals!" % value)


    """  _validate_type_<typename>
    ################################################################
    """

    def _validate_type_uuid(self, field, value):
        """
        以_validate_type_为前缀的Validator成员方法，其词根可以作为schema定义中的type的字符串值。
        对于词根uuid而言，schema定义为{'foo': {'type': 'uuid'}}，
        此种情况下，Validator会验证该字段的值是否符合uuid，验证的方式就是本函数

        :param field:
        :param value:
        :return:
        """
        try:
            UUID(value)
        except ValueError:
            self._error(field, "value '%s' cannot be converted to a UUID" % value)


    """  __validator_<validator_name>
    ################################################################
    """


    def _validator_bur_tree_node(self, field, value):
        """自定义validator：

        在schema定义一个属性，含有validator: bur_tree_node，就会启动本validator
            bur_tree_node:
              type: dict
              validator: bur_tree_node  或者 [ bur_tree_node ]

        :param field:
        :param value:
        :return:
        """
        if False :
            self._error(field, "Must be an odd number")


    """   _normalize_coerce_<coerce_name>
    ################################################################
    """

    def _normalize_coerce_deunit(self, value):
        """正规化: deunit
        当值中包含单位的时候，去掉单位，将其转化为数字，默认单位采用国际标准单位

        在schema中定义一个属性，含有coerc: deunit，就会先启动本正规化，然后再validate

            period:
              type: number
              coerce: deunit

        :param value:
        :return:
        """

        if isinstance(value, str):
            if value[-2:] == " s":  ## 单位为秒
                return float(value[:-2])
            if value[-2:] == " ms":  ## 单位为毫秒
                return float(value[:-2]) * 0.001

        # TODO: 各种各样的去单位

        return value

    def _normalize_coerce_multiply(self, value):
        """正规化: multiply
        把值统统放大

        以_normalize_coerce_作为前缀的Validator成员方法，定义后，其词根可以作为schema定义中的coerce的字符串值。
        对于词根为multiply而言， schema定义为{'foo': {'coerce': 'multiply'}}，
        此种情况下，Validator会将字符串'multiply'替换为callable的成员变量，
        这样可以达到schema定义为纯json对象（不包括callable的python代码）

        >>> schema = {'foo': {'coerce': 'multiply'}}
        >>> document = {'foo': 2}
        >>> MyValidator(2).normalized(document, schema)
        {'foo': 4}

        :param value:
        :return:
        """
        return value * self.multiplier



    """  _normalize_default_setter_<validator_name>
    ################################################################
    """
    def _normalize_default_setter_utcnow(self, document):
        """

        当属性定义有 default_setter设置
        creation_date:
          type: datetime
          default_setter: utcnow


        :param document:
        :return:
        """
        return datetime.utcnow()

    def _normalize_coerce_align_to_day(self, value):
        return arrow.get(value).replace(hour=0,minute=0,second=0).datetime

    def _validate_type_boknpid(self,value):
        """
        以_validate_type_为前缀的Validator成员方法，其词根可以作为schema定义中的type的字符串值。
        对于词根uuid而言，schema定义为{'foo': {'type': 'uuid'}}，
        此种情况下，Validator会验证该字段的值是否符合uuid，验证的方式就是本函数

        :param value:
        :return:
        """
        if isinstance(value,list):
            for val in value:
                if not ObjectId.is_valid(val):
                    return False
                bok = BOKNode.coll().find_one(ObjectId(val))
                if not bok:
                    return False
                if bok.get("koLyro") != "point":
                    return False
            return True
        if not ObjectId.is_valid(value):
            return False
        bok = BOKNode.coll().find_one(ObjectId(value))
        if not bok:
            return False
        if bok.get("koLyro") != "point":
            return False
        return True

    def _normalize_coerce_distbok(self, value):
        """
        distinct bokn,去除重复包含id，保留底层id
        :param value:
        :return:
        """
        bok = BOKNode.coll()
        valueobj = [ObjectId(i) for i in value]
        lookup = {"_id":{"$in":valueobj}}
        dadlist = []
        values_info = list(bok.find(lookup))
        [valueobj.remove(val.get("dad")) for val in values_info if val.get("dad") in valueobj]
        return valueobj






