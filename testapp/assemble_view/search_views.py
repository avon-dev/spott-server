from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from random import *

class SearchView(APIView):

    permission_classes = (IsAuthenticated,)
#




# #으로 검색을 했을 시에는 해쉬태그로 검색 아이템 하나로
# 검색을 할 때 그러면 객체의 수를 다 세어서
    def get(self, request, format=None):
        required_keys = ['search_word', 'is_tag']
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
        try:
            for key in required_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(required_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            search_word = request_data[required_keys[0]]
            is_tag = request_data[required_keys[1]]

        post = Post.objects.filter(is_active = True, problem = False, is_public = True)
        post_tag = PostTag.objects.filter(post__in = post).distinct('tag').values()
        tag_id_list = []
        for tag in post_tag:
            tag_id_list.append(tag['tag_id'])
        print(str(post_tag))
        if is_tag:

            tag_obj = HashTag.objects.filter(name__istartswith = search_word, id__in = tag_id_list).order_by('-count')[:16]
            tag_serializer = SearchTagSerializer(tag_obj, many = True)
            result = Return_Module.ReturnPattern.success_text\
            ("Search success", items = tag_serializer.data)
            return Response(result)
        else:
            user_obj = User.objects.filter(is_active = True, nickname__istartswith = search_word)
            tag_obj = HashTag.objects.filter(name__istartswith = search_word, id__in = tag_id_list)
            tag_serializer = SearchTagSerializer(tag_obj,many=True)
            user_serializer = SearchNameSerializer(user_obj,many=True)

            user_json_dumps_loads = json.loads(json.dumps(user_serializer.data))
            count = 0
            for users in range(len(user_json_dumps_loads)):
                user_json_dumps_loads[count]['is_tag'] = False
                count += 1

            result_list = tag_serializer.data + user_json_dumps_loads
            result = Return_Module.ReturnPattern.success_text\
            ("Search success",items = result_list)
            return Response(result)


        # user= User.objects.all()
        # user[0].user_hashtag.all()
        # # tag_obj = HashTag.objects.all().select_related()
        # # tag_serializer = SerialTest(tag_obj,many=True)
        # # print(str(tag_obj[0].query())
        # # print(tag_obj.query)
        # return Response(str(user))



class RecentSearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    action_user = 1202
    action_tag = 1102
    #user, tag 각 각 하나씩 2쿼리
    def list(self,request):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        # request_data = Return_Module.string_to_dict(request.data)
        user = User.objects.all()
        tag = HashTag.objects.all()
        list = []
        try:
            myself = user.get(user_uid = decodedPayload['user_uid'])
        except User.DoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result,status = status.HTTP_404_NOT_FOUND)

        count = 0
        for recent in myself.recent_search:
            if recent['action'] == 1202:
                try:
                    user.get(pk = recent['user_pk'])
                except Exception as e:
                    del myself.recent_search[count]
                    myself.save()
                else:
                    list.append(SearchNameSerializer(user.get(pk = recent['user_pk'])).data)
                    list[count]['is_tag'] = False

            else:
                try:
                    tag.get(name = recent['tag_name'])
                except Exception as e:
                    del myself.recent_search[count]
                    myself.save()
                else:
                    list.append(SearchTagSerializer(tag.get(name = recent['tag_name'])).data)
            count += 1

        result = Return_Module.ReturnPattern.success_text\
        ("create success",items = list)
        return Response(result,status=status.HTTP_200_OK)



#사이즈가 16이상시 맨 마지막꺼 pop 시키는 코드 추가
    @transaction.atomic
    def post(self, request):
        request_data_key = ['action','tag_name', 'user_pk']

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        request_data = Return_Module.string_to_dict(request.data)
        user = User.objects.get(user_uid = decodedPayload['user_uid'])


        user.recent_search.insert(0,request_data)
        del user.recent_search[0]
        user.save()

        result = Return_Module.ReturnPattern.success_text\
        ("create success",result = True)


        return Response(result, status=status.HTTP_201_CREATED)



    # def partial_update(self, request, pk=None):
    #     position = int(pk)
    #     string = request.headers["Authorization"]
    #     decodedPayload = jwt.decode(string[4:],None,None)
    #     user = User.objects.get(user_uid = decodedPayload['id'])
    #     recent_search_word = user.recent_search[position]
    #     del user.recent_search[position]
    #     user.recent_search.insert(0,recent_search_word)
    #     user.save()
    #
    #     result = Return_Module.ReturnPattern.success_test\
    #     ("recent_search_item_click success",result = True)
    #     return Response(result, status=status.HTTP_404_NOT_FOUND)



    @transaction.atomic
    def destroy(self, request, pk=None):
        position = int(pk)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload['user_uid'])

        if position == -1:
            user.recent_search.clear()
            user.save()
        else:
            if len(user.recent_search) == 0:
                pass
            else:
                del user.recent_search[position]
                user.save()

        result = Return_Module.ReturnPattern.success_text\
        ("delete success",result = True)
        return Response(result)
