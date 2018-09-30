from django import template
from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, results
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='to_url')
@stringfilter
def to_url(value):
    return value + '/'


@register.inclusion_tag("base/my_chang_list.html")
def my_result_list(cl):
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1

    rl = list(results(cl))
    for i in range(len(rl)):
        for j in range(1,len(rl[i])):
            rl[i][j] = mark_safe(rl[i][j].replace(
                '<a ','<a class="btn-link" ').replace(
                '<th class="','<th style="vertical-align:middle" class="text-center ').replace(
                '<td class="','<td style="vertical-align:middle" class="')
                )

    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': rl,}


@register.inclusion_tag('base/my_actions.html', takes_context=True)
def my_admin_actions(context):
    """
    Track the number of times the action field has been rendered on the page,
    so we know which value to use.
    """
    context['action_index'] = context.get('action_index', -1) + 1
    return context