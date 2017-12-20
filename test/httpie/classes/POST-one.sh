#!/bin/bash
echo "######先创建一个学校############################"
http -v POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_1001"
}
EOF
school_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_1001"}'| jq -r '._items[0]._id')
echo $school_id

echo "######先创建创建学校的一个年纪############################"
http -v POST ${SUT_B}/schools/${school_id}/grades token==$TOKEN  << EOF
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


echo "删除 班级,年级,学校"
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id}/ClassStypes/${class_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id} token==$TOKEN


