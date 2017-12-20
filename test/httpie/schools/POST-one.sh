#!/bin/bash

echo "创建一个学校"
echo "展示学校####################"
http -hb POST ${SUT_B}/schools token==$TOKEN  << EOF
{
"title":"襄阳四中",
"codeDtype":"阿大三的森发送发送地方"
}
EOF
echo "展示学校####################"
one_id=$(http -b GET ${SUT_B}/schools token==$TOKEN where=='{"codeDtype":"阿大三的森发送发送地方"}' | jq -r '._items[0]._id')

echo "删除该学校"
http -bh DELETE ${SUT_B}/schools/${one_id} token==$TOKEN