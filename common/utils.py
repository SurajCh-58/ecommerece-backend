from PIL import Image
from rest_framework import serializers
from django.utils.text import slugify

def generate_unique_slug(instance, title_field='name', slug_field='slug'):
    """
    Generates a unique slug dynamically using getattr and setattr.
    """
    current_slug = getattr(instance, slug_field)
    
    # If a slug already exists, leave it alone (protects manual SEO changes)
    if current_slug:
        return

    # Get the source text (e.g., name) and slugify it
    title_value = getattr(instance, title_field)
    base_slug = slugify(title_value)
    slug = base_slug
    counter = 1

    ModelClass = instance.__class__

    # Check for duplicates and append a counter if needed
    while ModelClass.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    # Save the final slug back to the instance
    setattr(instance, slug_field, slug)

def validate_image(image):
        if image.size>2*1024*1024:
            raise serializers.ValidationError("Image size must be less than 2 MB.")
        try:
            img=Image.open(image)
            img.verify()

            image.seek(0)

            img=Image.open(image)

        except Exception:
            raise serializers.ValidationError("The uploaded file is not a valid image.")
        if img.format not in ('JPEG','PNG','WEBP'):
            raise serializers.ValidationError("Only JPEG, PNG, and WEBP images are supported.")
        return image