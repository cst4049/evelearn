#!/bin/bash
#1.创建一个school
#2.在school下创建 grade
#3.查询 该年纪
#4.删除该学校
#5.删除该年纪

echo "######先创建一个学校############################"
http -hb POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_68"
}
EOF

school_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_68"}'| jq -r '._items[0]._id')




echo "######先创建创建学校的两个年纪############################"
http -hb POST ${SUT_B}/schools/${school_id}/grades token==$TOKEN  << EOF
[
{
"birth":2999 ,
"kind":"eniorMiddle"
},
{
"birth":2888 ,
"kind":"eniorMiddle"
}
]
EOF
echo "展示两个年级############################"
http -b GET ${SUT_B}/schools/${school_id}/grades token==$TOKEN
echo "展示两个年级############################"




echo "删除该年纪"
temp_id=$(http -b GET ${SUT_B}/schools/${school_id}/grades token==$TOKEN where=='{"birth": 2999}'| jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${temp_id} token==$TOKEN

temp_id=$(http -b GET ${SUT_B}/schools/${school_id}/grades token==$TOKEN where=='{"birth": 2888}'| jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${school_id}/grades/${temp_id} token==$TOKEN

echo "删除该学校"
http -h DELETE ${SUT_B}/schools/${school_id}  token==$TOKEN