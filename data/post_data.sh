

#提交 bot-Tree
curl -X POST -H 'content-type: application/json'  -d  @./data/json/bot/english_math_bot_tree.json http://localhost:5000/bot-trees

#提交 bok-Tree
curl -X POST -H 'content-type: application/json'  -d  @./data/json/bok/phy_bok.json http://localhost:5000/bok-trees/

#提交 系统用户(批量)
curl -X POST -H 'content-type: application/json'  -d  @./data/json/system_user_list.json http://localhost:5000/users/

