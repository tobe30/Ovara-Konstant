from import_export import resources
from dashboard.models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        import_id_fields = ['item_id']
        skip_unchanged = True
        report_skipped = True
