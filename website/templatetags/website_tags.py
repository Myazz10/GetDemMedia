from django import template
from website.models import PermitPlaylistDownload, MyazzDesignzProfile, WebsiteName, AnimatedHeaderText, Notice


register = template.Library()


# THIS IS A GREAT WAY TO DEAL WITH THE SUB-QUERIES AND ASSIGN THE RESULTS TO CUSTOM TAGS


# The simple_tag will return a variable.
@register.simple_tag
def permission():
    permitted = PermitPlaylistDownload.objects.filter(approved=True)
    approved = False

    for item in permitted:
        if item.approved:
            approved = True

    return approved


@register.simple_tag
def designer():
    contact_set = MyazzDesignzProfile.objects.all()
    contacts = []

    for item in contact_set:
        contacts.append(item.website)
        contacts.append(item.facebook)
        contacts.append(item.twitter)
        contacts.append(item.instagram)
        contacts.append(item.pinterest)

    return contacts


@register.simple_tag
def name_of_website():
    name_set = WebsiteName.objects.all()
    name = ""

    for item in name_set:
        name = item.name

    return name


@register.simple_tag
def animated_header_text():
    text_set = AnimatedHeaderText.objects.all()
    context = []

    for item in text_set:
        context.append(item.first_paragraph)
        context.append(item.second_paragraph)
        context.append(item.third_paragraph)
        context.append(item.fourth_paragraph)

    return context


@register.simple_tag
def site_maintenance():
    timer = Notice.objects.filter(approved=True)
    approved = False

    for item in timer:
        if item.approved:
            approved = True

    return approved


# In the preceding code, you register the template tag using @register.inclusion_
# tag and specify the template that will be rendered with the returned values using
# website/countdown.html.
@register.inclusion_tag('website/countdown.html')
def countdown_timer():
    timer = Notice.objects.filter(approved=True).first()
    context = {
        'timer': timer,
    }
    return context
