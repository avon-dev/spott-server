# from testapp.assemble_model.user_model import *
# from testapp.assembel_model.hashtag_model import *
# from testapp.assembel_model.post_model import *
# from testapp.assembel_model.comment_model import *
# from testapp.assembel_model.postlike_model import *
# from testapp.assembel_model.scrap_model import *












from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytz import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from .managers import UserManager
from django.utils.html import mark_safe
from django.contrib.postgres.fields import JSONField

class User(AbstractBaseUser, PermissionsMixin): #나중에 널 값 처리
    basic = 9000
    google = 9001
    facebook = 9002


    USER_TYPE = (
        (basic, '이메일 유저'),
        (google, '구글 유저'),
        (facebook, '페이스북 유저')
    )
    user_type = models.IntegerField(default = basic, choices = USER_TYPE, verbose_name = '가입한 방식')
    user_uid = models.CharField(max_length=255, unique = True) #이메일 해싱 삭제를 했어 lwbvv@naver.com
    email = models.EmailField(_('email address'))
    password = models.CharField(_('password'), max_length=200)
    nickname = models.CharField(max_length=150)
    profile_image = models.ImageField(upload_to = 'usr', null = True, blank = True)
    joined_date = models.DateTimeField(_('date joined'), auto_now_add=True) #생성날짜
    is_active = models.BooleanField(_('active'), default=True) #아이디 활성화 상태인지(삭제여부)  판별
    is_public = models.BooleanField(default = True)
    is_login = models.BooleanField(default = False) #로그인 여부
    modify_date = models.DateTimeField(null = True, blank = True)
    is_staff = models.BooleanField(_('is staff'), default = False)
    recent_search = JSONField(blank = True, default = list)
    objects = UserManager()
    USEREMAIL_FIELD = 'email'
    USERNAME_FIELD = 'user_uid'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.user_uid

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser


# 스크랩을 취소 한다는건 해당 스크랩 테이블에서 레코드가 지워진다는 것을 뜻함
# 게시물이 지워졌을 때 연결 돼 있는 해당 스크랩까지 지워지도록 구현
# 스크랩 날짜를 구해야 될까??? 딱히??? 안 구해도 될거 같다.
# class Hashtag(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
#     name = models.CharField(max_length = 255)
#
#
#     def __str__(self):
#         return self.name



class Post(models.Model): #!내용(conents), !작성일, !수정일, !공개여부(public),
                        # !게시물 신고 여부, !신고 날짜, 부적절 게시물 여부(problem), !삭제여부, !삭제 날짜
    before_confirmation = 22000
    no_problem = 22001
    bad_location = 22002
    bad_picture = 22003
    bad_contents = 22004
    HANDLING_CHOICES = (
        (before_confirmation, '검사 전'),
        (no_problem, '사진 통과'),
        (bad_location, '잘못된 위치정보'),
        (bad_picture, '부적절한 사진'),
        (bad_contents, '부적절한 내용'),
    )

    basic_post = 200
    admin_post = 201
    KIND = (
        (basic_post, '일반 게시물'),
        (admin_post, '관리자 게시물'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'get_user') #get_post로 변경
    post_kind = models.IntegerField(default = basic_post ,choices = KIND ,verbose_name = '카테고리')
    posts_image = models.ImageField(upload_to = 'post') #R
    back_image = models.ImageField(upload_to = 'postb',null = True, blank = True) #R
    latitude = models.FloatField() #R
    longitude = models.FloatField() #R
    contents = models.TextField(default = "",verbose_name = '내용') #내용
    views = models.IntegerField(default = 0)
    created = models.DateTimeField(auto_now_add=True) #작성일
    modify_date = models.DateTimeField(null = True, blank = True) #게시글 수정일
    is_public = models.BooleanField(default = True) #공개여부
    handling = models.IntegerField(default = before_confirmation ,choices = HANDLING_CHOICES ,verbose_name = '검사')
    problem = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    hashtag = models.ManyToManyField('HashTag', through='PostTag',related_name='get_hashtag')
    like_user = models.ManyToManyField('User', through = 'PostLike',related_name= 'get_like')
    comment = models.ManyToManyField('User', through='Comment',related_name='get_comment')
    like_count = models.IntegerField(default = 0)
    scrap_users = models.ManyToManyField('User', through = 'Scrapt',related_name= 'get_scrap')
    reason_detail = models.TextField(default = "",verbose_name = "반려 사유 작성란" ) #상세 사유
    #좋아요가 1000개 이상 넘어가면 카운트로 조회
    def __str__(self):
        return str(self.id)

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.posts_image.url))  # Get Image url

        image_tag.short_description = 'Image'

    def user_email(self):
        return f'{self.user.email}'  # Get Image url

        user_email.short_description = 'user_email'


# class UserData(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,related_name= 'user_data')
#     scrap_users = models.ManyToManyField('Post', through = 'Scrap',related_name= 'get_scrap')
#     objects = UserManager()

class HashTag(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    name = models.CharField(unique = True, max_length=250, verbose_name = '태그명') #태그
    is_tag = models.BooleanField(default = True)
    count = models.IntegerField(default = 0)

    def __str__(self):
        return self.name


class PostTag(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name= 'post_posttag')
    tag = models.ForeignKey(HashTag,on_delete=models.CASCADE, related_name= 'tag_posttag')
    created = models.DateTimeField(auto_now_add=True) #작성일

    def __str__(self):
        return str(f'post pk:{self.post} tag pk:{self.tag}')


class Comment(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'post_comment')
    is_problem = models.BooleanField(default = False)
    contents = models.TextField(verbose_name = '내용') #내용
    created = models.DateTimeField(auto_now_add=True) #작성일
    modify_date = models.DateTimeField(null = True, blank = True) #댓글 수정일
    is_active = models.BooleanField(default = True)


    def __str__(self):
        return self.contents


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_like')
    created_date = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return str(self.post.id)


class Scrapt(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'post_scrap')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_scrap')
    created_date = models.DateTimeField(auto_now_add=True,)


    class Meta:
        ordering = ('-created_date',)

    # def __str__(self):
    #     return self.user




# def set_userFK_report(uuid):
#     return User.objects.get(user_uid = uuid)
#
DEFAULT_TEST_MODEL_PK = -1

class Report(models.Model):

    etc = 0
    spam = 1
    slander = 2
    porno = 3
    steal = 4

    no_problem = 0
    before_posts = 1
    after_posts = 2
    before_comment = 3
    after_comment = 4

    REASON_CHOICES = (
        (etc, '기타'),
        (spam, '스팸'),
        (slander, '욕설 및 비방'),
        (porno, '음란물'),
        (steal, '무단도용'),
    )


    HANDLING_CHOICES = (
        (no_problem, '문제 없음'),
        (before_posts, '게시물 처리 전'),
        (after_posts, '게시물 처리 후'),
        (before_comment, '댓글 처리 전'),
        (after_comment, '댓글 처리 후'),
    )
    rel_name = "phopo_reports_post_related"
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, to_field = 'user_uid', blank = True, null = True , related_name="%(app_label)s_%(class)s_reporter_related")
    # post_owner = models.CharField(default = "null",max_length = 200) #삭제해도 됨
    # comment_owner = models.CharField(default = "null",max_length = 200) #삭제해도 됨
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank = True, \
    null = True, related_name=rel_name)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank = True,\
    null = True, related_name="%(app_label)s_%(class)s_comment_related")

    handling = models.IntegerField(default = 0,choices = HANDLING_CHOICES, verbose_name = '신고처리')
    post_url = models.CharField(default = "null",max_length = 200, verbose_name = '이미지')
    post_caption = models.TextField(default = "null", verbose_name = '게시물 내용') #내용
    comment_contents = models.TextField(default = "null",verbose_name = "댓글")
    reason = models.IntegerField(default = -1, choices = REASON_CHOICES)
    detail = models.TextField(default = "", verbose_name = "상세내용")
    created_date= models.DateTimeField(auto_now_add=True) #신고 날짜
    reason_detail = models.TextField(default = "",verbose_name = "사유 작성란" ) #상세 사유

    def __str__(self):
        return f"id: {str(self.id)} reason: {self.get_reason_display()}"

    def image_post(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.post_url))  # Get Image url

        image_tag.short_description = 'Image'


    def reporter_email(self):
        return f'{self.reporter_email}'  # Get Image url

        reporter_email.short_description = 'reporter_email'

class Notice(models.Model):
    picture_return = 22001
    picture_no_problem = 22002
    created_comment = 22003
    violation_posts = 22004
    violation_comment = 22005
    KIND_CHOICES = (
        (picture_return, '사진 반려'),
        (picture_no_problem, '사진 통과'),
        (created_comment, '댓글 남김'),
        (violation_posts, '규칙 위반 게시물'),
        (violation_comment, '규칙 위반 댓글'),
    )

    receiver = models.ForeignKey(User, on_delete=models.CASCADE, to_field="id",related_name="%(app_label)s_%(class)s_receiver_related")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank = True, null = True, to_field="id",related_name="%(app_label)s_%(class)s_post_related")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank = True, null = True, to_field="id",related_name="%(app_label)s_%(class)s_comment_related")
    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank = True, null = True, to_field="id",related_name="%(app_label)s_%(class)s_report_related")
    kind = models.IntegerField(choices = KIND_CHOICES, verbose_name = '알림 종류')
    confirmation = models.BooleanField(default = False, verbose_name = '확인')
    created_date= models.DateTimeField(auto_now_add=True)


class AppNotices(models.Model):

    title = models.CharField(unique = True, max_length=250, verbose_name = '공지사항 타이틀')
    created_date = models.DateTimeField(auto_now_add=True,)
    contents_url = models.CharField(max_length = 200, verbose_name = '공지사항 내용')


    def __str__(self):
        return self.title
