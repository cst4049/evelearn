#!/usr/bin/env bash

## question-stat和question-tagging依赖于question，必须出现在question之后

#cat *.yaml > allinone

cat botn.yaml  \
    bott.yaml  \
    burtreenode.yaml  \
    enum.yaml  \
    literal.yaml  \
    picture.yaml  \
    quesbank.yaml  \
    question.yaml  \
    question-stat.yaml  \
    question-tagging.yaml  \
    signal.yaml \
    user.yaml \
    propertySet.yaml \
    exam.yaml \
    jsonWebToken.yaml \
    role.yaml  \
    bokn.yaml  \
    bokt.yaml  \
    school.yaml  \
    grade.yaml  \
    class.yaml  \
    teacher.yaml  \
    student.yaml \
    seminar.yaml \
    seminarSpans.yaml \
    > ../schema-allinone.yaml
