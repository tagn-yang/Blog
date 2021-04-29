from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'blog'
    site_title = 'blog manager background'
    index_title = 'index'


custom_site = CustomSite(name='cus_admin')
