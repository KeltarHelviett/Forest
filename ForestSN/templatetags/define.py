from django import template
register = template.Library()

class DefineNode(template.Node):
    def __init__(self, var_name, value):
        self.var = var_name
        self.value = value

    def render(self, context):
        context[self.var] = self.value.strip("'").strip('"')
        return ''

def define(parser, token):
    try:
        tag_name, var_name, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r requires two arguments' % token.contents.split()[0]
        )
    return DefineNode(var_name, value)

register.tag('define', define)
