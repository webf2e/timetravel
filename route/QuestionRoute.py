from flask import Blueprint
from flask import session,request,Response
from service import QuestionService
import json
import uuid

questionRoute = Blueprint('questionRoute', __name__)

@questionRoute.route('/getQuestions',methods=["POST"])
def getQuestions():
    questions = QuestionService.getRandomQuestions()
    return Response(questions, mimetype='application/json')

@questionRoute.route('/getAnswer',methods=["POST"])
def getAnswer():
    id = request.form.get("ids")
    answers = QuestionService.getAnswerByIds(id)
    answer = str(request.form.get("answer")).split(",")
    ids = id.split(",")
    result={}
    for a in answers:
        index = ids.index(str(a[0]))
        print("{}->{}".format(a[1],answer[index]))
        if(a[1] == answer[index]):
            result[a[0]] = 1
            QuestionService.updateCorrectQuestion(a[0])
        else:
            result[a[0]] = 0
            print("【回答错误】{} -> {}".format(a[2], answer[index]))
            QuestionService.updateErrorQuestion(a[0])
    result["uuid"] = str(uuid.uuid4())
    session["uuid"]=result["uuid"]
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')