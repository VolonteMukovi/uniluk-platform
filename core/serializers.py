from rest_framework import serializers
from .models import *

class PublicModelSerializer(serializers.ModelSerializer):
    def media_value(self, obj, field, url_field):
        value = getattr(obj, field, None)
        return self.context['request'].build_absolute_uri(value.url) if value else getattr(obj, url_field, '')

class SiteSettingsSerializer(PublicModelSerializer):
    logo_display = serializers.SerializerMethodField()
    class Meta: model = SiteSettings; fields = '__all__'
    def get_logo_display(self, o): return self.media_value(o, 'logo', 'logo_url')

class HeroSlideSerializer(PublicModelSerializer):
    image_display = serializers.SerializerMethodField()
    class Meta: model = HeroSlide; fields = '__all__'
    def get_image_display(self, o): return self.media_value(o, 'image', 'image_url')

class ImageSerializer(PublicModelSerializer):
    image_display = serializers.SerializerMethodField()
    def get_image_display(self, o): return self.media_value(o, 'image', 'image_url')

class FacultySerializer(ImageSerializer):
    schedule_url = serializers.SerializerMethodField()
    class Meta: model = Faculty; fields = '__all__'
    def get_schedule_url(self,o):
        return self.context['request'].build_absolute_uri(o.schedule_file.url) if o.schedule_file else ''

class ArticleSerializer(ImageSerializer):
    class Meta: model = Article; fields = '__all__'
class AnnouncementSerializer(PublicModelSerializer):
    attachment_url = serializers.SerializerMethodField()
    class Meta: model = Announcement; fields = '__all__'
    def get_attachment_url(self,o): return self.context['request'].build_absolute_uri(o.attachment.url) if o.attachment else ''
class InstitutionSerializer(ImageSerializer):
    class Meta: model = Institution; fields = '__all__'
class StudentGroupSerializer(ImageSerializer):
    class Meta: model = StudentGroup; fields = '__all__'
class CampusBuildingSerializer(ImageSerializer):
    class Meta: model = CampusBuilding; fields = '__all__'
class GalleryImageSerializer(ImageSerializer):
    class Meta: model = GalleryImage; fields = '__all__'
class TestimonialSerializer(PublicModelSerializer):
    avatar_display = serializers.SerializerMethodField()
    class Meta: model = Testimonial; fields = '__all__'
    def get_avatar_display(self,o): return self.media_value(o, 'avatar', 'avatar_url')
class StatisticSerializer(serializers.ModelSerializer):
    class Meta: model = Statistic; fields = '__all__'
class ServiceSerializer(serializers.ModelSerializer):
    class Meta: model = Service; fields = '__all__'
class PageContentSerializer(PublicModelSerializer):
    image_display = serializers.SerializerMethodField(); video_display = serializers.SerializerMethodField()
    class Meta: model = PageContent; fields = '__all__'
    def get_image_display(self,o): return self.media_value(o, 'image', 'image_url')
    def get_video_display(self,o): return self.media_value(o, 'video', 'video_url')
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta: model = Registration; fields = '__all__'; read_only_fields = ('created_at',)
