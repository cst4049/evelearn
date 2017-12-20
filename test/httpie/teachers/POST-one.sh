#!/bin/bash



#1. 创建 学校
#2. 拿到学校ID
#3. 创建老师
#4. 拿到老师ID
#5. 删除 老师ID
#6. 删除学校

echo "######先创建一个学校############################"
http -h POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳1001中",
"codeDtype":"xysz_1001"
}
EOF
school_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_1001"}'| jq -r '._items[0]._id')




echo "######创建老师############################"
http -v POST ${SUT_B}/schools/${school_id}/teachers token==$TOKEN  << EOF
{
	"code":123,
	"name":"王1丫",
	"sex":"female",
	"codeDtype":"ptgz_dl_wer1",
	"primaryDiscipline":"math"
}
EOF
teacher_id_1=$(http -b GET ${SUT_B}/schools/${school_id}/teachers  token==$TOKEN where=='{"codeDtype":"ptgz_dl_wer1"}'| jq -r '._items[0]._id')


echo "删除相关信息"
http -h DELETE ${SUT_B}/schools/${school_id} token==$TOKEN
http -h DELETE ${SUT_B}/schools/${school_id}/teachers/${teacher_id_1} token==$TOKEN



