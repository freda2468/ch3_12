from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict


def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET["cName"]
        print(cName)
        resultList = students.objects.filter(cName__contains=cName)
    else:
        resultList = students.objects.all()

    errorMessage=""
    if not resultList:
        errorMessage="無此資料"
    # for data in resultList:       
    #     print(model_to_dict(data))     #此段為練習用

    # return HttpResponse("hello!")
    return render(request,"search_list.html", locals())
from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去除前後空白
        print(site_search)
        #一個關鍵字、搜尋一個欄位
        # resultList = students.objects.filter(cName__contains=site_search)
        #一個關鍵字、搜尋多個欄位
        # resultList = students.objects.filter(
        #     Q(cName__contains=site_search)|
        #     Q(cBirthday__contains=site_search)|
        #     Q(cEmail__contains=site_search)|
        #     Q(cPhone__contains=site_search)|
        #     Q(cAddr__contains=site_search)
        # )
        #多個關鍵字、搜尋多個欄位
        keywords = site_search.split() #切割
        print(keywords)
        # resultList=[]
        q_object = Q()
        for keyword in keywords:
            q_object.add(Q(cName__contains=keyword), Q.OR)
            q_object.add(Q(cBirthday__contains=keyword), Q.OR)
            q_object.add(Q(cEmail__contains=keyword), Q.OR)
            q_object.add(Q(cPhone__contains=keyword), Q.OR)
            q_object.add(Q(cAddr__contains=keyword), Q.OR)
        resultList = students.objects.filter(q_object)

    else:
        resultList = students.objects.all().order_by("cID")
    dataCount = len(resultList)
    status=True
    errorMessage=""
    if not resultList:
        status = False
        errorMessage="無此資料"
    # 分頁設定，每頁顯示3筆
    paginator = Paginator(resultList,3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number) #根據取得page_number，得到對應頁數的資料
    # page_obj 包含該頁資料的物件
    # page_obj.object_list:該頁的資料
    # page_obj.has_next, page_obj.has_previous:是否有下一頁或上一頁
    # page_obj.next_page_number, page_obj.previous_page_number #上一頁、下一頁頁碼
    # page_obj.number 目前的頁碼
    # page_obj.paginator.num_pages:總頁數

    # print(dataCount)
    # return HttpResponse("hello!")
    return render(request,"index.html", locals())

from django.shortcuts import redirect #用來轉址
def post(request):
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr = request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        # orm
        add = students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr) #要看models.py
        add.save()
        # return HttpResponse("hello!")
        return redirect('/index/')
    else:
        return render(request,"post.html", locals())
    
def edit(request,id=None):
        print(f"id={id}")
        if request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # orm
            update = students.objects.get(cID=id)
            update.cName = cName
            update.cSex = cSex
            update.cBirthday = cBirthday
            update.cEmail = cEmail
            update.cPhone = cPhone
            update.cAddr = cAddr
            update.save()
            # return HttpResponse("hello!")
            return redirect('/index/')
        else:
            obj_data = students.objects.get(cID=id)
            print(model_to_dict(obj_data))
            return render(request,"edit.html", locals()) 
        
def delete(request,id=None):
    print(f"id={id}")
    if request.method == "POST":
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        # return HttpResponse("hello!")
        return redirect('/index/')
    else: 
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        return render(request,"delete.html", locals()) 
    
##############################################################
# web api
from django.http import JsonResponse
def getallitems(request):
    resultListObject = students.objects.all().order_by("cID")
    # for data in resultListObject:
    #    print(model_to_dict(data))
    # queerySet->object 轉成 list->dict
    resultListObject = list(resultListObject.values())
    print(resultListObject)
    # return HttpResponse("hello!")
    return JsonResponse(resultListObject, safe=False)

def getitem(request, id=None):
    print(f"id={id}")
    resultListObject = students.objects.filter(cID=id)
    if not resultListObject.exists():
        return JsonResponse({"message":"無資料"}, safe=False)
    resultListObject = list(resultListObject.values())
    print(resultListObject)
    # return HttpResponse("hello!")
    return JsonResponse(resultListObject, safe=False)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def createItem(request):
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print("GET......................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday}"+
                f",cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print("POST......................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday}"+
                f",cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
    except:
        return JsonResponse({"message":"缺少資料"}, safe=False)
    
    try:    
        add = students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        return JsonResponse({"message":"新增成功"}, safe=False)
    except:
        return JsonResponse({"message":"新增失敗"}, safe=False)

@csrf_exempt
def updateItem(request,id=None):
    print(id)
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print("GET...........................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday}"+
            f",cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print("POST...........................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday}"+
            f",cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")  
    except:
        return JsonResponse({"message":"缺少資料"}, safe=False)
    try:
        #orm
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cBirthday = cBirthday
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        return JsonResponse({"message":"更新成功"}, safe=False)
    except:
        return JsonResponse({"message":"更新失敗"}, safe=False)
    # return HttpResponse("hello!")


@csrf_exempt
def deleteItem(request,id=None):
    print(id)
    try:
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        return JsonResponse({"message":"刪除成功"}, safe=False)
    except:
        return JsonResponse({"message":"刪除失敗"}, safe=False)
    # return HttpResponse("hello!")

            
            
    