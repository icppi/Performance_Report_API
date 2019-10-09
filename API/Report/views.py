import datetime
import json

import numpy as np
from API.exception_logger import logger
from API.exception_decor import exception

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseRedirect

import API.utils as utils
from API.Report.models import PersonModel, GroupModel, DevelopmentDataModel, ReturnDataModel, PerformanceDataModel, HighSeasDataModel, TransferPerformanceDataModel
from API.Report.serializers import PersonSerializer, GroupSerializer, DevelopmentDataSerializer, ReturnDataSerializer, PerformanceDataSerializer, HighSeasDataSerializer, TransferPerformanceDataSerializer


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


def statistical_rate_view(request):
    if request.user.is_authenticated:
        return render(request, 'statistical-report.html')
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


def transfer_performance_data_view(request):
    if request.user.is_authenticated:
        return render(request, 'report-transfer-performance-data.html')
    else:
        return render(request, 'login.html')


def return_data_view(request):
    if request.user.is_authenticated:
        return render(request, 'report-return-data.html')
    else:
        return render(request, 'login.html')


def high_seas_data_view(request):
    if request.user.is_authenticated:
        return render(request, 'report-highseas-data.html')
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
    else:
        return redirect("/index/")
        # return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '退出成功'})


@exception(logger)
def panel_api(request):
    if request.method == 'GET' or request.is_ajax():
        performance_data = PerformanceDataModel.objects.all()
        return_data = ReturnDataModel.objects.all()
        development_data = DevelopmentDataModel.objects.all()
        high_seas_data = HighSeasDataModel.objects.all()

        high_seas_count = high_seas_data.count()
        person_count = PersonModel.objects.all().count()
        group_count = GroupModel.objects.all().count()

        development_count = development_data.count()
        return_count = return_data.count()
        performance_count = performance_data.count()

        yesterday_development_data = development_data.filter(data_time=utils.before_n_day(1))
        yesterday_development_new_volume_list = [item.new_volume for item in yesterday_development_data if item.new_volume is not None]
        yesterday_development_new_volume = np.sum(yesterday_development_new_volume_list)

        yesterday_development_contract_pay_volume_list = [item.contract_pay_volume for item in yesterday_development_data if item.contract_pay_volume is not None]
        yesterday_development_contract_pay_volume = np.sum(yesterday_development_contract_pay_volume_list)

        yesterday_development_success_opening_volume_list = [item.success_opening_volume for item in yesterday_development_data if item.success_opening_volume is not None]
        yesterday_development_success_opening_volume = np.sum(yesterday_development_success_opening_volume_list)
        yesterday_development_business_introduction_volume_list = [item.business_introduction_volume for item in yesterday_development_data if item.business_introduction_volume is not None]
        yesterday_development_business_introduction_volume = np.sum(yesterday_development_business_introduction_volume_list)

        if yesterday_development_success_opening_volume is None or yesterday_development_success_opening_volume == 0:
            yesterday_development_business_introduction_rate_day = 0.0
        else:
            yesterday_development_business_introduction_rate_day = round((yesterday_development_business_introduction_volume / float(yesterday_development_success_opening_volume)), 2)

        yesterday_return_data = return_data.filter(data_time=utils.before_n_day(1))
        yesterday_return_return_volume_list = [item.return_visit_volume for item in yesterday_return_data if item.return_visit_volume is not None]
        yesterday_return_return_volume = np.sum(yesterday_return_return_volume_list)

        yesterday_performance_data = performance_data.filter(data_time=utils.before_n_day(1))
        yesterday_performance_transaction_volume_list = [item.transaction_volume for item in yesterday_performance_data if item.transaction_volume is not None]
        yesterday_performance_transaction_volume = np.sum(yesterday_performance_transaction_volume_list)

        yesterday_seas_data = high_seas_data.filter(data_time=utils.before_n_day(1))
        yesterday_seas_volume_list = [item.high_seas_volume for item in yesterday_seas_data if item.high_seas_volume is not None]
        yesterday_seas_volume = np.sum(yesterday_seas_volume_list)

        yesterday_transaction_volume_all = int(yesterday_development_new_volume) + int(yesterday_return_return_volume) + int(yesterday_seas_volume)
        if yesterday_transaction_volume_all is None or yesterday_transaction_volume_all == 0:
            yesterday_transaction_rate_day = 0.0
        else:
            yesterday_transaction_rate_day = round((yesterday_performance_transaction_volume / float(yesterday_transaction_volume_all)), 2)

        development_success_opening_volume_list_all = [item.success_opening_volume for item in development_data if item.success_opening_volume is not None]
        development_success_opening_volume_all = np.sum(development_success_opening_volume_list_all)
        development_business_introduction_volume_list_all = [item.business_introduction_volume for item in development_data if item.business_introduction_volume is not None]
        development_business_introduction_volume_all = np.sum(development_business_introduction_volume_list_all)

        if development_success_opening_volume_all is None or development_success_opening_volume_all == 0:
            development_business_introduction_rate_all = 0.0
        else:
            development_business_introduction_rate_all = round((development_business_introduction_volume_all / float(development_success_opening_volume_all)), 2)

        development_new_volume_all = [item.new_volume for item in development_data if item.new_volume is not None]
        development_new_volume_all = np.sum(development_new_volume_all)

        development_transaction_value_list = [item.transaction_volume for item in performance_data if item.transaction_volume is not None and item.source == 0]
        development_transaction_volume_all = np.sum(development_transaction_value_list, axis=0)

        development_new_customer_volume_list = [item.new_customer_volume for item in development_data if item.new_customer_volume is not None]
        development_new_customer_volume_all = np.sum(development_new_customer_volume_list, axis=0)

        development_pay_volume_list = [item.contract_pay_volume for item in development_data if item.contract_pay_volume is not None]
        development_pay_volume_all = np.sum(development_pay_volume_list, axis=0)

        return_return_transaction_value_list = [item.transaction_volume for item in performance_data if item.transaction_volume is not None and item.source == 1]
        return_return_transaction_volume_all = np.sum(return_return_transaction_value_list, axis=0)

        return_return_visit_volume = [item.return_visit_volume for item in return_data if item.return_visit_volume]
        return_return_visit_volume_all = np.sum(return_return_visit_volume, axis=0)

        return_contract_pay_volume = [item.contract_pay_volume for item in return_data if item.contract_pay_volume]
        return_contract_pay_volume_all = np.sum(return_contract_pay_volume, axis=0)

        return_success_opening_volume_list_all = [item.success_opening_volume for item in return_data if item.success_opening_volume is not None]
        return_success_opening_volume_all = np.sum(return_success_opening_volume_list_all)

        return_business_introduction_volume_list_all = [item.business_introduction_volume for item in return_data if item.business_introduction_volume is not None]
        return_business_introduction_volume_all = np.sum(return_business_introduction_volume_list_all)

        if return_success_opening_volume_all is None or return_success_opening_volume_all == 0:
            return_business_introduction_rate_all = 0.0
        else:
            return_business_introduction_rate_all = round((return_business_introduction_volume_all / float(return_success_opening_volume_all)), 2)

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'code': 0,
            'msg': 'success',
            'data': {
                'sys': {
                    'person_count': person_count,
                    'group_count': group_count,
                    'development_count': development_count,
                    'return_count': return_count,
                    'performance_count': performance_count,
                    'high_seas_count': high_seas_count,
                    'time': time
                },
                'panel': {
                    'yesterday_development_new_volume': str(int(yesterday_development_new_volume)),
                    'yesterday_return_return_volume': str(int(yesterday_return_return_volume)),
                    'yesterday_seas_volume': str(int(yesterday_seas_volume)),
                    'yesterday_development_contract_pay_volume': str(int(yesterday_development_contract_pay_volume)),
                    'yesterday_performance_transaction_volume': str(int(yesterday_performance_transaction_volume)),
                    'yesterday_development_business_introduction_rate_day': str(yesterday_development_business_introduction_rate_day) + '%',
                    'yesterday_transaction_rate_day': str(yesterday_transaction_rate_day) + '%',

                    'development_new_volume_all': str(int(development_new_volume_all)),
                    'development_transaction_volume_all': str(int(development_transaction_volume_all)),
                    'development_new_customer_volume_all': str(int(development_new_customer_volume_all)),
                    'development_pay_volume_all': str(int(development_pay_volume_all)),
                    'development_business_introduction_rate_all': str(development_business_introduction_rate_all) + '%',

                    'return_return_visit_volume_all': str(int(return_return_visit_volume_all)),
                    'return_contract_pay_volume_all': str(int(return_contract_pay_volume_all)),
                    'return_return_transaction_volume_all': str(int(return_return_transaction_volume_all)),
                    'return_business_introduction_rate_all': str(return_business_introduction_rate_all) + '%',
                }
            }
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
@exception(logger)
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
@exception(logger)
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
@exception(logger)
def person_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            username = request.POST.get('username')
            # if username is not None and username != '':
            #     user = PersonModel.objects.filter(username=username)
            #     if user.__len__() > 0:
            #         return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '用户已存在'})
            if username is None and username == '' and username == 'undefined':
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

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
            print(person.status)
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
            if start is not None and start != '' and end is not None and end != '':
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                persons = persons.filter(date_joined__range=(start, end))

        person_count = persons.count()
        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            persons = persons.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            persons = persons.order_by('data_time').order_by('-id')
        rows = []
        for item in persons:
            if item.status is None:
                person_status = '未设置'
            elif item.status == 0:
                person_status = '老员工'
            elif item.status == 1:
                person_status = '新员工'
            else:
                person_status = '离职'
            if item.actual_name is None or item.actual_name == 'None':
                actual_name = ''
            else:
                actual_name = item.actual_name

            rows.append({
                "id": item.id,
                "username": item.username,
                "actual_name": actual_name,
                "status": person_status,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                'group_name': item.group_id.group_name
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': person_count,
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


# GET /api/group-data/?id=1&start=2019-09-19&end=2019-09-21
@csrf_exempt
@exception(logger)
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
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                groups = groups.filter(date_joined__range=(start, end))

        group_count = groups.count()
        if page is not None and page != '' or limit is not None and limit != '':
            groups = groups.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            groups = groups.order_by('data_time').order_by('-id')

        rows = []
        for item in groups:
            rows.append({
                "id": item.id,
                'group_name': item.group_name,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': group_count,
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
@exception(logger)
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
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                development_data = development_data.filter(data_time__range=(start, end))
        development_data_count = development_data.count()
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
                "new_volume": utils.check_none(item.new_volume),
                "new_customer_volume": utils.check_none(item.new_customer_volume),
                "success_opening_volume": utils.check_none(item.success_opening_volume),
                "business_introduction_volume": utils.check_none(item.business_introduction_volume),
                "answer_question_volume": utils.check_none(item.answer_question_volume),
                "contract_pay_volume": utils.check_none(item.contract_pay_volume),
                "quality_error_volume": utils.check_none(item.quality_error_volume),
                "data_time": utils.check_none(item.data_time),
                "date_joined": item.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': development_data_count,
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
@exception(logger)
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
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                return_data = return_data.filter(data_time__range=(start, end))
        return_data_count = return_data.count()
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
                "return_visit_volume": utils.check_none(item.return_visit_volume),
                "success_opening_volume": utils.check_none(item.success_opening_volume),
                "business_introduction_volume": utils.check_none(item.business_introduction_volume),
                "answer_question_volume": utils.check_none(item.answer_question_volume),
                "contract_pay_volume": utils.check_none(item.contract_pay_volume),
                "quality_error_volume": utils.check_none(item.quality_error_volume),
                "data_time": item.data_time,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': return_data_count,
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
@exception(logger)
def high_seas_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            serializer = HighSeasDataSerializer(data=request.POST)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '添加成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})
        elif operating == 'edit' and id is not None and id != '' and id != 'undefined':
            high_seas_data = HighSeasDataModel.objects.get(id=id)
            person_id = request.POST.get('person_id')
            high_seas_volume = request.POST.get('high_seas_volume')
            success_opening_volume = request.POST.get('success_opening_volume')
            business_introduction_volume = request.POST.get('business_introduction_volume')
            answer_question_volume = request.POST.get('answer_question_volume')
            contract_pay_volume = request.POST.get('contract_pay_volume')
            quality_error_volume = request.POST.get('quality_error_volume')
            data_time = request.POST.get('data_time')

            if person_id is not None and person_id != '' and person_id != 'undefined':
                high_seas_data.person_id = PersonModel.objects.get(id=person_id)

            if high_seas_volume is not None and high_seas_volume != 'undefined':
                if high_seas_volume == '':
                    high_seas_data.high_seas_volume = None
                else:
                    high_seas_data.high_seas_volume = high_seas_volume

            if success_opening_volume is not None and success_opening_volume != 'undefined':
                if success_opening_volume == '':
                    high_seas_data.success_opening_volume = None
                else:
                    high_seas_data.success_opening_volume = success_opening_volume

            if business_introduction_volume is not None and business_introduction_volume != 'undefined':
                if business_introduction_volume == '':
                    high_seas_data.business_introduction_volume = None
                else:
                    high_seas_data.business_introduction_volume = business_introduction_volume

            if answer_question_volume is not None and answer_question_volume != 'undefined':
                if answer_question_volume == '':
                    high_seas_data.answer_question_volume = None
                else:
                    high_seas_data.answer_question_volume = answer_question_volume

            if contract_pay_volume is not None and contract_pay_volume != 'undefined':
                if contract_pay_volume == '':
                    high_seas_data.contract_pay_volume = None
                else:
                    high_seas_data.contract_pay_volume = contract_pay_volume

            if quality_error_volume is not None and quality_error_volume != 'undefined':
                if quality_error_volume == '':
                    high_seas_data.quality_error_volume = None
                else:
                    high_seas_data.quality_error_volume = quality_error_volume

            if data_time is not None and data_time != '' and data_time != 'undefined':
                high_seas_data.data_time = data_time
            try:
                high_seas_data.save()
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '保存成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'delone' and id is not None and id != '' and id != 'undefined':
            HighSeasDataModel.objects.get(id=id).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '删除成功'})
        elif operating == 'delall' and id is not None and id != '' and id != 'undefined':
            id = str(id)[1:-1].split(',')
            for index in id:
                HighSeasDataModel.objects.get(id=index).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '全部删除成功'})
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

    if request.method == 'GET':
        event = request.GET.get('event')
        if event is not None and event != '' and event != 'undefined' and event == 'edit':
            id = request.GET.get('id')
            if id is not None and id != '' and id != 'undefined':
                return_data = HighSeasDataModel.objects.get(id=id)
                search = request.GET.get('search')
                search = eval(search)
                return render(request, 'report-highseas-data-edit.html', {'return_data': return_data, 'search': search})
        if event is not None and event != '' and event != 'undefined' and event == 'add':
            search = request.GET.get('search')
            search = eval(search)
            return render(request, 'report-highseas-data-add.html', {'search': search})

        # 搜索 数据表格内容
        person_id = request.GET.get('person_id')
        group_id = request.GET.get('group_id')
        date_range = request.GET.get('date_range')
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        high_seas_data = HighSeasDataModel.objects.all()

        # 搜索条件
        if person_id is not None and person_id != '' and person_id != 'undefined':
            high_seas_data = high_seas_data.filter(person_id=person_id)

        if group_id is not None and group_id != '' and group_id != 'undefined':
            persons = PersonModel.objects.filter(group_id=group_id)
            high_seas_data = high_seas_data.filter(person_id__in=persons)

        if date_range is not None and date_range != '' and date_range != 'undefined':
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                high_seas_data = high_seas_data.filter(data_time__range=(start, end))
        high_seas_data_count = high_seas_data.count()
        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            high_seas_data = high_seas_data.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            high_seas_data = high_seas_data.order_by('data_time').order_by('-id')
        rows = []
        for item in high_seas_data:
            rows.append({
                "id": item.id,
                "person_name": item.person_id.username,
                "group_name": item.person_id.group_id.group_name,
                "high_seas_volume": utils.check_none(item.high_seas_volume),
                "success_opening_volume": utils.check_none(item.success_opening_volume),
                "business_introduction_volume": utils.check_none(item.business_introduction_volume),
                "answer_question_volume": utils.check_none(item.answer_question_volume),
                "contract_pay_volume": utils.check_none(item.contract_pay_volume),
                "quality_error_volume": utils.check_none(item.quality_error_volume),
                "data_time": item.data_time,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': high_seas_data_count,
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
@exception(logger)
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
            data_source = request.POST.get('data_source')
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

            if data_source is not None and data_source != 'undefined':
                if data_source == '':
                    performance_data.source = None
                else:
                    performance_data.source = data_source

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
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                performance_data = performance_data.filter(data_time__range=(start, end))
        performance_data_count = performance_data.count()
        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            performance_data = performance_data.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            performance_data = performance_data.order_by('data_time').order_by('-id')
        rows = []
        for item in performance_data:
            if not item.source:
                source = '新增数据'
            elif item.source == 1:
                source = '回访数据'
            else:
                source = '公海数据'
            rows.append({
                "id": item.id,
                "person_name": item.person_id.username,
                "group_name": item.person_id.group_id.group_name,
                "new_addition_volume": utils.check_none(item.new_addition_volume),
                "talkable_volume": utils.check_none(item.talkable_volume),
                "work_customer_volume": utils.check_none(item.work_customer_volume),
                "transaction_volume": utils.check_none(item.transaction_volume),
                "data_source": source,
                "data_time": item.data_time,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': performance_data_count,
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


@csrf_exempt
@exception(logger)
def transfer_performance_data_api(request):
    if request.method == 'POST':
        operating = request.POST.get('operating')
        id = request.POST.get('id')
        if operating == 'add':
            serializer = TransferPerformanceDataSerializer(data=request.POST)
            try:
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '添加成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'edit' and id is not None and id != '' and id != 'undefined':
            transfer_performance_data = TransferPerformanceDataModel.objects.get(id=id)
            person_id = request.POST.get('person_id')
            development_volume = request.POST.get('development_volume')
            transfer_volume = request.POST.get('transfer_volume')
            data_time = request.POST.get('data_time')

            if person_id is not None and person_id != '' and person_id != 'undefined':
                transfer_performance_data.person_id = PersonModel.objects.get(id=person_id)

            if development_volume is not None and development_volume != 'undefined':
                if development_volume == '':
                    transfer_performance_data.development_volume = None
                else:
                    transfer_performance_data.development_volume = development_volume

            if transfer_volume is not None and transfer_volume != 'undefined':
                if transfer_volume == '':
                    transfer_performance_data.transfer_volume = None
                else:
                    transfer_performance_data.transfer_volume = transfer_volume

            if data_time is not None and data_time != '' and data_time != 'undefined':
                transfer_performance_data.data_time = data_time
            try:
                transfer_performance_data.save()
                return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '保存成功'})
            except Exception as e:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': 'POST参数错误'})

        elif operating == 'delone' and id is not None and id != '' and id != 'undefined':
            TransferPerformanceDataModel.objects.get(id=id).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '删除成功'})
        elif operating == 'delall' and id is not None and id != '' and id != 'undefined':
            id = str(id)[1:-1].split(',')
            for index in id:
                TransferPerformanceDataModel.objects.get(id=index).delete()
            return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': '全部删除成功'})
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

    if request.method == 'GET':
        event = request.GET.get('event')
        if event is not None and event != '' and event != 'undefined' and event == 'edit':
            id = request.GET.get('id')
            if id is not None and id != '' and id != 'undefined':
                transfer_performance_data = TransferPerformanceDataModel.objects.get(id=id)
                search = request.GET.get('search')
                search = eval(search)
                return render(request, 'report-transfer-performance-data-edit.html', {'transfer_performance_data': transfer_performance_data, 'search': search})
        if event is not None and event != '' and event != 'undefined' and event == 'add':
            search = request.GET.get('search')
            search = eval(search)
            return render(request, 'report-transfer-performance-data-add.html', {'search': search})

        # 搜索 数据表格内容
        person_id = request.GET.get('person_id')
        group_id = request.GET.get('group_id')
        date_range = request.GET.get('date_range')
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        transfer_performance_data = TransferPerformanceDataModel.objects.all()

        # 搜索条件
        if person_id is not None and person_id != '' and person_id != 'undefined':
            transfer_performance_data = transfer_performance_data.filter(person_id=person_id)

        if group_id is not None and group_id != '' and group_id != 'undefined':
            persons = PersonModel.objects.filter(group_id=group_id)
            transfer_performance_data = transfer_performance_data.filter(person_id__in=persons)

        if date_range is not None and date_range != '' and date_range != 'undefined':
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                transfer_performance_data = transfer_performance_data.filter(data_time__range=(start, end))
        transfer_performance_data_count = transfer_performance_data.count()
        if page is not None and page != '' or limit is not None and limit != '' and page != 'undefined' and limit != 'undefined':
            transfer_performance_data = transfer_performance_data.order_by('data_time').order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        else:
            transfer_performance_data = transfer_performance_data.order_by('data_time').order_by('-id')
        rows = []
        for item in transfer_performance_data:
            rows.append({
                "id": item.id,
                "person_name": item.person_id.username,
                "group_name": item.person_id.group_id.group_name,
                "development_volume": utils.check_none(item.development_volume),
                "transfer_volume": utils.check_none(item.transfer_volume),
                "data_time": item.data_time,
                "date_joined": item.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            })

        data = {
            'code': 0,
            'msg': 'success',
            'count': transfer_performance_data_count,
            'data': rows
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


# 报表统计
@exception(logger)
def data_conversion_rate(request):
    if request.method == 'GET':
        # 新增数据
        id = request.GET.get('id')
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        obj = request.GET.get('obj')
        types = request.GET.get('types')
        date_range = request.GET.get('date-range')

        # 判断数据类型(新增/回访) 必选
        if types is not None and types != '' and types != 'undefined':
            if types == 'development':
                same_period_data = data = DevelopmentDataModel.objects.all()
            elif types == 'return':
                same_period_data = data = ReturnDataModel.objects.all()
            elif types == 'highseas':
                same_period_data = data = HighSeasDataModel.objects.all()
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})

        same_period_performance_data = performance_data = PerformanceDataModel.objects.all()

        # 过滤时间
        if date_range is not None and date_range != '' and date_range != 'undefined':
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except Exception as e:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                days = utils.getEveryDay(start, end).__len__()
                start = utils.parse_ymd(start + ' 00:00:00')
                end = utils.parse_ymd(end + ' 23:59:59')
                if types is not None and types != 'undefined':
                    # 当前选择日期数据
                    data = data.filter(data_time__range=(start, end))
                    performance_data = performance_data.filter(data_time__range=(start, end))
                    # 同期对比数据
                    same_period_data = same_period_data.filter(data_time__range=(utils.from_before_n_day(start, days), utils.from_before_n_day(end, days)))
                    same_period_performance_data = same_period_performance_data.filter(data_time__range=(utils.from_before_n_day(start, days), utils.from_before_n_day(end, days)))
        else:
            if types is not None and types != 'undefined':
                # 若未选择日期则默认前7天数据
                date_range = '{} - {}'.format(utils.before_n_day(8), utils.before_n_day(2))
                data = data.filter(data_time__range=(utils.before_n_day(8), utils.before_n_day(2)))
                performance_data = performance_data.filter(data_time__range=(utils.before_n_day(8), utils.before_n_day(2)))
                # 同期对比数据
                same_period_data = same_period_data.filter(data_time__range=(utils.before_n_day(15), utils.before_n_day(9)))
                same_period_performance_data = same_period_performance_data.filter(data_time__range=(utils.before_n_day(15), utils.before_n_day(9)))

        # if data.__len__() <= 0 or performance_data.__len__() <= 0:
        if data.__len__() <= 0:
            return JsonResponse(status=status.HTTP_200_OK, data={
                'code': 200,
                'msg': '该时间段内没有数据哦！'
            })

        if id is not None and id != '' and id != 'undefined' and id != '[]':
            id_list = str(id)[1:-1].split(',')
        else:
            if obj == 'group':
                id_list = [group.id for group in GroupModel.objects.all()]
            else:
                id_list = [person.id for person in PersonModel.objects.all()]

        # 当前选择日期数据
        data_list = []
        performance_data_list = []

        # 同期数据
        same_period_data_list = []
        same_period_performance_data_list = []

        if obj is not None and obj != '' and obj != 'undefined':
            # 取整组的数据
            if obj == 'group':
                for index in id_list:
                    person = PersonModel.objects.filter(group_id=index)
                    # 当前日期整租数据
                    data_list.append(data.filter(person_id__in=person))
                    performance_data_list.append(performance_data.filter(person_id__in=person))
                    # 同期整租数据
                    same_period_data_list.append(same_period_data.filter(person_id__in=person))
                    same_period_performance_data_list.append(same_period_performance_data.filter(person_id__in=person))
            # 取人员的数据
            if obj == 'person':
                for index in id_list:
                    # 当前日期人员数据
                    data_list.append(data.filter(person_id=index))
                    performance_data_list.append(performance_data.filter(person_id=index))
                    # 同期人员数据
                    same_period_data_list.append(same_period_data.filter(person_id=index))
                    same_period_performance_data_list.append(same_period_performance_data.filter(person_id=index))

        item_list = []
        if types == 'development':
            # 同期数据
            same_period_rate_list = []
            if same_period_data_list.__len__() > 0 or same_period_performance_data_list.__len__() > 0:
                same_period_list_count = 0
                for same_period_data_items in same_period_data_list:
                    if same_period_data_items.__len__() <= 0:
                        continue
                    same_period_dev_data_lists = []
                    same_period_per_data_lists = []

                    for same_period_per_item in same_period_performance_data_list[same_period_list_count]:
                        if same_period_per_item.source == 0:
                            same_period_transaction_volume = same_period_per_item.transaction_volume
                        else:
                            same_period_transaction_volume = 0

                        if same_period_transaction_volume is None:
                            same_period_transaction_volume = 0
                        same_period_per_data_lists.append(same_period_transaction_volume)

                    for same_period_data_item in same_period_data_items:
                        same_period_new_volume = same_period_data_item.new_volume
                        same_period_new_customer_volume = same_period_data_item.new_customer_volume
                        same_period_success_opening_volume = same_period_data_item.success_opening_volume
                        same_period_business_introduction_volume = same_period_data_item.business_introduction_volume
                        same_period_answer_question_volume = same_period_data_item.answer_question_volume
                        same_period_contract_pay_volume = same_period_data_item.contract_pay_volume
                        same_period_quality_error_volume = same_period_data_item.quality_error_volume
                        if same_period_new_volume is None:
                            same_period_new_volume = 0
                        if same_period_new_customer_volume is None:
                            same_period_new_customer_volume = 0
                        if same_period_success_opening_volume is None:
                            same_period_success_opening_volume = 0
                        if same_period_business_introduction_volume is None:
                            same_period_business_introduction_volume = 0
                        if same_period_answer_question_volume is None:
                            same_period_answer_question_volume = 0
                        if same_period_contract_pay_volume is None:
                            same_period_contract_pay_volume = 0
                        if same_period_quality_error_volume is None:
                            same_period_quality_error_volume = 0
                        same_period_dev_data_list = [same_period_new_volume, same_period_new_customer_volume, same_period_success_opening_volume, same_period_business_introduction_volume, same_period_answer_question_volume, same_period_contract_pay_volume, same_period_quality_error_volume]
                        same_period_dev_data_lists.append(same_period_dev_data_list)

                    # 求和
                    same_period_data_sum = np.sum(same_period_dev_data_lists, axis=0)
                    same_period_per_data_sum = np.sum(same_period_per_data_lists)

                    # 求各项rate
                    if same_period_data_sum[1] is None or same_period_data_sum[1] == 0:
                        same_period_success_opening_rate = 0.0
                    else:
                        same_period_success_opening_rate = round((same_period_data_sum[2] / float(same_period_data_sum[1])) * 100, 2)  # 成功开场率

                    if same_period_data_sum[2] is None or same_period_data_sum[2] == 0:
                        same_period_business_introduction_rate = 0.0
                    else:
                        same_period_business_introduction_rate = round((same_period_data_sum[3] / float(same_period_data_sum[2])) * 100, 2)  # 业务介绍成功率

                    if same_period_data_sum[3] is None or same_period_data_sum[3] == 0:
                        same_period_answer_question_rate = 0.0
                    else:
                        same_period_answer_question_rate = round((same_period_data_sum[4] / float(same_period_data_sum[3])) * 100, 2)  # 解答问题成功率

                    if same_period_data_sum[4] is None or same_period_data_sum[4] == 0:
                        same_period_contract_pay_rate = 0.0
                    else:
                        same_period_contract_pay_rate = round((same_period_data_sum[5] / float(same_period_data_sum[4])) * 100, 2)  # 约定付款率

                    if same_period_data_sum[0] is None or same_period_data_sum[0] == 0:
                        same_period_transaction_rate = 0.0
                    else:
                        same_period_transaction_rate = round((same_period_per_data_sum / float(same_period_data_sum[0])) * 100, 2)  # 成交率

                    # 存储同期百分比
                    same_period_rate = [
                        same_period_data_sum[0],
                        same_period_data_sum[1],
                        same_period_success_opening_rate,
                        same_period_business_introduction_rate,
                        same_period_answer_question_rate,
                        same_period_contract_pay_rate,
                        same_period_transaction_rate,
                        same_period_per_data_sum
                    ]
                    same_period_rate_list.append(same_period_rate)
                    same_period_list_count += 1

            # 现选日期数据
            list_count = 0
            for data_items in data_list:
                if data_items.__len__() <= 0:
                    continue
                dev_data_lists = []
                per_data_lists = []

                for per_item in performance_data_list[list_count]:
                    if per_item.source == 0:
                        transaction_volume = per_item.transaction_volume
                    else:
                        transaction_volume = 0
                    if transaction_volume is None:
                        transaction_volume = 0
                    per_data_lists.append(transaction_volume)

                for data_item in data_items:
                    new_volume = data_item.new_volume
                    new_customer_volume = data_item.new_customer_volume
                    success_opening_volume = data_item.success_opening_volume
                    business_introduction_volume = data_item.business_introduction_volume
                    answer_question_volume = data_item.answer_question_volume
                    contract_pay_volume = data_item.contract_pay_volume
                    quality_error_volume = data_item.quality_error_volume
                    if new_volume is None:
                        new_volume = 0
                    if new_customer_volume is None:
                        new_customer_volume = 0
                    if success_opening_volume is None:
                        success_opening_volume = 0
                    if business_introduction_volume is None:
                        business_introduction_volume = 0
                    if answer_question_volume is None:
                        answer_question_volume = 0
                    if contract_pay_volume is None:
                        contract_pay_volume = 0
                    if quality_error_volume is None:
                        quality_error_volume = 0
                    dev_data_list = [new_volume, new_customer_volume, success_opening_volume, business_introduction_volume, answer_question_volume, contract_pay_volume, quality_error_volume]
                    dev_data_lists.append(dev_data_list)

                # 求和
                if dev_data_lists.__len__() <= 0:  # 如果该用户没有数据则跳过
                    continue
                data_sum = np.sum(dev_data_lists, axis=0)
                per_data_sum = np.sum(per_data_lists)

                # 求各项rate
                if data_sum[1] is None or data_sum[1] == 0:
                    success_opening_rate = 0.0
                else:
                    success_opening_rate = round((data_sum[2] / float(data_sum[1])) * 100, 2)  # 成功开场率

                if data_sum[2] is None or data_sum[2] == 0:
                    business_introduction_rate = 0.0
                else:
                    business_introduction_rate = round((data_sum[3] / float(data_sum[2])) * 100, 2)  # 业务介绍成功率

                if data_sum[3] is None or data_sum[3] == 0:
                    answer_question_rate = 0.0
                else:
                    answer_question_rate = round((data_sum[4] / float(data_sum[3])) * 100, 2)  # 解答问题成功率

                if data_sum[4] is None or data_sum[4] == 0:
                    contract_pay_rate = 0.0
                else:
                    contract_pay_rate = round((data_sum[5] / float(data_sum[4])) * 100, 2)  # 约定付款率

                if data_sum[0] is None or data_sum[0] == 0:
                    transaction_rate = 0.0
                else:
                    transaction_rate = round((per_data_sum / float(data_sum[0])) * 100, 2)  # 成交率
                new_volume = str(data_sum[0])
                new_customer_volume = str(data_sum[1])
                # 同期数据对比
                if same_period_rate_list.__len__() > 0:
                    res_same_period_new_volume = data_sum[0] - same_period_rate_list[list_count][0]
                    res_same_period_new_customer_volume = data_sum[1] - same_period_rate_list[list_count][1]
                    res_same_period_success_opening_rate = round((success_opening_rate - same_period_rate_list[list_count][2]), 2)
                    res_same_period_business_introduction_rate = round((business_introduction_rate - same_period_rate_list[list_count][3]), 2)
                    res_same_period_answer_question_rate = round((answer_question_rate - same_period_rate_list[list_count][4]), 2)
                    res_same_period_contract_pay_rate = round((contract_pay_rate - same_period_rate_list[list_count][5]), 2)
                    res_same_period_transaction_rate = round((transaction_rate - same_period_rate_list[list_count][6]), 2)
                    res_same_period_per_data_sum = per_data_sum - same_period_rate_list[list_count][7]

                    if res_same_period_new_volume > 0:
                        new_volume = str(data_sum[0]) + '(↑' + str(int(res_same_period_new_volume)) + ')'
                    elif res_same_period_new_volume == 0:
                        new_volume = str(data_sum[0])
                    else:
                        new_volume = str(data_sum[0]) + '(↓' + str(abs(res_same_period_new_volume)) + ')'

                    if res_same_period_new_customer_volume > 0:
                        new_customer_volume = str(data_sum[1]) + '(↑' + str(int(res_same_period_new_customer_volume)) + ')'
                    elif res_same_period_new_customer_volume == 0:
                        new_customer_volume = str(data_sum[1])
                    else:
                        new_customer_volume = str(data_sum[1]) + '(↓' + str(abs(res_same_period_new_customer_volume)) + ')'

                    if res_same_period_success_opening_rate > 0:
                        success_opening_rate = str(success_opening_rate) + '%(↑' + str(res_same_period_success_opening_rate) + '%)'
                    elif res_same_period_success_opening_rate == 0:
                        success_opening_rate = str(success_opening_rate) + '%'
                    else:
                        success_opening_rate = str(success_opening_rate) + '%(↓' + str(abs(res_same_period_success_opening_rate)) + '%)'

                    if res_same_period_business_introduction_rate > 0:
                        business_introduction_rate = str(business_introduction_rate) + '%(↑' + str(res_same_period_business_introduction_rate) + '%)'
                    elif res_same_period_business_introduction_rate == 0:
                        business_introduction_rate = str(business_introduction_rate) + '%'
                    else:
                        business_introduction_rate = str(business_introduction_rate) + '%(↓' + str(abs(res_same_period_business_introduction_rate)) + '%)'

                    if res_same_period_answer_question_rate > 0:
                        answer_question_rate = str(answer_question_rate) + '%(↑' + str(res_same_period_answer_question_rate) + '%)'
                    elif res_same_period_answer_question_rate == 0:
                        answer_question_rate = str(answer_question_rate) + '%'
                    else:
                        answer_question_rate = str(answer_question_rate) + '%(↓' + str(abs(res_same_period_answer_question_rate)) + '%)'

                    if res_same_period_contract_pay_rate > 0:
                        contract_pay_rate = str(contract_pay_rate) + '%(↑' + str(res_same_period_contract_pay_rate) + '%)'
                    elif res_same_period_contract_pay_rate == 0:
                        contract_pay_rate = str(contract_pay_rate) + '%'
                    else:
                        contract_pay_rate = str(contract_pay_rate) + '%(↓' + str(abs(res_same_period_contract_pay_rate)) + '%)'

                    if res_same_period_transaction_rate > 0:
                        transaction_rate = str(transaction_rate) + '%(↑' + str(res_same_period_transaction_rate) + '%)'
                    elif res_same_period_transaction_rate == 0:
                        transaction_rate = str(transaction_rate) + '%'
                    else:
                        transaction_rate = str(transaction_rate) + '%(↓' + str(abs(res_same_period_transaction_rate)) + '%)'

                    if res_same_period_per_data_sum > 0:
                        per_data_sum = str(int(per_data_sum)) + '(↑' + str(int(res_same_period_per_data_sum)) + ')'
                    elif res_same_period_per_data_sum == 0:
                        per_data_sum = str(int(per_data_sum))
                    else:
                        per_data_sum = str(int(per_data_sum)) + '(↓' + str(abs(res_same_period_per_data_sum)) + ')'
                else:
                    transaction_rate = str(transaction_rate) + '%'
                    success_opening_rate = str(success_opening_rate) + '%'
                    business_introduction_rate = str(business_introduction_rate) + '%'
                    contract_pay_rate = str(contract_pay_rate) + '%'
                    answer_question_rate = str(answer_question_rate) + '%'

                res_data = {
                    'date': str(date_range),
                    'new_volume': str(new_volume),
                    'new_customer_volume': str(new_customer_volume),
                    'success_opening_rate': str(success_opening_rate),
                    'business_introduction_rate': str(business_introduction_rate),
                    'answer_question_rate': str(answer_question_rate),
                    'contract_pay_rate': str(contract_pay_rate),
                    'transaction_rate': str(transaction_rate),
                    'per_data_sum': str(per_data_sum),
                }
                if obj == 'group':
                    res_data.setdefault('name', GroupModel.objects.get(id=id_list[list_count]).group_name)
                if obj == 'person':
                    res_data.setdefault('name', PersonModel.objects.get(id=id_list[list_count]).username)
                item_list.append(res_data)
                list_count += 1

            return JsonResponse(status=status.HTTP_200_OK, data={
                'code': 0,
                'msg': 'success',
                'count': item_list.__len__(),
                'data': item_list[(int(page) - 1) * int(limit):int(page) * int(limit)]
            })

        elif types == 'return':
            # 同期数据
            same_period_rate_list = []
            if same_period_data.__len__() > 0 or same_period_performance_data.__len__() > 0:
                same_period_list_count = 0
                for same_period_data_items in same_period_data_list:
                    if same_period_data_items.__len__() <= 0:
                        continue
                    same_period_dev_data_lists = []
                    same_period_per_data_lists = []

                    for same_period_per_item in same_period_performance_data_list[same_period_list_count]:
                        if same_period_per_item.source == 1:
                            same_period_transaction_volume = same_period_per_item.transaction_volume
                        else:
                            same_period_transaction_volume = 0
                        if same_period_transaction_volume is None:
                            same_period_transaction_volume = 0
                        same_period_per_data_lists.append(same_period_transaction_volume)

                    for same_period_data_item in same_period_data_items:
                        same_period_return_visit_volume = same_period_data_item.return_visit_volume
                        same_period_success_opening_volume = same_period_data_item.success_opening_volume
                        same_period_business_introduction_volume = same_period_data_item.business_introduction_volume
                        same_period_answer_question_volume = same_period_data_item.answer_question_volume
                        same_period_contract_pay_volume = same_period_data_item.contract_pay_volume
                        same_period_quality_error_volume = same_period_data_item.quality_error_volume
                        if same_period_return_visit_volume is None:
                            same_period_return_visit_volume = 0
                        if same_period_success_opening_volume is None:
                            same_period_success_opening_volume = 0
                        if same_period_business_introduction_volume is None:
                            same_period_business_introduction_volume = 0
                        if same_period_answer_question_volume is None:
                            same_period_answer_question_volume = 0
                        if same_period_contract_pay_volume is None:
                            same_period_contract_pay_volume = 0
                        if same_period_quality_error_volume is None:
                            same_period_quality_error_volume = 0
                        same_period_dev_data_list = [same_period_return_visit_volume, same_period_success_opening_volume, same_period_business_introduction_volume, same_period_answer_question_volume, same_period_contract_pay_volume, same_period_quality_error_volume]
                        same_period_dev_data_lists.append(same_period_dev_data_list)

                    # 求和
                    same_period_data_sum = np.sum(same_period_dev_data_lists, axis=0)
                    same_period_per_data_sum = np.sum(same_period_per_data_lists)

                    # 求各项rate
                    if same_period_data_sum[0] is None or same_period_data_sum[0] == 0:
                        same_period_success_opening_rate = 0.0
                    else:
                        same_period_success_opening_rate = round((same_period_data_sum[1] / float(same_period_data_sum[0])) * 100, 2)  # 成功开场率

                    if same_period_data_sum[1] is None or same_period_data_sum[1] == 0:
                        same_period_business_introduction_rate = 0.0
                    else:
                        same_period_business_introduction_rate = round((same_period_data_sum[2] / float(same_period_data_sum[1])) * 100, 2)  # 业务介绍成功率

                    if same_period_data_sum[2] is None or same_period_data_sum[2] == 0:
                        same_period_answer_question_rate = 0.0
                    else:
                        same_period_answer_question_rate = round((same_period_data_sum[3] / float(same_period_data_sum[2])) * 100, 2)  # 解答问题成功率

                    if same_period_data_sum[3] is None or same_period_data_sum[3] == 0:
                        same_period_contract_pay_rate = 0.0
                    else:
                        same_period_contract_pay_rate = round((same_period_data_sum[4] / float(same_period_data_sum[3])) * 100, 2)  # 约定付款率

                    if same_period_data_sum[1] is None or same_period_data_sum[1] == 0:
                        same_period_transaction_rate = 0.0
                    else:
                        same_period_transaction_rate = round((same_period_per_data_sum / float(same_period_data_sum[1])) * 100, 2)  # 成交率

                    # 存储同期百分比
                    same_period_rate = [
                        same_period_data_sum[0],
                        same_period_data_sum[1],
                        same_period_success_opening_rate,
                        same_period_business_introduction_rate,
                        same_period_answer_question_rate,
                        same_period_contract_pay_rate,
                        same_period_transaction_rate,
                        same_period_per_data_sum
                    ]
                    same_period_rate_list.append(same_period_rate)
                    same_period_list_count += 1

            list_count = 0
            for data_items in data_list:
                if data_items.__len__() <= 0:
                    continue
                dev_data_lists = []
                per_data_lists = []
                for per_item in performance_data_list[list_count]:
                    if per_item.source == 1:
                        transaction_volume = per_item.transaction_volume
                    else:
                        transaction_volume = 0
                    if transaction_volume is None:
                        transaction_volume = 0
                    per_data_lists.append(transaction_volume)

                for data_item in data_items:
                    return_visit_volume = data_item.return_visit_volume
                    success_opening_volume = data_item.success_opening_volume
                    business_introduction_volume = data_item.business_introduction_volume
                    answer_question_volume = data_item.answer_question_volume
                    contract_pay_volume = data_item.contract_pay_volume
                    quality_error_volume = data_item.quality_error_volume

                    if return_visit_volume is None:
                        return_visit_volume = 0
                    if success_opening_volume is None:
                        success_opening_volume = 0
                    if business_introduction_volume is None:
                        business_introduction_volume = 0
                    if answer_question_volume is None:
                        answer_question_volume = 0
                    if contract_pay_volume is None:
                        contract_pay_volume = 0
                    if quality_error_volume is None:
                        quality_error_volume = 0
                    dev_data_list = [return_visit_volume, success_opening_volume, business_introduction_volume, answer_question_volume, contract_pay_volume, quality_error_volume]
                    dev_data_lists.append(dev_data_list)

                # 求和
                data_sum = np.sum(dev_data_lists, axis=0)
                per_data_sum = np.sum(per_data_lists)

                # 求各项rate
                if data_sum[0] is None or data_sum[0] == 0:
                    success_opening_rate = 0.0
                else:
                    success_opening_rate = round((data_sum[1] / float(data_sum[0]) * 100), 2)  # 成功开场率

                if data_sum[1] is None or data_sum[1] == 0:
                    business_introduction_rate = 0.0
                else:
                    business_introduction_rate = round((data_sum[2] / float(data_sum[1]) * 100), 2)  # 业务介绍成功率

                if data_sum[2] is None or data_sum[2] == 0:
                    answer_question_rate = 0.0
                else:
                    answer_question_rate = round((data_sum[3] / float(data_sum[2]) * 100), 2)  # 解答问题成功率

                if data_sum[3] is None or data_sum[3] == 0:
                    contract_pay_rate = 0.0
                else:
                    contract_pay_rate = round((data_sum[4] / float(data_sum[3]) * 100), 2)  # 约定付款率

                if data_sum[0] is None or data_sum[0] == 0:
                    transaction_rate = 0.0
                else:
                    transaction_rate = round((per_data_sum / float(data_sum[0]) * 100), 2)  # 成交率

                # 同期数据对比
                return_visit_volume = str(data_sum[0])

                if same_period_rate_list.__len__() > 0:
                    res_same_period_return_visit_volume = data_sum[0] - same_period_rate_list[list_count][0]
                    res_same_period_success_opening_rate = round((success_opening_rate - same_period_rate_list[list_count][1]), 2)
                    res_same_period_business_introduction_rate = round((business_introduction_rate - same_period_rate_list[list_count][2]), 2)
                    res_same_period_answer_question_rate = round((answer_question_rate - same_period_rate_list[list_count][3]), 2)
                    res_same_period_contract_pay_rate = round((contract_pay_rate - same_period_rate_list[list_count][4]), 2)
                    res_same_period_transaction_rate = round((transaction_rate - same_period_rate_list[list_count][5]), 2)
                    res_same_period_per_data_sum = per_data_sum - same_period_rate_list[list_count][7]

                    if res_same_period_return_visit_volume > 0:
                        return_visit_volume = str(data_sum[0]) + '(↑' + str(int(res_same_period_return_visit_volume)) + ')'
                    elif res_same_period_return_visit_volume == 0:
                        return_visit_volume = str(data_sum[0])
                    else:
                        return_visit_volume = str(data_sum[0]) + '(↓' + str(abs(res_same_period_return_visit_volume)) + ')'

                    if res_same_period_success_opening_rate > 0:
                        success_opening_rate = str(success_opening_rate) + '%(↑' + str(res_same_period_success_opening_rate) + '%)'
                    elif res_same_period_success_opening_rate == 0:
                        success_opening_rate = str(success_opening_rate) + '%'
                    else:
                        success_opening_rate = str(success_opening_rate) + '%(↓' + str(abs(res_same_period_success_opening_rate)) + '%)'

                    if res_same_period_business_introduction_rate > 0:
                        business_introduction_rate = str(business_introduction_rate) + '%(↑' + str(res_same_period_business_introduction_rate) + '%)'
                    elif res_same_period_business_introduction_rate == 0:
                        business_introduction_rate = str(business_introduction_rate) + '%'
                    else:
                        business_introduction_rate = str(business_introduction_rate) + '%(↓' + str(abs(res_same_period_business_introduction_rate)) + '%)'

                    if res_same_period_answer_question_rate > 0:
                        answer_question_rate = str(answer_question_rate) + '%(↑' + str(res_same_period_answer_question_rate) + '%)'
                    elif res_same_period_answer_question_rate == 0:
                        answer_question_rate = str(answer_question_rate) + '%'
                    else:
                        answer_question_rate = str(answer_question_rate) + '%(↓' + str(abs(res_same_period_answer_question_rate)) + '%)'

                    if res_same_period_contract_pay_rate > 0:
                        contract_pay_rate = str(contract_pay_rate) + '%(↑' + str(res_same_period_contract_pay_rate) + '%)'
                    elif res_same_period_contract_pay_rate == 0:
                        contract_pay_rate = str(contract_pay_rate) + '%'
                    else:
                        contract_pay_rate = str(contract_pay_rate) + '%(↓' + str(abs(res_same_period_contract_pay_rate)) + '%)'

                    if res_same_period_transaction_rate > 0:
                        transaction_rate = str(transaction_rate) + '%(↑' + str(res_same_period_transaction_rate) + '%)'
                    elif res_same_period_transaction_rate == 0:
                        transaction_rate = str(transaction_rate) + '%'
                    else:
                        transaction_rate = str(transaction_rate) + '%(↓' + str(abs(res_same_period_transaction_rate)) + '%)'

                    if res_same_period_per_data_sum > 0:
                        per_data_sum = str(int(per_data_sum)) + '(↑' + str(int(res_same_period_per_data_sum)) + ')'
                    elif res_same_period_per_data_sum == 0:
                        per_data_sum = str(int(per_data_sum))
                    else:
                        per_data_sum = str(int(per_data_sum)) + '(↓' + str(abs(res_same_period_per_data_sum)) + ')'
                else:
                    transaction_rate = str(transaction_rate) + '%'
                    success_opening_rate = str(success_opening_rate) + '%'
                    business_introduction_rate = str(business_introduction_rate) + '%'
                    contract_pay_rate = str(contract_pay_rate) + '%'
                    answer_question_rate = str(answer_question_rate) + '%'

                res_data = {
                    'date': str(date_range),
                    'return_visit_volume': str(return_visit_volume),
                    'success_opening_rate': str(success_opening_rate),
                    'business_introduction_rate': str(business_introduction_rate),
                    'answer_question_rate': str(answer_question_rate),
                    'contract_pay_rate': str(contract_pay_rate),
                    'transaction_rate': str(transaction_rate),
                    'per_data_sum': str(per_data_sum),
                }
                if obj == 'group':
                    res_data.setdefault('name', GroupModel.objects.get(id=id_list[list_count]).group_name)
                if obj == 'person':
                    res_data.setdefault('name', PersonModel.objects.get(id=id_list[list_count]).username)
                item_list.append(res_data)
                list_count += 1
            rows = {
                'code': 0,
                'msg': 'success',
                'count': item_list.__len__(),
                'data': item_list[(int(page) - 1) * int(limit):int(page) * int(limit)]
            }
            return JsonResponse(status=status.HTTP_200_OK, data=rows)

        elif types == 'highseas':
            # 同期数据
            same_period_rate_list = []
            if same_period_data.__len__() > 0 or same_period_performance_data.__len__() > 0:
                same_period_list_count = 0
                for same_period_data_items in same_period_data_list:
                    if same_period_data_items.__len__() <= 0:
                        continue
                    same_period_dev_data_lists = []
                    same_period_per_data_lists = []
                    # 取同期成交量
                    for same_period_per_item in same_period_performance_data_list[same_period_list_count]:
                        if same_period_per_item.source == 2:
                            same_period_transaction_volume = same_period_per_item.transaction_volume
                        else:
                            same_period_transaction_volume = 0
                        if same_period_transaction_volume is None:
                            same_period_transaction_volume = 0
                        same_period_per_data_lists.append(same_period_transaction_volume)

                    for same_period_data_item in same_period_data_items:
                        same_period_return_visit_volume = same_period_data_item.high_seas_volume
                        same_period_success_opening_volume = same_period_data_item.success_opening_volume
                        same_period_business_introduction_volume = same_period_data_item.business_introduction_volume
                        same_period_answer_question_volume = same_period_data_item.answer_question_volume
                        same_period_contract_pay_volume = same_period_data_item.contract_pay_volume
                        same_period_quality_error_volume = same_period_data_item.quality_error_volume
                        if same_period_return_visit_volume is None:
                            same_period_return_visit_volume = 0
                        if same_period_success_opening_volume is None:
                            same_period_success_opening_volume = 0
                        if same_period_business_introduction_volume is None:
                            same_period_business_introduction_volume = 0
                        if same_period_answer_question_volume is None:
                            same_period_answer_question_volume = 0
                        if same_period_contract_pay_volume is None:
                            same_period_contract_pay_volume = 0
                        if same_period_quality_error_volume is None:
                            same_period_quality_error_volume = 0
                        same_period_dev_data_list = [same_period_return_visit_volume, same_period_success_opening_volume, same_period_business_introduction_volume, same_period_answer_question_volume, same_period_contract_pay_volume, same_period_quality_error_volume]
                        same_period_dev_data_lists.append(same_period_dev_data_list)
                    # 求和
                    same_period_data_sum = np.sum(same_period_dev_data_lists, axis=0)
                    same_period_per_data_sum = np.sum(same_period_per_data_lists)
                    # 求各项rate
                    if same_period_data_sum[0] is None or same_period_data_sum[0] == 0:
                        same_period_success_opening_rate = 0.0
                    else:
                        same_period_success_opening_rate = round((same_period_data_sum[1] / float(same_period_data_sum[0])) * 100, 2)  # 成功开场率
                    if same_period_data_sum[1] is None or same_period_data_sum[1] == 0:
                        same_period_business_introduction_rate = 0.0
                    else:
                        same_period_business_introduction_rate = round((same_period_data_sum[2] / float(same_period_data_sum[1])) * 100, 2)  # 业务介绍成功率

                    if same_period_data_sum[2] is None or same_period_data_sum[2] == 0:
                        same_period_answer_question_rate = 0.0
                    else:
                        same_period_answer_question_rate = round((same_period_data_sum[3] / float(same_period_data_sum[2])) * 100, 2)  # 解答问题成功率

                    if same_period_data_sum[3] is None or same_period_data_sum[3] == 0:
                        same_period_contract_pay_rate = 0.0
                    else:
                        same_period_contract_pay_rate = round((same_period_data_sum[4] / float(same_period_data_sum[3])) * 100, 2)  # 约定付款率

                    if same_period_data_sum[1] is None or same_period_data_sum[1] == 0:
                        same_period_transaction_rate = 0.0
                    else:
                        same_period_transaction_rate = round((same_period_per_data_sum / float(same_period_data_sum[1])) * 100, 2)  # 成交率

                    # 存储同期百分比
                    same_period_rate = [
                        same_period_data_sum[0],
                        same_period_data_sum[1],
                        same_period_success_opening_rate,
                        same_period_business_introduction_rate,
                        same_period_answer_question_rate,
                        same_period_contract_pay_rate,
                        same_period_transaction_rate,
                        same_period_per_data_sum
                    ]
                    same_period_rate_list.append(same_period_rate)
                    same_period_list_count += 1
            list_count = 0
            for data_items in data_list:
                if data_items.__len__() <= 0:
                    continue
                dev_data_lists = []
                per_data_lists = []
                for per_item in performance_data_list[list_count]:
                    if per_item.source == 2:
                        transaction_volume = per_item.transaction_volume
                    else:
                        transaction_volume = 0
                    if transaction_volume is None:
                        transaction_volume = 0
                    per_data_lists.append(transaction_volume)

                for data_item in data_items:
                    return_visit_volume = data_item.high_seas_volume
                    success_opening_volume = data_item.success_opening_volume
                    business_introduction_volume = data_item.business_introduction_volume
                    answer_question_volume = data_item.answer_question_volume
                    contract_pay_volume = data_item.contract_pay_volume
                    quality_error_volume = data_item.quality_error_volume

                    if return_visit_volume is None:
                        return_visit_volume = 0
                    if success_opening_volume is None:
                        success_opening_volume = 0
                    if business_introduction_volume is None:
                        business_introduction_volume = 0
                    if answer_question_volume is None:
                        answer_question_volume = 0
                    if contract_pay_volume is None:
                        contract_pay_volume = 0
                    if quality_error_volume is None:
                        quality_error_volume = 0
                    dev_data_list = [return_visit_volume, success_opening_volume, business_introduction_volume, answer_question_volume, contract_pay_volume, quality_error_volume]
                    dev_data_lists.append(dev_data_list)

                # 求和
                data_sum = np.sum(dev_data_lists, axis=0)
                per_data_sum = np.sum(per_data_lists)

                # 求各项rate
                if data_sum[0] is None or data_sum[0] == 0:
                    success_opening_rate = 0.0
                else:
                    success_opening_rate = round((data_sum[1] / float(data_sum[0]) * 100), 2)  # 成功开场率

                if data_sum[1] is None or data_sum[1] == 0:
                    business_introduction_rate = 0.0
                else:
                    business_introduction_rate = round((data_sum[2] / float(data_sum[1]) * 100), 2)  # 业务介绍成功率

                if data_sum[2] is None or data_sum[2] == 0:
                    answer_question_rate = 0.0
                else:
                    answer_question_rate = round((data_sum[3] / float(data_sum[2]) * 100), 2)  # 解答问题成功率

                if data_sum[3] is None or data_sum[3] == 0:
                    contract_pay_rate = 0.0
                else:
                    contract_pay_rate = round((data_sum[4] / float(data_sum[3]) * 100), 2)  # 约定付款率

                if data_sum[0] is None or data_sum[0] == 0:
                    transaction_rate = 0.0
                else:
                    transaction_rate = round((per_data_sum / float(data_sum[0]) * 100), 2)  # 成交率

                # 同期数据对比
                return_visit_volume = str(data_sum[0])

                if same_period_rate_list.__len__() > 0:
                    res_same_period_return_visit_volume = data_sum[0] - same_period_rate_list[list_count][0]
                    res_same_period_success_opening_rate = round((success_opening_rate - same_period_rate_list[list_count][1]), 2)
                    res_same_period_business_introduction_rate = round((business_introduction_rate - same_period_rate_list[list_count][2]), 2)
                    res_same_period_answer_question_rate = round((answer_question_rate - same_period_rate_list[list_count][3]), 2)
                    res_same_period_contract_pay_rate = round((contract_pay_rate - same_period_rate_list[list_count][4]), 2)
                    res_same_period_transaction_rate = round((transaction_rate - same_period_rate_list[list_count][5]), 2)
                    res_same_period_per_data_sum = per_data_sum - same_period_rate_list[list_count][7]

                    if res_same_period_return_visit_volume > 0:
                        return_visit_volume = str(data_sum[0]) + '(↑' + str(int(res_same_period_return_visit_volume)) + ')'
                    elif res_same_period_return_visit_volume == 0:
                        return_visit_volume = str(data_sum[0])
                    else:
                        return_visit_volume = str(data_sum[0]) + '(↓' + str(abs(res_same_period_return_visit_volume)) + ')'

                    if res_same_period_success_opening_rate > 0:
                        success_opening_rate = str(success_opening_rate) + '%(↑' + str(res_same_period_success_opening_rate) + '%)'
                    elif res_same_period_success_opening_rate == 0:
                        success_opening_rate = str(success_opening_rate) + '%'
                    else:
                        success_opening_rate = str(success_opening_rate) + '%(↓' + str(abs(res_same_period_success_opening_rate)) + '%)'

                    if res_same_period_business_introduction_rate > 0:
                        business_introduction_rate = str(business_introduction_rate) + '%(↑' + str(res_same_period_business_introduction_rate) + '%)'
                    elif res_same_period_business_introduction_rate == 0:
                        business_introduction_rate = str(business_introduction_rate) + '%'
                    else:
                        business_introduction_rate = str(business_introduction_rate) + '%(↓' + str(abs(res_same_period_business_introduction_rate)) + '%)'

                    if res_same_period_answer_question_rate > 0:
                        answer_question_rate = str(answer_question_rate) + '%(↑' + str(res_same_period_answer_question_rate) + '%)'
                    elif res_same_period_answer_question_rate == 0:
                        answer_question_rate = str(answer_question_rate) + '%'
                    else:
                        answer_question_rate = str(answer_question_rate) + '%(↓' + str(abs(res_same_period_answer_question_rate)) + '%)'

                    if res_same_period_contract_pay_rate > 0:
                        contract_pay_rate = str(contract_pay_rate) + '%(↑' + str(res_same_period_contract_pay_rate) + '%)'
                    elif res_same_period_contract_pay_rate == 0:
                        contract_pay_rate = str(contract_pay_rate) + '%'
                    else:
                        contract_pay_rate = str(contract_pay_rate) + '%(↓' + str(abs(res_same_period_contract_pay_rate)) + '%)'

                    if res_same_period_transaction_rate > 0:
                        transaction_rate = str(transaction_rate) + '%(↑' + str(res_same_period_transaction_rate) + '%)'
                    elif res_same_period_transaction_rate == 0:
                        transaction_rate = str(transaction_rate) + '%'
                    else:
                        transaction_rate = str(transaction_rate) + '%(↓' + str(abs(res_same_period_transaction_rate)) + '%)'

                    if res_same_period_per_data_sum > 0:
                        per_data_sum = str(int(per_data_sum)) + '(↑' + str(int(res_same_period_per_data_sum)) + ')'
                    elif res_same_period_per_data_sum == 0:
                        per_data_sum = str(int(per_data_sum))
                    else:
                        per_data_sum = str(int(per_data_sum)) + '(↓' + str(abs(res_same_period_per_data_sum)) + ')'
                else:
                    transaction_rate = str(transaction_rate) + '%'
                    success_opening_rate = str(success_opening_rate) + '%'
                    business_introduction_rate = str(business_introduction_rate) + '%'
                    contract_pay_rate = str(contract_pay_rate) + '%'
                    answer_question_rate = str(answer_question_rate) + '%'

                res_data = {
                    'date': str(date_range),
                    'high_seas_volume': str(return_visit_volume),
                    'success_opening_rate': str(success_opening_rate),
                    'business_introduction_rate': str(business_introduction_rate),
                    'answer_question_rate': str(answer_question_rate),
                    'contract_pay_rate': str(contract_pay_rate),
                    'transaction_rate': str(transaction_rate),
                    'per_data_sum': str(per_data_sum),
                }
                if obj == 'group':
                    res_data.setdefault('name', GroupModel.objects.get(id=id_list[list_count]).group_name)
                if obj == 'person':
                    res_data.setdefault('name', PersonModel.objects.get(id=id_list[list_count]).username)
                item_list.append(res_data)
                list_count += 1
            rows = {
                'code': 0,
                'msg': 'success',
                'count': item_list.__len__(),
                'data': item_list[(int(page) - 1) * int(limit):int(page) * int(limit)]
            }
            return JsonResponse(status=status.HTTP_200_OK, data=rows)

        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'code': 10001, 'msg': '参数错误'})


def statistical_echarts_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'statistical-echarts.html')
    else:
        return render(request, 'login.html')


# 默认只选日期 显示各组的数据
@exception(logger)
def statistical_echarts_data(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        obj = request.GET.get('obj')
        date_range = request.GET.get('date-range')

        if id is not None and id != '' and id != 'undefined' and id != '[]':
            id_list = str(id)[1:-1].split(',')
        else:
            if obj == 'group':
                id_list = [group.id for group in GroupModel.objects.all()]
            else:
                id_list = [person.id for person in PersonModel.objects.all()]

        if obj is not None and obj != '' and obj != 'undefined':
            if obj == 'group':
                id_data = GroupModel.objects.filter(id__in=id_list)
                name = [item.group_name for item in id_data]
            if obj == 'person':
                id_data = PersonModel.objects.filter(id__in=id_list)
                name = [item.username for item in id_data]

        if date_range is not None and date_range != '' and date_range != 'undefined':
            try:
                start = str(date_range).split(' - ')[0]
                end = str(date_range).split(' - ')[1]
            except Exception as e:
                start = end = str(date_range)
            if start is not None and start != '' and end is not None and end != '':
                date_list = utils.getEveryDay(start, end)
                if obj == 'person':
                    person_sum_list = []
                    return_sum_data = []
                    for index in id_list:
                        person_sum = []
                        return_sum_list = []
                        for item_date in date_list:
                            development_data = DevelopmentDataModel.objects.filter(data_time=item_date)
                            return_data = ReturnDataModel.objects.filter(data_time=item_date)
                            person_sum.append(int(np.sum([int(item.new_customer_volume) for item in development_data.filter(person_id=index) if item.new_customer_volume is not None], axis=0)))
                            return_sum_list.append(int(np.sum([int(item.return_visit_volume) for item in return_data.filter(person_id=index) if item.return_visit_volume is not None], axis=0)))
                        person_sum_list.append(person_sum)
                        return_sum_data.append(return_sum_list)
                    ret1 = [{'name': name[index],
                             'data': item,
                             'type': 'line',
                             'stack': '总量',
                             'label': {
                                 'normal': {
                                     'show': 'true',
                                     'position': 'top'
                                 }
                             }, } for index, item in enumerate(person_sum_list)]
                    ret2 = [{'name': name[index],
                             'data': item,
                             'type': 'line',
                             'stack': '总量',
                             'label': {
                                 'normal': {
                                     'show': 'true',
                                     'position': 'top'
                                 }
                             }, } for index, item in enumerate(return_sum_data)]
                    ret_data1 = {
                        'legend': name,
                        'xAxis_data': date_list,
                        'series': ret1
                    }
                    ret_data2 = {
                        'legend': name,
                        'xAxis_data': date_list,
                        'series': ret2
                    }
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': 'success', 'data': {'new': ret_data1, 'return': ret_data2}})

                if obj == 'group':
                    sum_data = []
                    return_sum_data = []
                    for index in id_list:
                        sum_list = []
                        return_sum_list = []
                        for item_date in date_list:
                            return_data = ReturnDataModel.objects.filter(data_time=item_date)
                            development_data = DevelopmentDataModel.objects.filter(data_time=item_date)
                            person = PersonModel.objects.filter(group_id=index)
                            sum_list.append(int(np.sum([int(item.new_customer_volume) for item in development_data.filter(person_id__in=person) if item.new_customer_volume is not None], axis=0)))
                            return_sum_list.append(int(np.sum([int(item.return_visit_volume) for item in return_data.filter(person_id__in=person) if item.return_visit_volume is not None], axis=0)))
                        sum_data.append(sum_list)
                        return_sum_data.append(return_sum_list)
                    ret1 = [{'name': name[index],
                             'data': item,
                             'type': 'line',
                             'stack': '总量',
                             'label': {
                                 'normal': {
                                     'show': 'true',
                                     'position': 'top'
                                 }
                             }, } for index, item in enumerate(sum_data)]
                    ret2 = [{'name': name[index],
                             'data': item,
                             'type': 'line',
                             'stack': '总量',
                             'label': {
                                 'normal': {
                                     'show': 'true',
                                     'position': 'top'
                                 }
                             }, } for index, item in enumerate(return_sum_data)]
                    ret_data1 = {
                        'legend': name,
                        'xAxis_data': date_list,
                        'series': ret1
                    }
                    ret_data2 = {
                        'legend': name,
                        'xAxis_data': date_list,
                        'series': ret2
                    }
                    return JsonResponse(status=status.HTTP_200_OK, data={'code': 0, 'msg': 'success', 'data': {'new': ret_data1, 'return': ret_data2}})


def top_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'top.html', context={})
    else:
        return render(request, 'login.html')


@exception(logger)
def top_data_api(request):
    date_range = request.GET.get('date-range')
    num = request.GET.get('num')
    if not num or num == '' or num == 'undefined':
        num = 10
    else:
        num = int(num)

    person_data = PersonModel.objects.all()
    development_data = DevelopmentDataModel.objects.all()
    return_data = ReturnDataModel.objects.all()
    performance_data = PerformanceDataModel.objects.all()
    # 过滤时间
    if date_range is not None and date_range != '' and date_range != 'undefined':
        try:
            start = str(date_range).split(' - ')[0]
            end = str(date_range).split(' - ')[1]
        except:
            start = end = str(date_range)
        if start is not None and start != '' and end is not None and end != '':
            start = utils.parse_ymd(start + ' 00:00:00')
            end = utils.parse_ymd(end + ' 23:59:59')
            development_data = development_data.filter(data_time__range=(start, end))
            return_data = return_data.filter(data_time__range=(start, end))
            performance_data = performance_data.filter(data_time__range=(start, end))
        else:
            development_data = development_data.filter(data_time__range=(utils.before_n_day(8), utils.before_n_day(2)))
            return_data = return_data.filter(data_time__range=(utils.before_n_day(8), utils.before_n_day(2)))
            performance_data = performance_data.filter(data_time__range=(utils.before_n_day(8), utils.before_n_day(2)))
        print(performance_data)

    return_person_dev_list = []
    return_person_return_list = []
    return_person_performance_list = []
    return_person_rate_list = []

    for person in person_data:
        ret_person_dev = {}
        ret_person_return = {}
        ret_person_performance = {}
        ret_person_rate = {}

        person_dev_data_list = [int(item.new_customer_volume) for item in development_data.filter(person_id=person) if item.new_customer_volume is not None and item.new_customer_volume != '']
        person_dev_data = int(np.sum(person_dev_data_list, axis=0))

        person_return_data_list = [int(item.return_visit_volume) for item in return_data.filter(person_id=person) if item.return_visit_volume is not None and item.return_visit_volume != '']
        person_return_data_data = int(np.sum(person_return_data_list, axis=0))

        person_per_data_list = [int(item.transaction_volume) for item in performance_data.filter(person_id=person) if item.transaction_volume is not None and item.transaction_volume != '']
        person_per_data = int(np.sum(person_per_data_list, axis=0))

        person_dev_success_opening_data_list = [int(item.success_opening_volume) for item in development_data.filter(person_id=person) if item.success_opening_volume is not None and item.new_customer_volume != '']
        person_dev_success_opening_data = np.sum(person_dev_success_opening_data_list, axis=0)

        person_dev_business_data_list = [int(item.business_introduction_volume) for item in development_data.filter(person_id=person) if item.business_introduction_volume is not None and item.new_customer_volume != '']
        person_dev_business_data = np.sum(person_dev_business_data_list, axis=0)
        if person_dev_success_opening_data == 0 or person_dev_success_opening_data is None:
            person_dev_business_rate = 0.0
        else:
            person_dev_business_rate = round((person_dev_business_data / person_dev_success_opening_data), 2)

        ret_person_rate['person_name'] = ret_person_dev['person_name'] = ret_person_return['person_name'] = ret_person_performance['person_name'] = person.username
        ret_person_rate['group_name'] = ret_person_dev['group_name'] = ret_person_return['group_name'] = ret_person_performance['group_name'] = person.group_id.group_name
        ret_person_dev['new_addition'] = person_dev_data
        ret_person_rate['business_rate'] = person_dev_business_rate
        ret_person_return['return_value'] = person_return_data_data
        ret_person_performance['transaction_value'] = person_per_data

        return_person_dev_list.append(ret_person_dev)
        return_person_rate_list.append(ret_person_rate)
        return_person_return_list.append(ret_person_return)
        return_person_performance_list.append(ret_person_performance)

    return_person_dev_list = sorted(return_person_dev_list, key=lambda e: e.__getitem__('new_addition'), reverse=True)
    return_person_return_list = sorted(return_person_return_list, key=lambda e: e.__getitem__('return_value'), reverse=True)
    return_person_performance_list = sorted(return_person_performance_list, key=lambda e: e.__getitem__('transaction_value'), reverse=True)
    return_person_rate_list = sorted(return_person_rate_list, key=lambda e: e.__getitem__('business_rate'), reverse=True)

    for index, item in enumerate(return_person_dev_list):
        item['ranking'] = int(index) + 1

    for index, item in enumerate(return_person_return_list):
        item['ranking'] = int(index) + 1

    for index, item in enumerate(return_person_performance_list):
        item['ranking'] = int(index) + 1

    for index, item in enumerate(return_person_rate_list):
        item['business_rate'] = str(item['business_rate']) + '%'
        item['ranking'] = int(index) + 1

    if development_data.__len__() <= 0:
        ret_new = []
    else:
        ret_new = return_person_dev_list[:num]

    if return_data.__len__() <= 0:
        ret_return = []
    else:
        ret_return = return_person_return_list[:num]

    if performance_data.__len__() <= 0:
        ret_transaction = []
    else:
        ret_transaction = return_person_performance_list[:num]

    return JsonResponse(status=status.HTTP_200_OK,
                        data={'code': 0,
                              'msg': 'success',
                              'count': 10,
                              'data':
                                  {
                                      'ret_new': ret_new,
                                      'ret_return': ret_return,
                                      'ret_rate': return_person_rate_list[:num],
                                      'ret_transaction': ret_transaction,
                                  }
                              })
