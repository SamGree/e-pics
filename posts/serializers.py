from rest_framework import serializers
from .models import Post
from tags.models import Tag
from posttags.models import PostTag
from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy
from urllib.parse import urljoin
from django.conf import settings
from urllib.parse import urlparse
from cloudinary.utils import cloudinary_url

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model, handling nested fields, tag management, 
    and image uploads via Cloudinary.
    """
    author = serializers.CharField(source='user.username', read_only=True)
    author_image = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'image', 'download_count',
            'created_at', 'author', 'author_image', 'comments_count',
            'likes_count', 'is_liked', 'tags'
        ]
        read_only_fields = ['id', 'created_at', 'user', 'download_count', 'comments_count', 'likes_count']
        
    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        count = obj.likes.count()
        return count

    def get_is_liked(self, obj):
        """
        Check if the logged-in user has liked the post.
        """
        request = self.context.get('request', None)
        if request:
            print(f"Request User: {request.user}, Post ID: {obj.id}")
            if request.user.is_authenticated:
                is_liked = obj.likes.filter(id=request.user.id).exists()
                print(f"Is Liked: {is_liked}")
                return is_liked
        return False

    def get_tags(self, obj):
        return [post_tag.tag.name for post_tag in obj.post_tags.all()]
    
    def get_author_image(self, obj):
        if obj.user.profile_image:
            return urljoin("https://res.cloudinary.com/", obj.user.profile_image.url)
        return None

    def get_image(self, obj):
      """
      Returns the image URL from the CloudinaryField.
      """
      if obj.image:
            if hasattr(obj.image, "url"):
                return obj.image.url
            elif hasattr(obj.image, "public_id"):
                url, options = cloudinary_url(obj.image.public_id, secure=True)
                return url
      return None

    def create(self, validated_data):
        """
        Handle the creation of a new post, including tag creation and 
        image upload via Cloudinary.
        """
        user = self.context['request'].user
        tags = self.context['request'].data.get('tags[]', [])
        image = self.context['request'].FILES.get('image')

        # Validate that the uploaded file is an image
        if image and not image.content_type.startswith('image/'):
            raise serializers.ValidationError("Uploaded file must be image type.")

        # Upload image to Cloudinary
        if image:
            upload_result = cloudinary_upload(image, resource_type="image")
            full_url = upload_result.get('secure_url')

            # Extract cloud name dynamically from CLOUDINARY_STORAGE or CLOUDINARY_URL
            cloudinary_url = settings.CLOUDINARY_STORAGE.get('CLOUDINARY_URL', '')
            parsed_url = urlparse(cloudinary_url)
            cloud_name = parsed_url.path.lstrip('/')  # Extract cloud name from the URL
            
            processed_url = full_url.replace(f"https://res.cloudinary.com/{cloud_name}/", "")
            validated_data['image'] = processed_url

        # Create the post
        post = Post.objects.create(user=user, **validated_data)

        # Create tags and associate them with the post
        for tag_name in tags:
            tag_name = tag_name.strip()
            tag, created = Tag.objects.get_or_create(name=tag_name)
            PostTag.objects.get_or_create(post=post, tag=tag)

        return post

    def update(self, instance, validated_data):
        """
        Handle the update of a post, including tag management and image replacement.
        """
        tags = self.context['request'].data.get('tags[]', [])
        image = self.context['request'].FILES.get('image')

        if image:
            if instance.image:
                public_id = instance.image.public_id
                cloudinary_destroy(public_id)

            upload_result = cloudinary_upload(image, resource_type="image")
            full_url = upload_result.get('secure_url')

            # Extract cloud name dynamically from CLOUDINARY_STORAGE or CLOUDINARY_URL
            cloudinary_url = settings.CLOUDINARY_STORAGE.get('CLOUDINARY_URL', '')
            parsed_url = urlparse(cloudinary_url)
            cloud_name = parsed_url.path.lstrip('/')  # Extract cloud name from the URL

            processed_url = full_url.replace(f"https://res.cloudinary.com/{cloud_name}/", "")
            validated_data['image'] = processed_url

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        if tags:
            instance.post_tags.all().delete()

            for tag_name in tags:
                tag_name = tag_name.strip()
                tag, created = Tag.objects.get_or_create(name=tag_name)
                PostTag.objects.create(post=instance, tag=tag)

        return instance
