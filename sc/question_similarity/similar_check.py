from sc.question_fingerprint import ques_col,comparecode,doall


def similar_check(code,lookup=None):
    if not lookup:
        lookup = {}
    simhash_1,simhash_2,simhash_3,simhash_4 = code
    lookup.update({
        "$or": [
            {"simhash_1": simhash_1},
            {"simhash_2": simhash_2},
            {"simhash_3": simhash_3},
            {"simhash_4": simhash_4}
        ],
        "dad": {
            "$exists": False
        },
        "_deleted": False
    })
    projection = {
        # "hashseg1":1,
        # "hashseg2":1,
        # "hashseg3":1,
        # "hashseg4":1
    }
    questions = list(ques_col.find(lookup))
    similar = []
    for question in questions:
        qseg1 = question.get("simhash_1")
        qseg2 = question.get("simhash_2")
        qseg3 = question.get("simhash_3")
        qseg4 = question.get("simhash_4")
        old_code = (qseg1 << 48) + (qseg2 << 32) + (qseg3 << 16) + qseg4
        code = (simhash_1 << 48) + (simhash_2 << 32) + (simhash_3 << 16) + simhash_4
        if comparecode(old_code,code):
            similar.append(question)
    if similar:
        return True,similar
    return False,code


def get_similar(content,lookup=None):
    if not lookup:
        lookup = {}
    hashcode = doall(content)
    hashseg_1, hashseg_2, hashseg_3, hashseg_4 = hashcode >> 48, (hashcode >> 32) & 0x0000ffff, (
    hashcode >> 16) & 0x00000000ffff, hashcode & 0x000000000000ffff
    data = similar_check((hashseg_1,hashseg_2,hashseg_3,hashseg_4), lookup)
    if data[0]:
        return data[1]
    return []