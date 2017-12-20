#!/bin/bash


#1.创建一个学校
#2.创建这个年级
#3.删除该年级


echo "######先创建一个学校############################"
http -v POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_68"
}
EOF


school_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_68"}'| jq -r '._items[0]._id')

echo "######先创建创建学校的一个年纪############################"
http -v POST ${SUT_B}/schools/${school_id}/grades token==$TOKEN  << EOF
{
"birth":20999999 ,
"kind":"eniorMiddle"
}
EOF
grade_id=$(http -b GET ${SUT_B}/schools/${school_id}/grades token==$TOKEN where=='{"birth":20999999}'| jq -r '._items[0]._id')


echo "删除该学校"
http -b DELETE ${SUT_B}/schools/${school_id}/grades/${grade_id} token==$TOKEN

echo "删除该年级"
http -b DELETE ${SUT_B}/schools/${school_id}  token==$TOKEN