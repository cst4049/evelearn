#!/bin/bash
echo "######先创建一个学校"
http -hb POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_1001"
}
EOF
school_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_1001"}'| jq -r '._items[0]._id')
echo $school_id

echo "######先创建创建学校的一个年级"
http -hb POST ${SUT_B}/schools/${school_id}/grades token==$TOKEN  << EOF
{
"birth":213312313 ,
"kind":"eniorMiddle"
}
EOF
grade_id=$(http -b GET ${SUT_B}/schools/${school_id}/grades token==$TOKEN where=='{"birth":213312313}'| jq -r '._items[0]._id')


echo "######创建班级"
http -hb POST ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN  << EOF
[
{
	"num":1111111222222 ,

	"studyDirection":"science",

	"code":"311"


},
{
	"num":11111112222223 ,

	"studyDirection":"science",

	"code":"312"


},
{
	"num":111111122222235 ,

	"studyDirection":"science",

	"code":"313"


}
]
EOF

echo "######展示班级############################"
http -hb -b GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN
echo "######展示班级############################"

echo "确认数据是否删除, 如果使用 -v 查看全部. 会返回已经被删除的数据. eve 遗留问题.先不处理"
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id} token==$TOKEN

echo "删除 班级,年级,学校"
item_1=$(http -b GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN where=='{"num":1111111222222}'| jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes/${item_1} token==$TOKEN

item_1=$(http -b GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN where=='{"num":11111112222223}'| jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes/${item_1} token==$TOKEN

item_1=$(http -b GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN where=='{"num":111111122222235}'| jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes/${item_1} token==$TOKEN


http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id} token==$TOKEN

echo $grade_id
echo "确认数据是否删除, 如果使用 -v 查看全部. 会返回已经被删除的数据. eve 遗留问题.先不处理"
http -h GET ${SUT_B}/schools/${school_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
echo "这个查询返回码是200,返回的结果是空,相当于被删除了"
http -v GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN


