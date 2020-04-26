from django.conf.urls import url
from .views import default_map, add_case_map, symptons_view

urlpatterns = [
    url('', default_map, name="default"),
    # url('current', default_map, name="default"),
    # url('add_case', symptons_view, name="add_case"),

]