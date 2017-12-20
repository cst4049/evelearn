#
# this.sh
# H=xxxx ; this.sh
# HOST=xxxx ; PORT=yyyy ; PATH=zzzz ; this.sh
host=${HOST:-127.0.0.1}
#172.17.12.6
port=${PORT:-5000}
path=${var_path:-"./src"}
# echo "$host"
#echo "$port"
#echo "$path"

echo "${#port} ${#host}"


echo "${port} ${host}"



##枚举enum
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/BOKLyroEnum.json http://${host}:${port}/mm/enums
 curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/BotLyroEnum.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/CheckStatusEnum.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/EnglishClozeMaterialLengthDeg.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/EnglishMatchingMaterialLengthDeg.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/EnglishQuestionComboFormatKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/EnglishReadingComprehensionMaterialLengthDeg.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/EnglishReadWriteTaskMaterialLengthDeg.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/ExampaperDisciplineKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/FlrEnum.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/Lyrienum.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionDifficultyKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionDisciplineKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionEnglishComboObjectiveKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionMaterialKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionMaterialLengthDeg.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionQueryFormatKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionResponseFormatKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionSourceKind.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionSourceLocaEnum.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/QuestionSourceTimeEnum.txt http://${host}:${port}/mm/enums
curl -X POST -H 'content-type: application/json'  -d  @${path}/enum/UserStatus.txt http://${host}:${port}/mm/enums

#录题
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/biology.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/chemistry.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/english.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/geography.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/history.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/math.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/physics.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/edit/politics.txt http://${host}:${port}/propertysets

#打标
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/e2_biology.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/e2_chemistry.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/e2_geography.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/e2_history.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/e2_math.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/e2_physics.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/e2_politics.txt http://${host}:${port}/propertysets

#打标-英语
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/cloze.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/fillWordInSentence.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/fillwordintext.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/matching.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/patternTransformation.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/phraseTransformation.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/reading_comprehension.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/sentenceCompletion.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/sentenceCorrection.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/sentenceTranslation.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/simple_selection.txt http://${host}:${port}/propertysets
curl -X POST -H 'content-type: application/json'  -d  @${path}/propertySet/mark/textCorrection.txt http://${host}:${port}/propertysets

#角色
curl -X POST -H 'content-type: application/json'  -d  @${path}/role/all_roles.txt http://${host}:${port}/roles

#bokt bott
curl -X POST -H 'content-type: application/json'  -d  @${path}/bok/bok.json http://${host}:${port}/bok-trees
curl -X POST -H 'content-type: application/json'  -d  @${path}/bot/bot.json http://${host}:${port}/bot-trees
curl -X POST -H 'content-type: application/json'  -d  @${path}/vocabulary_phrase/phrase.txt http://${host}:${port}/wordlists
curl -X POST -H 'content-type: application/json'  -d  @${path}/vocabulary_phrase/vocabulary.txt http://${host}:${port}/wordlists

