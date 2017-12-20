#!/bin/bash

#http -b GET ${SUT_B}/schools token==$TOKEN


echo "######先创建一个学校############################"
http -v POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"xysz_66"
}
EOF


one_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"xysz_66"}' | jq -r '._items[0]._id')



echo "######删除该学校的id############################"
http -v DELETE ${SUT_B}/schools/${one_id} token==$TOKEN

echo "######再查询该学校的id, 应该是404 not found############################"
http -v GET ${SUT_B}/schools/${one_id} token==$TOKEN