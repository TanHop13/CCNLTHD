from rest_framework import viewsets, generics,  status, parsers, permissions
from courses.models import Category, Course, Lesson, Tag, User, Comment, Like
from courses import serializers, paginators, perms

from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializers


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializers
    pagination_class = paginators.CoursePaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action == 'List':
            q = self.request.query_params.get('q')
            if q:
                queryset = Course.objects.filter(name__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                queryset = Course.objects.filter(category_id=cate_id)

        return queryset

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)
        return Response(serializers.LessonSerializers(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tag').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    def get_permissions(self):
        if self.action in ["add_comments"]:
            return [permissions.IsAuthenticated(), ]

        return [permissions.AllowAny(), ]

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        paginator = paginators.CommentPaginator()
        comments = self.get_object().comment_set.select_related('user').order_by("-id")
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializers(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializers(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        comment = self.get_object().comment_set.create(content=request.data.get('content'),
                                                       user=request.user)

        return Response(serializers.CommentSerializers(comment).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='likes', detail=True)
    def like(self, request, pk):
        li, created = Like.objects.get_or_create(lesson=self.get_object(), user=request.user)

        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.LessonDetailsSerializer(self.get_object()).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializers
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ["get_current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get", "patch"], url_path="current_user", detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializers(user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializers
    permission_classes = [perms.CommentOwner]
