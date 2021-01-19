from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_exptlem import models
from django_exptlem.models import Employee
from django.core.paginator import Paginator
import json


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        isRight = False
        user_info = json.loads(request.body)
        for i in Employee.objects.all():
            if i.name == user_info.get('name') and i.password == user_info.get('password'):
                isRight = True
        if isRight == True:
            return JsonResponse({'state': 200, 'isTrue': True})
        else:
            return JsonResponse({'state': 200, 'isTrue': False})
    else:
        return HttpResponse('请求方式出错！！！')


# /getEmployees ---post /分页
def get_employees_list(request):
    if request.method == "POST":
        pagesize = int(json.loads(request.body).get('pagesize'))
        pagenum = int(json.loads(request.body).get('pagenum'))
        employees = []
        for i in Employee.objects.all():
            employees.append(
                {'id': i.id, 'name': i.name, 'password': i.password, 'address': str(i.address), 'isworking': i.isworking,
                 'department': i.department, 'tel': i.tel})
        paginator = Paginator(Employee.objects.all(), pagesize)
        page = paginator.page(pagenum)
        # paginator_data={'currentPage':page.number,'total':paginator.num_pages,'page_data':page.object_list}
        paginator_data=[]
        for item in page:
            paginator_data.append(
                {'id': item.id, 'name': item.name, 'password': item.password, 'address': str(item.address),
                 'isworking': item.isworking,
                 'department': item.department, 'tel': item.tel})

        res = {'state': 200, 'data': employees,'paginator_data':paginator_data}
        return JsonResponse(res)


# 添加员工
# /insertEmployess ---post
def insert_employees(req):
    if req.method == "POST":
        postBody = req.body
        json_result = json.loads(postBody)
        # 插入数据方式一
        # info={"username":u,"sex":e,"email":e}
        # models.Employee.objects.create(**info)
        # ---------表中插入数据方式二
        models.Employee.objects.create(
            name=json_result.get('name'),
            password=json_result.get('password'),
            address=json_result.get('address'),
            isworking=json_result.get('isworking'),
            department=json_result.get('department'),
            tel=json_result.get('tel')
        )
        return HttpResponse('数据插入成功！')

def update_employess(request):
        if request.method == 'POST':
            postBody = request.body
            result = json.loads(postBody)
        employess_list = []
        for info in Employee.objects.all():
            employess_list.append(
                {'id': info.id, 'name': info.name, 'password': info.password, 'address': str(info.address)})
        for i in employess_list:
            if result.get('id') == i.get('id'):
                current_employess = Employee.objects.get(id=i.get('id'))
                current_employess.name = result.get('name')
                current_employess.password = result.get('password')
                current_employess.address = result.get('address')
                current_employess.isworking = result.get('isworking')
                current_employess.department = result.get('department')
                current_employess.tel = result.get('tel')
                current_employess.save()
        return HttpResponse('修改成功！')

def delete_employess(request):
        if request.method == 'GET':
            id = int(request.GET.get('id'))
        if Employee.objects is not None:
            for i in Employee.objects.all():
                if i.id == id:
                    try:
                        Employee.objects.get(id=i.id).delete()
                        return HttpResponse('删除成功！')
                    except ValueError as e:
                        return HttpResponse('未查询到此条记录！', e)
