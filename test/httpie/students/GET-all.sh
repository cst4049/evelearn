#!/bin/bash
echo "######先创建一个学校############################"
http -h POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_1001"
}
EOF
school_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_1001"}'| jq -r '._items[0]._id')
echo $school_id

echo "######先创建创建学校的一个年纪############################"
http -h POST ${SUT_B}/schools/${school_id}/grades token==$TOKEN  << EOF
{
"birth":2030 ,
"kind":"eniorMiddle"
}
EOF
grade_id=$(http -b GET ${SUT_B}/schools/${school_id}/grades token==$TOKEN where=='{"birth":2030}'| jq -r '._items[0]._id')


echo "######创建班级############################"
http -b POST ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN  << EOF

{
	"num":21 ,

	"studyDirection":"science",

	"code":"dadsadada"
}

EOF

echo "###############################"
class_id=$(http -b GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN where=='{"code":"dadsadada"}'| jq -r '._items[0]._id')
echo ${class_id}
echo "###############################"

echo "######创建学生############################"
http -v POST ${SUT_B}/schools/${school_id}/classes/${class_id}/students token==$TOKEN  << EOF
[
{
	"code":"21312311231343423",
	"name":"王二丫"
},
{
	"code":"21312311231343423",
	"name":"王脚丫"
}
]
EOF
student_id=$(http -b GET ${SUT_B}/schools/${school_id}/classes/${class_id}/students/ token==$TOKEN where=='{"name":"王二丫"}'| jq -r '._items[0]._id')
student_id_1=$(http -b GET ${SUT_B}/schools/${school_id}/classes/${class_id}/students/ token==$TOKEN where=='{"name":"王脚丫"}'| jq -r '._items[0]._id')







echo "######展示学生############################"
http -b GET ${SUT_B}/schools/${school_id}/classes/${class_id}/students/ token==$TOKEN where=='{"name":{"$in":["王二丫","王脚丫"]}}'
echo "######展示学生完毕############################"

echo "确认数据是否删除, 如果使用 -v 查看全部. 会返回已经被删除的数据. eve 遗留问题.先不处理"
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id}/classes/${class_id}/students/${student_id} token==$TOKEN
http -h GET ${SUT_B}/schools/${school_id}/classes/${class_id}/students/${student_id_1} token==$TOKEN




http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id}/classes/${class_id}/students/${student_id} token==$TOKEN

