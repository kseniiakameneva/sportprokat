from django.conf.urls import url
from prokat.views import base_view, prod_list, rules_view, prod_detail, booking_view, contact_view, thankyou_view, \
    get_queryset, check

urlpatterns = [
    # url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    # url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    url(r'^$', base_view, name='base'),
    url(r'^category/(?P<pk>\d+)/$', prod_list, name='category'),

    url(r'^rules/', rules_view, name='rules'),
    url(r'^booking/', booking_view, name='booking'),
    url(r'^prod_detail/(?P<pk>\d+)/$', prod_detail, name='prod_detail'),
    url(r'^contacts/', contact_view, name='contacts'),
    url(r'^thankyou/', thankyou_view, name='thankyou'),
    url(r'^place_search/$', get_queryset, name='place_search'),
    url(r'^check/', check, name='check'),

]
