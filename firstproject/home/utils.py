from django.template.defaultfilters import slugify
import uuid

def generate_unique_slug(name, ModelClas):
    new_slug = slugify(name)
    if ModelClas.objects.filter(slug=new_slug).exists():
        new_slug = f"{new_slug}-{uuid.uuid4().hex[:8]}"
    return new_slug