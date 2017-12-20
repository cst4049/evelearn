#!/bin/bash
echo "######先创建一个学校############################"
http -hb POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_1001"
}
EOF
school_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_1001"}'| jq -r '._items[0]._id')
echo $school_id

echo "######先创建创建学校的一个年纪############################"
http -hb POST ${SUT_B}/schools/${school_id}/grades token==$TOKEN  << EOF
{
"birth":2030 ,
"kind":"eniorMiddle"
}
EOF
grade_id=$(http -b GET ${SUT_B}/schools/${school_id}/grades token==$TOKEN where=='{"birth":2030}'| jq -r '._items[0]._id')


echo "######创建班级############################"
http -hb POST ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN  << EOF

{
	"num":21 ,

	"studyDirection":"science",

	"code":"3dasdasdasdsadsgdfdg11"


}

EOF

echo "######展示班级############################"
http -hb GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN

class_id =$( http -b GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN where=='{"code":"3dasdasdasdsadsgdfdg11"}'| jq -r '._items[0]._id')

echo "######展示班级############################"

echo "确认数据是否删除, 如果使用 -v 查看全部. 会返回已经被删除的数据. eve 遗留问题.先不处理"
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes/${class_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id} token==$TOKEN

echo "删除 班级,年级,学校"
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes/${class_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id} token==$TOKEN

echo "确认数据是否删除, 如果使用 -v 查看全部. 会返回已经被删除的数据. eve 遗留问题.先不处理"
http -h GET ${SUT_B}/schools/${school_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN

echo "这个查询返回码是200,返回的结果是空,相当于被删除了"
http -v GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN


