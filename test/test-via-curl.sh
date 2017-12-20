# 题库的增加
curl -X POST -H "Content-Type:application/json" -d '{"name":"math","title":"数学题"}' http://localhost:5000/questionbanks

# 题库的查找
curl http://localhost:5000/questionbanks
curl http://localhost:5000/questionbanks/{name}  # name=math
curl http://localhost:5000/questionbanks/{id}  # id=59c8a8b90b4b4b6464c31bfc

# 题库信息的修改
curl -X PATCH -H "Content-Type:application/json" -d '{"name":"math","title":"小学数学"}' http://localhost:5000/questionbanks/59c8a8b90b4b4b6464c31bfc

# 题库信息的替换
curl -X PUT -H "Content-Type:application/json" -d '{"name":"english"}' http://localhost:5000/questionbanks/59c8a8b90b4b4b6464c31bfc

# 题库信息的删除
curl -X DELETE http://localhost:5000/questionbanks/59c8a8b90b4b4b6464c31bfc

# 题目上传命令(会自动加上questionbanks信息)
curl -v -X POST -H "Content-Type:application/json" -d '{"QuestionPoSource":{"koSource":"acbe"},"QuestionPoContent":{"contOfQuery":"ccccc"}}' http://localhost:5000/questionbanks/{name}/questions

# 题目的查找
curl http://localhost:5000/questionbanks/{name}/questions
curl http://localhost:5000/questionbanks/{name}/questions/{id}  # id=id

# todo
curl http://localhost:5000/questionbanks/{name}/questions/{id}/similar/?topN=3&similarity_gt=1
curl http://localhost:5000/quesbanks/{name}/questions/?similar_to={id}&similarity_gt=1&topN=3

# 题目修改命令
curl -v -X PATCH -H "Content-Type:application/json" -d '{"QuestionPoSource":{"koSource":"AAAAAAAAA"}}' http://localhost:5000/questionbanks/{name}/questions/{id}

# 题目替换
curl -v -X PUT -H "Content-Type:application/json" -d '{"QuestionPoSource":{"koSource":"AAAAAAAAA"},"QuestionPoContent":{"contOfQuery":"ccccc"}}' http://localhost:5000/questionbanks/{name}/questions/{id}

# 题目的删除
curl -X DELETE http://localhost:5000/questionbanks/{name}/questions/{id}

# 题目的图片
curl -v -X POST -H "Content-Type:application/json" -d '{"QuestionPoSource":{"koSource":"acbe"},"QuestionPoContent":{"contOfQuery":"ccccc"}}' http://localhost:5000/questionbanks/{name}/questions/pictures

# x-http--method-override用法示例（spur 代替get方法）
curl -H "X-HTTP-Method-Override:GET" -X SPUR 'http://localhost:5000/questionbanks/'