from django import template

register = template.Library()


def tagslist(tags):
    return [str(name) for name in tags.all()]

def tags(tags):
    return ", ".join([f"#{name}" for name in tags.all()])


register.filter('tagslist', tagslist)
register.filter('tags', tags)