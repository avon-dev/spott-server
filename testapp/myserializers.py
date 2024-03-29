from rest_framework import serializers
from .models import *
import datetime






class SerialTest(serializers.Serializer):
    tag_name = serializers.CharField(max_length = 200)
    user_is_active = serializers.CharField(max_length = 200)
    # content = serializers.CharField(max_length=200)
    # created = serializers.DateTimeField()





class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        # extra_kwargs = {"password": {"write_only": True}}
        #
        # def create(self, validated_data):
        #     user = User(email=validated_data['email'],nickname=validated_data['nickname'])
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')



class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','posts_image',"created",)
        # read_only_fields = ('created_at',)




class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_login',)
        # read_only_fields = ('created_at',)

class EmailRertieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','nickname',)
        # read_only_fields = ('created_at',)


class PostSerializer(serializers.ModelSerializer):
    # created = serializers.DateTimeField(format="%Y-%m-%dT%H:%MZ")
    class Meta:
        model = Post
        fields = ('id' ,'posts_image', 'latitude', 'longitude','like_count', 'post_kind')
        # read_only_fields = ('created_at',)

class PostAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        # read_only_fields = ('created_at',)


class PostsContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('contents',)
        # read_only_fields = ('created_at',)
##############################################

class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','nickname','profile_image',)

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('name',)

class PostDetailSerializer(serializers.ModelSerializer):
    user = UserProfile(read_only=True)
    # hashtag = HashTagSerializer(read_only=True,many=True)
    class Meta:
        model = Post
        # fields = ('user',)
        exclude = ('modify_date','is_active','problem')
#################################################



##############################################

class MypageSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = Post
        # fields=('__all__')
        fields = ('id','posts_image','latitude','longitude',)
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')
#################################################




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('__all__')
        # read_only_fields = ('created_at',)



class ScrapPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','posts_image','back_image')
        # read_only_fields = ('created_at',)

class ScrapAllSerializer(serializers.ModelSerializer):
    hashtag = ScrapPostSerializer(read_only=True,many=True)
    class Meta:
        model = Post
        fields = ('__all__')
        # exclude = ('__all__')


class ScrapSerializer(serializers.ModelSerializer):
    post = ScrapPostSerializer(read_only=True)
    class Meta:
        model = Scrapt
        fields = ('post',)
#################################################


class MyUserCommentSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = User
        # fields=('__all__')
        fields = ('id','nickname','profile_image','user_uid', 'email')
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')


class CommentSerializer(serializers.ModelSerializer):
    user = MyUserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        # fields = ('__all__')
        exclude = ('is_active','post','modify_date')



class SearchNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('__all__')
        fields = ('id','nickname','profile_image')


class SearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        # fields = ('__all__')
        fields = ('name','is_tag')


class TagListSerializer(serializers.ModelSerializer):
    post = HomeSerializer(read_only=True)
    class Meta:
        model = PostTag
        # fields = ('__all__')
        fields = ('__all__')








############################유저 프로필 시리얼라이징
class MyUserSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = User
        # fields=('__all__')
        fields = ('email','nickname','profile_image','is_public')
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')
############################유저 프로필 시리얼라이징
class MyProfileSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = User
        # fields=('__all__')
        fields = ('email','nickname','profile_image','is_public', 'user_type')
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')

class NoticeSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = Notice
        # fields=('__all__')
        fields = ('__all__')
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')



class AppNoticeSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = AppNotices
        # fields=('__all__')
        fields = ('__all__')
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')
