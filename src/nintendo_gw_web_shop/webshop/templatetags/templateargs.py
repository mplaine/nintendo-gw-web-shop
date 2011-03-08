from django import template
register = template.Library()

#@register.filter("call", callMethod)
#def callMethod(obj, methodName):
#    method = getattr(obj, methodName)
 
#    if obj.__dict__.has_key("__callArg"):
#        ret = method(*obj.__callArg)
#        del obj.__callArg
#        return ret
#    return method()
 
#@register.filter("args", args)
#def args(obj, arg):
#    if not obj.__dict__.has_key("__callArg"):
#        obj.__callArg = []
# 
#    obj.__callArg += [arg]
#    return obj
 
@register.filter(name='own_rating')
def own_rating(obj, epk):
    return obj.ownrating(epk)

