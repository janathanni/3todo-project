from django.shortcuts import render, redirect
from todo.models import Todo, DoneDays
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
import datetime

# 나중에 시간 날 때 클래스뷰로 리팩터링 필요

# todo_read


@login_required(login_url='common:login')
def todo(request):
    queryset = None
    is_all_done = False
    context = {}
    if request.method == "GET":
        # user = request.user
        # if not user.agree_terms or not user.agree_marketing:
        #     return redirect("common:social_signup_complete")
        # else:

        now = datetime.datetime.now()
        date_now = datetime.date(now.year, now.month, now.day)
        date_str = f"{now.year}/{now.month}/{now.day}"
        # 오늘 날짜의 일들 가져오기, 만든 순서대로 order
        queryset = Todo.objects.filter(
            user=request.user, create_date=date_now).order_by('create_date')

        # 오늘 며칠 째 달성했는지 보여주기
        done_days = DoneDays.objects.filter(
            user=request.user).exclude(day=date_now).count() + 1

        # todo 레코드 세 개의 is_done attribute가 True라면 is_all_done True로 설정.
        if queryset.count() == 3:
            for query in queryset:
                if query.is_done == False:
                    break

            # for문을 통해 다 돌렸을 때, 즉 query.is_done들이 다 True라면 실행
            else:
                is_all_done = True

                # 쿼리를 통해 일을 다 해낸 오늘을 기록했는지 확인
                # get 하면 오류 떠서 filter로 처리
                done_days_query = DoneDays.objects.filter(
                    user=request.user, day=date_now)
                # 쿼리에 해당하는 값이 없다면 해낸 날을 create
                if not done_days_query:
                    DoneDays.objects.create(user=request.user, day=date_now)

    context = {
        "today": date_str,  # 오늘날짜
        "todo_list": queryset,  # 할일목록
        "is_all_done": is_all_done,  # 일들을 다 했는지
        "done_days": done_days  # 며칠째 일들을 해왔는지
    }

    return render(request, "todo/todo.html", context)

# 오늘 외의 해낸 날들을 보여주기


@login_required(login_url='common:login')
def donelist(request):
    # 1) DoneDays 모델에서 어느 날 했는지 확인해오기
    # 2) DoneDays.objects.filter(user = request.user).exclude(day__startswith = date_now).order_by(day)
    # 3) for문 + enumerate 이용해서 일차, 한일들 가져오기 .
    # 4) day 꺼내서 Todo.objects.filter(user = request.user, day__startswith = day) 해서 일 가져오기

    done_days = DoneDays.objects.filter(user=request.user).order_by('day')
    # 날짜들 가져오기.
    done_todos_with_day = OrderedDict()
    # todo들 가져오기
    for i, done_day in enumerate(done_days):
        # 해당 일자의 todo들
        done_todos = [query.todo for query in Todo.objects.filter(
            user=request.user, create_date=done_day.day)]
        done_todos_with_day[f'{i + 1}'] = done_todos

    # forloop.counter 사용해도 될지도.. 
    done_todos_with_day_recent = OrderedDict(
        reversed(list(done_todos_with_day.items())))
    return render(request, "todo/donelist.html", context={'done_todos_with_day': done_todos_with_day, 'done_todos_with_day_recent': done_todos_with_day_recent})


# todo_create
@login_required(login_url='common:login')
def add_todo(request):
    if request.method == "POST":
        # todo가 공백이 아니라면 정상적으로 todo에 등록
        todo = request.POST["todo"].strip()
        if todo:
            now = datetime.datetime.now()
            date_now = datetime.date(now.year, now.month, now.day)
            Todo.objects.create(user=request.user, todo=todo,
                                is_done=False, create_date=date_now)

    return redirect('todo:todo')

# todo_update


@login_required(login_url='common:login')
def update_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    is_done = request.POST.get('is_done')

    # input 체크박스가 체크 되어있다면 todo 레코드에 is_done attribute를 True로 설정하고 저장
    if is_done == 'on':
        is_done = True

    else:
        is_done = False

    todo.is_done = is_done
    todo.save()

    return redirect('todo:todo')

# todo_delete


@login_required(login_url='common:login')
def delete_todo(request, todo_id):
    if request.method == "POST":
        query = Todo.objects.get(id=todo_id)
        query.delete()

    return redirect('todo:todo')
