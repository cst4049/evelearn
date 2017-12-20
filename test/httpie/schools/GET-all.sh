#!/bin/bash

echo "######先创建3个学校############################"
http -v POST ${SUT_B}/schools token==$TOKEN  << EOF
[
{
"title":"襄阳1中",
"codeDtype":"xysz_61111"
},{
"title":"襄阳2中",
"codeDtype":"xysz_62222"
},{
"title":"襄阳3中",
"codeDtype":"xysz_63333"
}
]
EOF
echo "######展示学校内容############################"

http -b GET ${SUT_B}/schools/ token==$TOKEN
echo "######展示学校内容############################"


echo "######删除相关信息############################"
one_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_61111"}' | jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${one_id} token==$TOKEN

one_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_62222"}' | jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${one_id} token==$TOKEN

one_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_63333"}' | jq -r '._items[0]._id')
http -h DELETE ${SUT_B}/schools/${one_id} token==$TOKEN




