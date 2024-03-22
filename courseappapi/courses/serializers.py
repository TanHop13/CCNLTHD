from rest_framework import serializers
from courses.models import Category, Course, Lesson, Tag, User, Comment


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url
        return rep


class CourseSerializers(ItemSerializers):
    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'create_date']


class LessonSerializers(ItemSerializers):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'create_date']


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonDetailsSerializer(LessonSerializers):
    tag = TagSerializers(many=True)

    class Meta:
        model = LessonSerializers.Meta.model
        fields = LessonSerializers.Meta.fields + ['tag', 'content']


class UserSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': 'true'
            }
        }


class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'create_date', 'user']
