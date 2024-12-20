from rest_framework import serializers
from .models import User
from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, handling validation, creation, and updating of user data.
    Includes additional logic for handling profile image uploads via Cloudinary.
    """
    password_again = serializers.CharField(write_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_again', 'profile_image', 'bio']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_image': {'required': False},
            'bio': {'required': False},
        }
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            return f"https://res.cloudinary.com/drmqd08fb/image/upload/{obj.profile_image}"
        return None

    def validate(self, attrs):
        """
        Validate that the passwords match and adhere to custom rules.
        """
        if 'password' in attrs or 'password_again' in attrs:
            if attrs.get('password') != attrs.get('password_again'):
                raise serializers.ValidationError({'error': 'Passwords do not match.'})
            if len(attrs.get('password')) < 8:
                raise serializers.ValidationError({'error': 'Password must be at least 8 characters long.'})

        return attrs

    def create(self, validated_data):
        """
        Create a new user instance with optional profile image upload to Cloudinary.
        """
        validated_data.pop('password_again')
        profile_image = self.context['request'].FILES.get('profile_image')

        # Validate that the uploaded file is an image
        if profile_image and not profile_image.content_type.startswith('image/'):
            raise serializers.ValidationError("Uploaded file must be image type.")

        # Upload image to Cloudinary
        if profile_image:
            upload_result = cloudinary_upload(profile_image, resource_type="image")
            full_url = upload_result.get('secure_url')
            
            processed_url = full_url.replace("https://res.cloudinary.com/drmqd08fb/image/upload/", "")
            validated_data['profile_image'] = processed_url

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            profile_image=validated_data.get('profile_image', None)
        )
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user instance, including profile image replacement if provided.
        """
        validated_data.pop('password', None)
        validated_data.pop('password_again', None)

        profile_image = self.context['request'].FILES.get('profile_image')

        if profile_image:
            if instance.profile_image:
                public_id = instance.profile_image.public_id
                result = cloudinary_destroy(public_id)
                if not result:
                    raise Exception("Deleting the old image failed.")

            upload_result = cloudinary_upload(profile_image, resource_type="image")
            full_url = upload_result.get('secure_url')
            processed_url = full_url.replace("https://res.cloudinary.com/drmqd08fb/image/upload/", "")
            instance.profile_image = processed_url

        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


