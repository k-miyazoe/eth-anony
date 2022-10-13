from pydoc import render_doc
from rest_framework import generics, permissions
from .models import User,Question,Answer,QuestionLike,AnswerLike,QuestionBad,AnswerBad
from .serializers import UserSerializer,QuestionSerializer,AnswerSerializer
from web3 import Web3
import environ,json
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.db.models import F

env = environ.Env()
env.read_env('back.env')

#remote provider sets 使用していない
w3 = Web3(Web3.HTTPProvider(env('GETH_REMOTE_PROVIDERS')))

class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    #管理者のみユーザーリスト確認可能
    #permission_classes = (permissions.IsAdminUser,)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #確認作業でパーミッションを設定しておくのはめんどくさいのでコメントアウト中 本番ではコメントアウト解除する
    #permission_classes = (permissions.IsAuthenticated, )
    
class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#Question
#[user_groupごとの質問を返す]
class QuestionList(generics.ListAPIView):
    #投稿時間が新しい順に変更したい[いつか調べる]
    queryset = Question.objects.all()
    #queryset = Question.objects.all().order_by('question_post_time')
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        flag = self.kwargs.get("flag")
        group = self.kwargs.get("group")
        #偶数
        if flag == "unresolved" and group == "real_name":
            return Question.objects.filter(question_status=False).filter(question_group=True)
        #奇数
        elif flag == "unresolved" and group == "anonymous":
            return Question.objects.filter(question_status=False).filter(question_group=False)
        elif flag == "resolved":
            return Question.objects.filter(question_status=True)
        #未完成
        elif flag == "my-question":
            return Question.objects.filter()
        else:
            return Question.objects.all()

class QuestionCreate(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#1つの質問を取得 + 更新
class QuestionGet(generics.RetrieveUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
#解決や評価に使用
class QuestionUpdate(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#自身の質問のみ編集可能[使用するか未定]
class QuestionUpdateOnlyCreater(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#質問検索機能[フロント側未実装]
class QuestionSearch(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def get_queryset(self):
        keyword = self.kwargs.get("question_content")
        return Question.objects.filter(question_content__icontains=keyword)
 
#Answer
#特定の質問に対する回答をすべて取得
class AnswerGet(generics.ListAPIView):
    serializer_class = AnswerSerializer
    
    def get_queryset(self):
        q_id = self.kwargs.get("question_id")
        return Answer.objects.filter(question_id=q_id)
    
class AnswerCreate(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerUpdate(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

#ok
def getUserEthAddress(request,user_key):
    user = User.objects.get(user_key=user_key)
    return JsonResponse(user.user_eth_address,safe=False)
    
#ポイントUP機能 requestが必要あるのか疑問
@csrf_exempt
def PointUp(request,user_id):
    User.objects.filter(pk=user_id).update(user_point=F('user_point') + 1)
    result = {
            'result':"point up"
        }
    return JsonResponse(result)
@csrf_exempt
def PointDown(request,user_id):
    User.objects.filter(pk=user_id).update(user_point=F('user_point') - 1)
    result = {
            'result':"point down"
        }
    return JsonResponse(result)
#質問閲覧カウント
@csrf_exempt
def AddViews(request,pk):
    Question.objects.filter(pk=pk).update(question_views=F('question_views') + 1)
    result = {
            'result':"add views"
        }
    return JsonResponse(result);  
#回答数増加機能
@csrf_exempt
def AddNumOfAnser(request,pk):
    Question.objects.filter(pk=pk).update(question_number_of_responses=F('question_number_of_responses') + 1)
    result = {
            'result':"add number of answer"
        }
    return JsonResponse(result);  

#質問いいね機能
@csrf_exempt
def Question_like(request):
    json_dict = json.loads(request.body)
    get_user_id = json_dict["user"]
    get_question_id = json_dict['question_id']
    #ユーザーと質問のインスタンス生成
    user = User.objects.get(id=get_user_id)
    question = Question.objects.get(id=get_question_id)
    
    is_like = QuestionLike.objects.filter(user=user).filter(question=question).count()
    # unlike
    if is_like > 0:
        #一度likeしたユーザーを削除 likeモデルを削除
        liking = QuestionLike.objects.get(question=question, user=user)
        liking.delete()
        #質問のいいねを1減らす
        question.question_value -= 1
        question.save()
        context = {
            'result':"いいね取り消し"
        }
        return JsonResponse(context)
    # like
    else:
        question.question_value += 1
        question.save()
        like = QuestionLike()
        #userInstanceが必要
        like.user = user
        like.question = question
        like.save()
        context = {
            'result':"いいね"
        }
        return JsonResponse(context)

#回答いいね機能
@csrf_exempt
def Answer_like(request):
    json_dict = json.loads(request.body)
    get_user_id = json_dict["user"]
    get_answer_id = json_dict['answer_id']
    #ユーザーと質問のインスタンス生成
    user = User.objects.get(id=get_user_id)
    answer = Answer.objects.get(id=get_answer_id)
    
    is_like = AnswerLike.objects.filter(user=user).filter(answer=answer).count()
    # unlike
    if is_like > 0:
        liking = AnswerLike.objects.get(user=user,answer=answer)
        liking.delete()
        answer.answer_value -= 1
        answer.save()
        context = {
            'result':"いいね取り消し"
        }
        return JsonResponse(context)
    # like
    else:
        answer.answer_value += 1
        answer.save()
        like = AnswerLike()
        like.user = user
        like.answer = answer
        like.save()
        context = {
        'result':"いいね"
        }
        return JsonResponse(context)

#質問bad機能
@csrf_exempt
def Question_Bad(request):
    json_dict = json.loads(request.body)
    get_user_id = json_dict["user"]
    get_question_id = json_dict['question_id']
    user = User.objects.get(id=get_user_id)
    question = Question.objects.get(id=get_question_id)
    is_bad = QuestionBad.objects.filter(user=user).filter(question=question).count()
    if is_bad > 0:
        bad = QuestionBad.objects.get(question=question, user=user)
        bad.delete()
        #質問のbadを1減らす
        question.question_bad_value -= 1
        question.save()
        context = {
            'result':"bad取り消し"
        }
        return JsonResponse(context)
    else:
        question.question_bad_value += 1
        question.save()
        bad = QuestionBad()
        bad.user = user
        bad.question = question
        bad.save()
        context = {
            'result':"bad追加"
        }
        return JsonResponse(context)

#回答bad機能
@csrf_exempt
def Answer_Bad(request):
    json_dict = json.loads(request.body)
    get_user_id = json_dict["user"]
    get_answer_id = json_dict['answer_id']
    user = User.objects.get(id=get_user_id)
    answer = Answer.objects.get(id=get_answer_id)
    is_bad = AnswerBad.objects.filter(user=user).filter(answer=answer).count()
    if is_bad > 0:
        bad = AnswerBad.objects.get(user=user,answer=answer)
        bad.delete()
        answer.answer_bad_value -= 1
        answer.save()
        context = {
            'result':"bad取り消し"
        }
        return JsonResponse(context)
    # like
    else:
        answer.answer_bad_value += 1
        answer.save()
        bad = AnswerBad()
        bad.user = user
        bad.answer = answer
        bad.save()
        context = {
            'result':"bad追加"
        }
        return JsonResponse(context)

#メール機能 変更必要
@csrf_exempt
def sendEmail(request):
    json_dict = json.loads(request.body)
    _subject = json_dict["subject"]
    _message = json_dict["message"]
    #ダミーメールアドレスにしたい[余裕があれば]
    _from_email = "22726022@edu.cc.saga-u.ac.jp"
    receipt_user_id = json_dict["receipt_user_id"]
    _user = User.objects.get(id=receipt_user_id)
    #ここが甘い
    receipt_email = _user.user_email
    #送信先は引数で受け取る必要がある また複数に送信することを想定されているためlist型である
    _recipient_list = [
        receipt_email
    ]
    obj = {
        "email": _user.user_email,
    }
    send_mail(_subject, _message, _from_email, _recipient_list, fail_silently=False)
    return  JsonResponse(obj,safe=False)