import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseRedirect

import API.utils as utils
from API.Report.models import PersonModel, GroupModel, DevelopmentDataModel, ReturnDataModel, PerformanceDataModel
from API.Report.serializers import PersonSerializer, GroupSerializer, DevelopmentDataSerializer, ReturnDataSerializer, PerformanceDataSerializer


def user_view(request):
    if request.user.is_authenticated:
        return render(request, 'user.html')
    else:
        return render(request, 'login.html')


def group_view(request):
    if request.user.is_authenticated:
        return render(request, 'group.html')
    else:
        return render(request, 'login.html')


def development_data_view(request):
    if request.user.is_authenticated:
        return render(request, 'report-development-data.html')
    else:
        return render(request, 'login.html')


def performance_data_view(request):
    if request.user.is_authenticated:
        return render(request, 'report-performance-data.html')
    else:
        return render(request, 'login.html')


def return_data_view(request):
    if request.user.is_authenticated:
        return render(request, 'report-return-data.html')
    else:
        return render(request, 'login.html')


def panel_view(request):
    if request.user.is_authenticated:
        return render(request, 'panel.html')
    else:
        return render(request, 'login.html')


def login_view(request):
    return render(request, 'login.html')


def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')


def logout_api(request):
    try:
        logout(request)
    except Exception as e:
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 0, 'msg': '退出失败'})
    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '退出成功'})


def panel_api(request):
    if request.method == 'GET' or request.is_ajax():
        person_count = PersonModel.objects.all().count()
        group_count = GroupModel.objects.all().count()
        time = datetime.datetime.now()
        data = {
            'code': 0,
            'msg': 'success',
            'data': {
                'person_count': person_count,
                'group_count': group_count,
                'time': time
            }
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
def user_login_api(request):
    if request.method == 'POST' or request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is None or username == '' or password is None or password == '':
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 10001, 'msg': '账号或密码不正确'})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '登录成功'})
            else:
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 10001, 'msg': '账号未激活'})
        else:
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 10001, 'msg': '账号或密码不正确'})
        pass
    else:
        return JsonResponse(status=status.HTTP_403_FORBIDDEN, data={'code': 10001, 'msg': '不允许访问'})


@csrf_exempt
def person_group_name_api(request):
    if request.method == 'GET':
        # 获取组别及所有花名
        persons = PersonModel.objects.all()
        groups = GroupModel.objects.all()
        group_arr = [{'id': group.id, 'name': group.group_name} for group in groups]
        username_arr = [{'id': person.id, 'name': person.username} for person in persons]
        data = {
            'code': 0,
            'msg': 'success',
            'count': {
                'group': groups.count(),
                'person': persons.count()
            },
            'data': {
                'group': group_arr,
                'person': username_arr
            }
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


# GET /api/user-data/?id=1&group=1&name=test1&start=2019-09-19&end=2019-09-21&page=1&limit=10
@csrf_exempt
def person_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            username = request.POST.get('username')
            if username is not None and username != '':
                user = PersonModel.objects.filter(username=username)
                if user.__len__() > 0:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '用户已存在'})

            actual_name = request.POST.get('actual_name')
            if actual_name is None and actual_name == '' and actual_name == 'undefined':
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

            group_id = request.POST.get('group_id')
            if group_id is None and group_id == '' and group_id == 'undefined':
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

            user_status = request.POST.get('status')
            if user_status is None and user_status == '' and user_status == 'undefined':
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

            serializer = PersonSerializer(data=request.POST)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '添加成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'edit' and id is not None and id != '' and id != 'undefined':
            person = PersonModel.objects.get(id=id)

            username = request.POST.get('username')
            if username is not None and username != '' and username != 'undefined':
                person.username = username

            actual_name = request.POST.get('actual-name')
            if actual_name is not None and actual_name != '' and actual_name != 'undefined':
                person.actual_name = actual_name

            group_id = request.POST.get('group-id')
            if group_id is not None and group_id != '' and group_id != 'undefined':
                person.group_id = GroupModel.objects.get(id=group_id)

            user_status = request.POST.get('status')
            if user_status is not None and user_status != '' and user_status != 'undefined':
                person.status = user_status
            try:
                person.save()
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '保存成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'delall' and id is not None and id != '' and id != 'undefined':
            id = str(id)[1:-1].split(',')
            for index in id:
                PersonModel.objects.get(id=index).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '全部删除成功'})

        elif operating == 'delone' and id is not None and id != '' and id != 'undefined':
            PersonModel.objects.get(id=id).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '删除成功'})

        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

    if request.method == 'GET':
        # 编辑用户
        event = request.GET.get('event')
        if event is not None and event != '' and event != 'undefined' and event == 'edit':
            id = request.GET.get('id')
            if id is not None and id != '' and id != 'undefined':
                person = PersonModel.objects.get(id=id)
                group = GroupModel.objects.all()
                search = request.GET.get('search')
                search = eval(search)
                return render(request, 'user-edit.html', {'person': person, 'group': group, 'search': search})

        if event is not None and event != '' and event != 'undefined' and event == 'add':
            search = request.GET.get('search')
            search = eval(search)
            group = GroupModel.objects.all()
            return render(request, 'user-add.html', {'group': group, 'search': search})

        # 搜索 数据表格内容
        id = request.GET.get('id')
        name = request.GET.get('name')
        group = request.GET.get('group')
        person_status = request.GET.get('person-status')
        date_range = request.GET.get('date-range')
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        persons = PersonModel.objects.all()

        # 搜索条件
        if id is not None and id != '' and id != 'undefined':
            persons = persons.filter(id=id)

        if person_status is not None and person_status != '' and person_status != 'undefined':
            persons = persons.filter(status=person_status)

        if name is not None and name != '' and name != 'undefined':
            persons = persons.filter(username=name)

        if group is not None and group != '' and group != 'undefined':
            persons = persons.filter(group_id_id=group)

        if date_range is not None and date_range != '' and date_range != 'undefined':
            start = str(date_range).split(' - ')[0]
            end = str(date_range).split(' - ')[1]
            if start is not None and start != '':
                if end is not None and end != '':
                    start = utils.parse_ymd(start + ' 00:00:00')
                    end = utils.parse_ymd(end + ' 23:59:59')
                    persons = persons.filter(date_joined__range=(start, end))

        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            persons = persons.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            persons = persons.order_by('data_time').order_by('-id')
        serializer = PersonSerializer(persons, many=True)
        rows = []
        for item in persons:
            if item.status is None:
                person_status = '未设置'
            elif item.status is False:
                person_status = '老员工'
            else:
                person_status = '新员工'

            rows.append({
                "id": item.id,
                "username": item.username,
                "actual_name": item.actual_name,
                "status": person_status,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %I:%M:%S'),
                'group_name': item.group_id.group_name
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': persons.count(),
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


# GET /api/group-data/?id=1&start=2019-09-19&end=2019-09-21
@csrf_exempt
def group_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            group_name = request.POST.get('group_name')
            if group_name is not None and group_name != '':
                group = GroupModel.objects.filter(group_name=group_name)
                if group.__len__() > 0:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '组别已存在'})
                serializer = GroupSerializer(data=request.POST)
                try:
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '添加成功'})
                except Exception as e:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'delone' and id is not None and id != '' and id != 'undefined':
            GroupModel.objects.get(id=id).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '删除成功'})

        elif operating == 'delall' and id is not None and id != '' and id != 'undefined':
            id = str(id)[1:-1].split(',')
            for index in id:
                GroupModel.objects.get(id=index).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '全部删除成功'})

        elif operating == 'edit' and id is not None and id != '' and id != 'undefined':
            group = GroupModel.objects.get(id=id)
            group_name = request.POST.get('group_name')
            if group_name is not None and group_name != '' and group_name != 'undefined':
                group.group_name = group_name
                try:
                    group.save()
                except Exception as e:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '保存失败'})
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '保存成功'})

        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

    if request.method == 'GET':
        # 搜索 数据表格内容
        id = request.GET.get('id')
        date_range = request.GET.get('date-range')
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        groups = GroupModel.objects.all().order_by('-id')

        if id is not None and id != '' and id != 'undefined':
            groups = groups.filter(id=id)

        if date_range is not None and date_range != '' and date_range != 'undefined':
            start = str(date_range).split(' - ')[0]
            end = str(date_range).split(' - ')[1]
            if start is not None and start != '':
                if end is not None and end != '':
                    start = utils.parse_ymd(start + ' 00:00:00')
                    end = utils.parse_ymd(end + ' 23:59:59')
                    groups = groups.filter(date_joined__range=(start, end))

        if page is not None and page != '' or limit is not None and limit != '':
            groups = groups.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            groups = groups.order_by('data_time').order_by('-id')

        rows = []
        for item in groups:
            rows.append({
                "id": item.id,
                'group_name': item.group_name,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %I:%M:%S'),
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': groups.count(),
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
def development_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            serializer = DevelopmentDataSerializer(data=request.POST)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '添加成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})
        elif operating == 'edit' and id is not None and id != '' and id != 'undefined':
            development_data = DevelopmentDataModel.objects.get(id=id)
            person_id = request.POST.get('person_id')
            new_volume = request.POST.get('new_volume')
            new_customer_volume = request.POST.get('new_customer_volume')
            success_opening_volume = request.POST.get('success_opening_volume')
            business_introduction_volume = request.POST.get('business_introduction_volume')
            answer_question_volume = request.POST.get('answer_question_volume')
            contract_pay_volume = request.POST.get('contract_pay_volume')
            quality_error_volume = request.POST.get('quality_error_volume')
            data_time = request.POST.get('data_time')

            if person_id is not None and person_id != '' and person_id != 'undefined':
                development_data.person_id = PersonModel.objects.get(id=person_id)

            if new_volume is not None and new_volume != 'undefined':
                if new_volume == '':
                    development_data.new_volume = None
                else:
                    development_data.new_volume = new_volume

            if new_customer_volume is not None and new_customer_volume != 'undefined':
                if new_customer_volume == '':
                    development_data.new_customer_volume = None
                else:
                    development_data.new_customer_volume = new_customer_volume

            if success_opening_volume is not None and success_opening_volume != 'undefined':
                if success_opening_volume == '':
                    development_data.success_opening_volume = None
                else:
                    development_data.success_opening_volume = success_opening_volume

            if business_introduction_volume is not None and business_introduction_volume != 'undefined':
                if business_introduction_volume == '':
                    development_data.business_introduction_volume = None
                else:
                    development_data.business_introduction_volume = business_introduction_volume

            if answer_question_volume is not None and answer_question_volume != 'undefined':
                if answer_question_volume == '':
                    development_data.answer_question_volume = None
                else:
                    development_data.answer_question_volume = answer_question_volume

            if contract_pay_volume is not None and contract_pay_volume != 'undefined':
                if contract_pay_volume == '':
                    development_data.contract_pay_volume = None
                else:
                    development_data.contract_pay_volume = contract_pay_volume

            if quality_error_volume is not None and quality_error_volume != 'undefined':
                if quality_error_volume == '':
                    development_data.quality_error_volume = None
                else:
                    development_data.quality_error_volume = quality_error_volume

            if data_time is not None and data_time != '' and data_time != 'undefined':
                development_data.data_time = data_time

            try:
                development_data.save()
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '保存成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'delone' and id is not None and id != '' and id != 'undefined':
            DevelopmentDataModel.objects.get(id=id).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '删除成功'})
        elif operating == 'delall' and id is not None and id != '' and id != 'undefined':
            id = str(id)[1:-1].split(',')
            for index in id:
                DevelopmentDataModel.objects.get(id=index).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '全部删除成功'})
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

    if request.method == 'GET':
        event = request.GET.get('event')
        if event is not None and event != '' and event != 'undefined' and event == 'edit':
            id = request.GET.get('id')
            if id is not None and id != '' and id != 'undefined':
                development_data = DevelopmentDataModel.objects.get(id=id)
                search = request.GET.get('search')
                search = eval(search)
                return render(request, 'report-development-data-edit.html', {'development_data': development_data, 'search': search})
        if event is not None and event != '' and event != 'undefined' and event == 'add':
            search = request.GET.get('search')
            search = eval(search)
            return render(request, 'report-development-data-add.html', {'search': search})

        # 搜索 数据表格内容
        person_id = request.GET.get('person_id')
        group_id = request.GET.get('group_id')
        date_range = request.GET.get('date_range')
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        development_data = DevelopmentDataModel.objects.all()

        # 搜索条件
        if person_id is not None and person_id != '' and person_id != 'undefined':
            development_data = development_data.filter(person_id=person_id)

        if group_id is not None and group_id != '' and group_id != 'undefined':
            persons = PersonModel.objects.filter(group_id=group_id)
            development_data = development_data.filter(person_id__in=persons)

        if date_range is not None and date_range != '' and date_range != 'undefined':
            start = str(date_range).split(' - ')[0]
            end = str(date_range).split(' - ')[1]
            if start is not None and start != '':
                if end is not None and end != '':
                    start = utils.parse_ymd(start + ' 00:00:00')
                    end = utils.parse_ymd(end + ' 23:59:59')
                    development_data = development_data.filter(data_time__range=(start, end))

        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            development_data = development_data.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            development_data = development_data.order_by('data_time').order_by('-id')
        rows = []
        for item in development_data:
            rows.append({
                "id": item.id,
                "person_name": item.person_id.username,
                "group_name": item.person_id.group_id.group_name,
                "new_volume": item.new_volume,
                "new_customer_volume": item.new_customer_volume,
                "success_opening_volume": item.success_opening_volume,
                "business_introduction_volume": item.business_introduction_volume,
                "answer_question_volume": item.answer_question_volume,
                "contract_pay_volume": item.contract_pay_volume,
                "quality_error_volume": item.quality_error_volume,
                "data_time": item.data_time,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %I:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': development_data.count(),
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
def return_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            serializer = ReturnDataSerializer(data=request.POST)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '添加成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})
        elif operating == 'edit' and id is not None and id != '' and id != 'undefined':
            return_data = ReturnDataModel.objects.get(id=id)
            person_id = request.POST.get('person_id')
            return_visit_volume = request.POST.get('return_visit_volume')
            success_opening_volume = request.POST.get('success_opening_volume')
            business_introduction_volume = request.POST.get('business_introduction_volume')
            answer_question_volume = request.POST.get('answer_question_volume')
            contract_pay_volume = request.POST.get('contract_pay_volume')
            quality_error_volume = request.POST.get('quality_error_volume')
            data_time = request.POST.get('data_time')

            if person_id is not None and person_id != '' and person_id != 'undefined':
                return_data.person_id = PersonModel.objects.get(id=person_id)

            if return_visit_volume is not None and return_visit_volume != 'undefined':
                if return_visit_volume == '':
                    return_data.return_visit_volume = None
                else:
                    return_data.return_visit_volume = return_visit_volume

            if success_opening_volume is not None and success_opening_volume != 'undefined':
                if success_opening_volume == '':
                    return_data.success_opening_volume = None
                else:
                    return_data.success_opening_volume = success_opening_volume

            if business_introduction_volume is not None and business_introduction_volume != 'undefined':
                if business_introduction_volume == '':
                    return_data.business_introduction_volume = None
                else:
                    return_data.business_introduction_volume = business_introduction_volume

            if answer_question_volume is not None and answer_question_volume != 'undefined':
                if answer_question_volume == '':
                    return_data.answer_question_volume = None
                else:
                    return_data.answer_question_volume = answer_question_volume

            if contract_pay_volume is not None and contract_pay_volume != 'undefined':
                if contract_pay_volume == '':
                    return_data.contract_pay_volume = None
                else:
                    return_data.contract_pay_volume = contract_pay_volume

            if quality_error_volume is not None and quality_error_volume != 'undefined':
                if quality_error_volume == '':
                    return_data.quality_error_volume = None
                else:
                    return_data.quality_error_volume = quality_error_volume

            if data_time is not None and data_time != '' and data_time != 'undefined':
                return_data.data_time = data_time
            try:
                return_data.save()
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '保存成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'delone' and id is not None and id != '' and id != 'undefined':
            ReturnDataModel.objects.get(id=id).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '删除成功'})
        elif operating == 'delall' and id is not None and id != '' and id != 'undefined':
            id = str(id)[1:-1].split(',')
            for index in id:
                ReturnDataModel.objects.get(id=index).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '全部删除成功'})
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

    if request.method == 'GET':
        event = request.GET.get('event')
        if event is not None and event != '' and event != 'undefined' and event == 'edit':
            id = request.GET.get('id')
            if id is not None and id != '' and id != 'undefined':
                return_data = ReturnDataModel.objects.get(id=id)
                search = request.GET.get('search')
                search = eval(search)
                return render(request, 'report-return-data-edit.html', {'return_data': return_data, 'search': search})
        if event is not None and event != '' and event != 'undefined' and event == 'add':
            search = request.GET.get('search')
            search = eval(search)
            return render(request, 'report-return-data-add.html', {'search': search})

        # 搜索 数据表格内容
        person_id = request.GET.get('person_id')
        group_id = request.GET.get('group_id')
        date_range = request.GET.get('date_range')
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        return_data = ReturnDataModel.objects.all()

        # 搜索条件
        if person_id is not None and person_id != '' and person_id != 'undefined':
            return_data = return_data.filter(person_id=person_id)

        if group_id is not None and group_id != '' and group_id != 'undefined':
            persons = PersonModel.objects.filter(group_id=group_id)
            return_data = return_data.filter(person_id__in=persons)

        if date_range is not None and date_range != '' and date_range != 'undefined':
            start = str(date_range).split(' - ')[0]
            end = str(date_range).split(' - ')[1]
            if start is not None and start != '':
                if end is not None and end != '':
                    start = utils.parse_ymd(start + ' 00:00:00')
                    end = utils.parse_ymd(end + ' 23:59:59')
                    return_data = return_data.filter(data_time__range=(start, end))

        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            return_data = return_data.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            return_data = return_data.order_by('data_time').order_by('-id')
        rows = []
        for item in return_data:
            rows.append({
                "id": item.id,
                "person_name": item.person_id.username,
                "group_name": item.person_id.group_id.group_name,
                "return_visit_volume": item.return_visit_volume,
                "success_opening_volume": item.success_opening_volume,
                "business_introduction_volume": item.business_introduction_volume,
                "answer_question_volume": item.answer_question_volume,
                "contract_pay_volume": item.contract_pay_volume,
                "quality_error_volume": item.quality_error_volume,
                "data_time": item.data_time,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %I:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': return_data.count(),
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
def performance_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            serializer = PerformanceDataSerializer(data=request.POST)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '添加成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'edit' and id is not None and id != '' and id != 'undefined':
            performance_data = PerformanceDataModel.objects.get(id=id)
            person_id = request.POST.get('person_id')
            new_addition_volume = request.POST.get('new_addition_volume')
            talkable_volume = request.POST.get('talkable_volume')
            work_customer_volume = request.POST.get('work_customer_volume')
            transaction_volume = request.POST.get('transaction_volume')
            data_time = request.POST.get('data_time')

            if person_id is not None and person_id != '' and person_id != 'undefined':
                performance_data.person_id = PersonModel.objects.get(id=person_id)

            if new_addition_volume is not None and new_addition_volume != 'undefined':
                if new_addition_volume == '':
                    performance_data.new_addition_volume = None
                else:
                    performance_data.new_addition_volume = new_addition_volume

            if talkable_volume is not None and talkable_volume != 'undefined':
                if talkable_volume == '':
                    performance_data.talkable_volume = None
                else:
                    performance_data.talkable_volume = talkable_volume

            if work_customer_volume is not None and work_customer_volume != 'undefined':
                if work_customer_volume == '':
                    performance_data.work_customer_volume = None
                else:
                    performance_data.work_customer_volume = work_customer_volume

            if transaction_volume is not None and transaction_volume != 'undefined':
                if transaction_volume == '':
                    performance_data.transaction_volume = None
                else:
                    performance_data.transaction_volume = transaction_volume

            if data_time is not None and data_time != '' and data_time != 'undefined':
                performance_data.data_time = data_time
            try:
                performance_data.save()
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '保存成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'delone' and id is not None and id != '' and id != 'undefined':
            PerformanceDataModel.objects.get(id=id).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '删除成功'})
        elif operating == 'delall' and id is not None and id != '' and id != 'undefined':
            id = str(id)[1:-1].split(',')
            for index in id:
                PerformanceDataModel.objects.get(id=index).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '全部删除成功'})
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

    if request.method == 'GET':
        event = request.GET.get('event')
        if event is not None and event != '' and event != 'undefined' and event == 'edit':
            id = request.GET.get('id')
            if id is not None and id != '' and id != 'undefined':
                performance_data = PerformanceDataModel.objects.get(id=id)
                search = request.GET.get('search')
                search = eval(search)
                return render(request, 'report-performance-data-edit.html', {'performance_data': performance_data, 'search': search})
        if event is not None and event != '' and event != 'undefined' and event == 'add':
            search = request.GET.get('search')
            search = eval(search)
            return render(request, 'report-performance-data-add.html', {'search': search})

        # 搜索 数据表格内容
        person_id = request.GET.get('person_id')
        group_id = request.GET.get('group_id')
        date_range = request.GET.get('date_range')
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        performance_data = PerformanceDataModel.objects.all()

        # 搜索条件
        if person_id is not None and person_id != '' and person_id != 'undefined':
            performance_data = performance_data.filter(person_id=person_id)

        if group_id is not None and group_id != '' and group_id != 'undefined':
            persons = PersonModel.objects.filter(group_id=group_id)
            performance_data = performance_data.filter(person_id__in=persons)

        if date_range is not None and date_range != '' and date_range != 'undefined':
            start = str(date_range).split(' - ')[0]
            end = str(date_range).split(' - ')[1]
            if start is not None and start != '':
                if end is not None and end != '':
                    start = utils.parse_ymd(start + ' 00:00:00')
                    end = utils.parse_ymd(end + ' 23:59:59')
                    performance_data = performance_data.filter(data_time__range=(start, end))

        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            performance_data = performance_data.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            performance_data = performance_data.order_by('data_time').order_by('-id')
        rows = []
        for item in performance_data:
            rows.append({
                "id": item.id,
                "person_name": item.person_id.username,
                "group_name": item.person_id.group_id.group_name,
                "new_addition_volume": item.new_addition_volume,
                "talkable_volume": item.talkable_volume,
                "work_customer_volume": item.work_customer_volume,
                "transaction_volume": item.transaction_volume,
                "data_time": item.data_time,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %I:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': performance_data.count(),
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)
