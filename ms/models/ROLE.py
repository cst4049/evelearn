from flask import current_app as app
from flask import g,abort


class Role:


    @staticmethod
    def coll():
        col = app.data.driver.db['roles']
        return col

    @staticmethod
    def authcheck(operate,data):
        user_role = g.user.get("primaryRole")
        user_disc = g.user.get("primaryDiscipline")
        user_id = g.user.get("_id")

        if operate == "Get":
            """
            题目查看
              1 录题员
                1.1 只可以看到自己所录的题目
              2 打标员
                2.1 可以看到本科目所有已经审核过的题目
              3 学科管理员，管理员，超级管理员
                3.1 所有权限
            """
            if user_role == "xk_cb_typewritist":
                data.update(typewritedByFirstly=user_id)
            # 打标员可以看到自己所属科目的题目，状态为2,3,4
            if user_role == "xk_cb_tagist":
                data.update(state={"$in":[2,3,4]},
                            koDiscipline=user_disc)
            return data

        if operate == "Type":
            """ 
            录题权限
              1 录题员
                1.1 只能录入本科题目
                1.2 只能修改自己录入且录题未审核的题目
              2 打标员
                2.1 不允许录题
              3 学科管理员，管理员，超级管理员
                3.1 所有权限
            """
            if data.get("state") in [2,3,4]:
                abort(403, description="not allow to add question")
            if user_role == "xk_cb_typewritist":
                if user_disc != data.get("koDiscipline"):
                    abort(403, description="not allow to add question")

                if data.get("typewritedByFirstly") and \
                    user_id != data.get("typewritedByFirstly") \
                    and data.get("state") !=1:
                    abort(403, description="not allow to add question")

            if user_role == "xk_cb_tagist":
                abort(403, description="not allow to add question")

        if operate == "Tag":
            """ 
            录题权限
              1 录题员
                1.1 不允许打标
              2 打标员
                2.1 只允许打标本科目
                2.2 只能修改自己打标且打标未审核的题目
              3 学科管理员，管理员，超级管理员
                3.1 所有权限
            """
            if data.get("state") not in [2,3]:
                return 403

            if user_role == "xk_cb_typewritist":
                abort(403, description="not allow to tag question")

            if user_role == "xk_cb_tagist":
                if user_disc != data.get("koDiscpline"):
                    abort(403, description="not allow to tag question")

                if data.get("tagedByFirstly") and \
                    user_id !=data.get("tagedByFirstly") and \
                    data.get("state") not in [2,3]:
                    abort(403, description="not allow to tag question")

        if operate == "typewriteCheck" or operate == "tagCheck":
            """
            录题权限
              1 录题员
                1.1 不允许审核
              2 打标员
                2.1 不允许审核
              3 学科管理员，管理员，超级管理员
                3.1 所有权限
            """
            if operate == "typewriteCheck" and data.get("state") not in [1,2,3]:
                return 403

            if operate == "tagCheck" and data.get("state") not in [3,4]:
                return 403

            if user_role == "xk_cb_typewritist":
                abort(403, description="not allow to check question")

            if user_role == "xk_cb_tagist":
                abort(403, description="not allow to check question")

        if operate == "Delete":
            """
            删题权限
              1 录题员
                1.1 unknow
              2 打标员
                2.1 unknow
              3 学科管理员，管理员，超级管理员
                3.1 所有权限
            """
            pass # todo

