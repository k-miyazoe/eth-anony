from django.urls import path
from . import views
from .views import *

name="api"

urlpatterns = [
    #User
    path('users/', UserList.as_view()),
    path('get-user/<slug:group>', UserGet.as_view()),
    path('create-user/',UserCreate.as_view()),
    path('users/<pk>', UserRetrieveUpdate.as_view()),
    path('user-delete/<pk>/', UserDelete.as_view()),
    #user_keyでユーザー情報を取得
    path('user-eth-address/<slug:user_key>',views.getUserEthAddress),
    
    #Question
    path('get-question/<slug:flag>/<slug:group>', QuestionList.as_view()),
    path('get-question/<pk>', QuestionGet.as_view()),
    path('create-question/', QuestionCreate.as_view()),
    path('update-question/<pk>', QuestionUpdate.as_view()),
    #閲覧数追加
    path('add-views-question/<pk>', views.AddViews),
    #回答数追加
    path('add-num-answer/<pk>',views.AddNumOfAnser),
    #閲覧回数追加
    # path('search-question/<slug:flag>', QuestionSearch.as_view()),
    
    #Answer
    path('get-answer/<int:question_id>', AnswerGet.as_view()),
    path('create-answer/', AnswerCreate.as_view()),
    #bestanswer処理など
    path('update-answer/<pk>', AnswerUpdate.as_view()),
    
    #Point
    path('point-up/<int:user_id>', views.PointUp),
    path('point-down/<int:user_id>', views.PointDown),
    
    #Like
    path('question-like/', views.Question_like),
    path('answer-like/', views.Answer_like),
    
    #Bad
    path('question-bad/', views.Question_Bad),
    path('answer-bad/', views.Answer_Bad),
    
    #Email
    path('send-email/',views.sendEmail)
    
    #WEB3
    #path('create-eth-address/', views.createEtherAddress),
]