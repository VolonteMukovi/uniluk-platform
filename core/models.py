from django.db import models

class Ordered(models.Model):
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)
    class Meta:
        abstract = True
        ordering = ('order', '-id')

class SiteSettings(models.Model):
    name = models.CharField(max_length=200, default='UNILUK')
    full_name = models.CharField(max_length=255, default='Université Adventiste de Lukanga')
    logo = models.ImageField(upload_to='branding/', blank=True)
    logo_url = models.URLField(blank=True)
    favicon = models.ImageField(upload_to='branding/', blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    maps_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True, verbose_name='Lien X / Twitter')
    footer_text = models.TextField(blank=True)
    class Meta: verbose_name_plural = 'Paramètres du site'
    def __str__(self): return self.name

class HeroSlide(Ordered):
    image = models.ImageField(upload_to='hero/', blank=True)
    image_url = models.URLField(blank=True)
    tag = models.CharField(max_length=255)
    title = models.CharField(max_length=300)
    alt = models.CharField(max_length=300, blank=True)
    caption = models.CharField(max_length=300, blank=True)

class Statistic(Ordered):
    icon = models.CharField(max_length=80)
    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=20, blank=True)
    label = models.CharField(max_length=150)

class Faculty(Ordered):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='faculties/', blank=True)
    image_url = models.URLField(blank=True)
    short_description = models.TextField()
    description = models.TextField()
    programs = models.JSONField(default=list, blank=True)
    schedule_file = models.FileField(upload_to='schedules/', blank=True)

class Article(Ordered):
    category = models.CharField(max_length=100)
    category_color = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='articles/', blank=True)
    image_url = models.URLField(blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    published_at = models.DateField(db_index=True)
    class Meta(Ordered.Meta): ordering = ('-published_at', '-id')

class Announcement(Ordered):
    tag = models.CharField(max_length=100)
    color = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    published_at = models.DateField(db_index=True)
    attachment = models.FileField(upload_to='announcements/', blank=True)
    class Meta(Ordered.Meta): ordering = ('-published_at', '-id')

class Institution(Ordered):
    acronym = models.CharField(max_length=30)
    color = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='institutions/', blank=True)
    image_url = models.URLField(blank=True)
    short_description = models.TextField()
    description = models.TextField()

class StudentGroup(Ordered):
    acronym = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=80, blank=True)
    color = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='groups/', blank=True)
    image_url = models.URLField(blank=True)
    description = models.TextField()
    full_description = models.TextField()
    achievements = models.JSONField(default=list, blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)

class CampusBuilding(Ordered):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='campus/', blank=True)
    image_url = models.URLField(blank=True)

class Service(Ordered):
    section = models.CharField(max_length=50, default='clinic', db_index=True)
    icon = models.CharField(max_length=80)
    title = models.CharField(max_length=255)
    description = models.TextField()

class GalleryImage(Ordered):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery/', blank=True)
    image_url = models.URLField(blank=True)
    alt = models.CharField(max_length=255, blank=True)

class Testimonial(Ordered):
    quote = models.TextField()
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    avatar_url = models.URLField(blank=True)

class PageContent(models.Model):
    """Editable text and media blocks for fixed template sections (church, clinic, campus video, registration)."""
    key = models.SlugField(unique=True)
    title = models.CharField(max_length=300)
    subtitle = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='pages/', blank=True)
    image_url = models.URLField(blank=True)
    video = models.FileField(upload_to='videos/', blank=True)
    video_url = models.URLField(blank=True)
    highlight_value = models.CharField(max_length=50, blank=True, verbose_name='Valeur mise en avant')
    highlight_label = models.CharField(max_length=255, blank=True, verbose_name='Libellé de la mise en avant')
    def __str__(self): return self.key

class Registration(models.Model):
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, null=True, blank=True, on_delete=models.SET_NULL)
    motivation = models.TextField()
    document = models.FileField(upload_to='registrations/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=20, default='new', choices=[('new','Nouveau'),('review','En cours'),('accepted','Accepté'),('rejected','Refusé')])
    class Meta: ordering = ('-created_at',)
