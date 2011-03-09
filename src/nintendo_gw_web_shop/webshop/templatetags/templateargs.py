from django import template
register = template.Library()

 
@register.filter( name='own_rating' )
def own_rating( obj, epk ):
    return obj.ownrating( epk )