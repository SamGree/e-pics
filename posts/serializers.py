from rest_framework import serializers
from .models import Post
from tags.models import Tag

from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy
from urllib.parse import  urljoin

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
        fields = ['id', 'title', 'description', 'image', 'download_count', 'created_at', 'author', 'author_image', 'comments_count', 'likes_count','is_liked', 'tags']
        read_only_fields = ['id', 'created_at', 'user', 'download_count', 'comments_count', 'likes_count']
        
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.post_likes.count()

    def get_tags(self, obj):
        return [post_tag.tag.name for post_tag in obj.post_tags.all()]
    
    def get_author_image(self, obj):
        if obj.user.profile_image:
            return urljoin("https://res.cloudinary.com/", obj.user.profile_image.url)
        return None

    def get_image(self, obj):
        if obj.image:
            return f"https://res.cloudinary.com/drmqd08fb/image/upload/{obj.image}"
        return None
    
    def get_is_liked(self, obj):
        """
        Check if the logged-in user has liked the post.
        """
        request = self.context.get('request', None)
        # print(f'')
        if request and request.user.is_authenticated:
            return obj.likes.filter(pk=request.user.pk).exists()
        return False

    def create(self, validated_data):
        """
        Handle the creation of a new post, including tag creation and 
        image upload via Cloudinary.
        """
        user = self.context['request'].user
        tags = self.context['request'].data.getlist('tags[]', [])
        image = self.context['request'].FILES.get('image')

        # Validate that the uploaded file is an image
        if image and not image.content_type.startswith('image/'):
            raise serializers.ValidationError("Uploaded file must be image type.")

        # Upload image to Cloudinary
        if image:
            upload_result = cloudinary_upload(image, resource_type="image")
            full_url = upload_result.get('secure_url')
            
            processed_url = full_url.replace("https://res.cloudinary.com/drmqd08fb/image/upload/", "")
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
        tags = self.context['request'].data.getlist('tags[]', [])
        image = self.context['request'].FILES.get('image')

        if image:
            if instance.image:
                public_id = instance.image.public_id
                cloudinary_destroy(public_id)

            upload_result = cloudinary_upload(image, resource_type="image")
            full_url = upload_result.get('secure_url')
            processed_url = full_url.replace("https://res.cloudinary.com/drmqd08fb/image/upload/", "")
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