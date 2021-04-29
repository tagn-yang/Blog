from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Blog'
    site_title = 'Blog Manager Background'
    index_title = 'Index'


custom_site = CustomSite(name='cus_admin')
