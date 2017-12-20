#!/bin/bash

#http -b GET ${SUT_B}/schools token==$TOKEN


echo "######先创建一个学校############################"
http -hb POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_66"
}
EOF


one_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_66"}' | jq -r '._items[0]._id')

echo "######再拿到这个学校的id############################"
http -hb GET ${SUT_B}/schools/${one_id} token==$TOKEN


echo "######删除该学校的id############################"
http -h DELETE ${SUT_B}/schools/${one_id} token==$TOKEN

echo "######再查询该学校的id, 应该是404 not found############################"
http -h GET ${SUT_B}/schools/${one_id} token==$TOKEN  where=='{"_deleted": "false"}'