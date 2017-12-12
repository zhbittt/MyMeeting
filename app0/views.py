from PIL import Image, ImageDraw, ImageFont
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app0.models import *
from io import BytesIO
from django.http import JsonResponse
import random
import json
import datetime
#图片点击   登录  login 原始版本
def login(request):
    if request.is_ajax():

        username = request.POST.get("username")
        password = request.POST.get("password")
        validCode = request.POST.get("validCode")

        login_response = {"is_login": False, "error_msg": None}
        if validCode.upper() == request.session.get("keepValidCode").upper():
            user = UserInfo.objects.filter(name=username,pwd=password )
            if user:
                login_response["is_login"] = True
                request.session["user_id"]=user.first().id
                request.session["user_name"]=user.first().name
            else:
                login_response["error_msg"] = '账号或密码错误'
        else:
            login_response["error_msg"] = '验证码错误'
        return HttpResponse(json.dumps(login_response))
    return render(request, 'login.html')

def get_validCode_img(request):
    '''
    获取验证码图片
    '''
    img = Image.new(mode="RGB" , size=(120,40) ,color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    draw = ImageDraw.Draw(img,"RGB")
    font = ImageFont.truetype('static/font/kumo.ttf',25)

    valid_list=[]
    for i in range(5):

        random_num =str(random.randint(0,9))
        random_lower_zimu =chr(random.randint(65,90))
        random_upper_zimu = chr(random.randint(97,122))

        random_char = random.choice([random_num,random_lower_zimu,random_upper_zimu])
        draw.text([5+i*24,10],random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        valid_list.append(random_char)

    f = BytesIO()
    img.save(f,'png')
    data = f.getvalue()

    valid_str = "".join(valid_list)
    print(valid_str)

    request.session["keepValidCode"]=valid_str

    return HttpResponse(data)

def index(request):
    '''
    会议室主页
    '''
    user_id=request.session.get("user_id")
    if not user_id:
        return redirect('/login/')
    time_choice=Select.time_choices
    return  render(request,'index.html',{"time_choice":time_choice})

def selecting(request):
    '''
    获取会议室数据或添加数据
    '''
    user_id = request.session.get("user_id")
    print("user_id",user_id)
    data = {"state": True, "msg": None, "data": []}
    nowdata = datetime.datetime.now().date()
    if request.method =="GET":

        selectData=request.GET.get("selectData")
        selectData = datetime.datetime.strptime(selectData,"%Y-%m-%d").date()
        if selectData < nowdata:
            raise Exception("不能查询已过期的日期")
        try:

            select_list = Select.objects.filter(data=selectData)
            time_choice = Select.time_choices
            room_list = Room.objects.all()
            for room in room_list:
                row_list=[]
                for tc in time_choice:
                    for sl in select_list:
                        if tc[0] == sl.time and room.id == sl.room_id and sl.data ==selectData:
                            print("111111111111",sl.user_id,user_id)
                            if sl.user_id == user_id:
                                row_list.append({"text": sl.user.name,"chosen": "chosen", "attrs": [("time_id", tc[0]),("room_id",room.id)]})
                            else:
                                row_list.append({"text": sl.user.name,"chosen": "chosen", "attrs": [("disable","true"),("time_id", tc[0]),("room_id",room.id)]})
                            break
                    else:
                        row_list.append({"text": "","chosen": "", "attrs": [("time_id", tc[0]),("room_id",room.id)]})
                data["data"].append({"title":room.title,"row_list":row_list})
            for i, x in enumerate(data["data"], 1):
                print("%s----%s" % (i, x))

        except Exception as e:
            print("---",e)
            data["state"] = False
            data["msg"]="查询失败%s"%str(e)
    else:
        chosen_data = request.POST.get("chosen_data")
        chosen_data = datetime.datetime.strptime(chosen_data, "%Y-%m-%d").date()
        if chosen_data < nowdata:
            raise Exception("不能查询已过期的日期")
        try:
            selected_info = json.loads(request.POST.get("selected_room"))
            # {
            #    "DEL":{
            #               "1":["2","1"],
            #               "2":["5"]},
            #    "ADD":{
            #               "1":["3","4","5","6","1"],
            #               "2":["6"]}}

            # 去除因失误取消的原预定
            for room_id, addtime_list in selected_info["ADD"].items():
                if room_id not in selected_info["DEL"]:
                    continue
                for time_id in list(addtime_list):
                    if time_id in selected_info["DEL"][room_id]:
                        selected_info["DEL"][room_id].remove(time_id)
                        selected_info["ADD"][room_id].remove(time_id)

            # 添加预定
            add_obj_list = []
            for room_id, addtime_list in selected_info["ADD"].items():
                for time_id in addtime_list:
                    obj = Select(user_id=user_id, room_id=room_id, time=time_id, data=chosen_data)
                    add_obj_list.append(obj)
            Select.objects.bulk_create(add_obj_list)

            # 删除预定
            remove_select = Q()
            for room_id, deltime_list in selected_info["DEL"].items():
                for time_id in deltime_list:
                    print("remove_select--time_id", time_id)
                    temp = Q()
                    temp.connector = "AND"
                    temp.children.append(("user_id", user_id))
                    temp.children.append(("room_id", room_id))
                    temp.children.append(("time", time_id))
                    temp.children.append(("data", chosen_data))
                    remove_select.add(temp, "OR")
            print("remove_select", remove_select)
            if remove_select:
                Select.objects.filter(remove_select).delete()
        except Exception as e:
            data["state"]=False
            data["msg"]="预定失败%s"%str(e)

    return JsonResponse(data)
