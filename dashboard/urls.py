from django.urls import path
from .views import index, addproduct, productlist, addpurchase, purchaselist, addsale, salelist, editproduct, edit_purchase, edit_sale, delete_product, delete_purchase, delete_sale, addtype, type, edit_type, delete_type, Login, logoutView, notifications, edit_admin_profile, addbc, addnumber, adddc, addnp, bclist, delete_bc, editbc, numlist, editnum, delete_num, dclist, delete_dc, editdc, nplist, editnp, delete_np, inventory, addcustomer, customer_list, delete_customer, editcutomer
from django.contrib.auth import views as auth_views
from .controllers import addbcpurchase, bcpurchaselist, delete_bcpurchase, edit_bcpurchase, addbcsale, bcsalelist, delete_bcsale, bcedit_sale, addnpurchase, npurchaselist, delete_npurchase, edit_npurchase, addnsale, nsalelist, delete_nsale, nedit_sale, add_dspurchase, dspurchaselist, delete_dpurchase, edit_dpurchase, adddsale, dsalelist, delete_dsale, dedit_sale, n7purchaselist, add_n7purchase, edit_n7purchase, delete_n7purchase, ad_np7sale, np_salelist, delete_npsale, edit_npsale, bc_inventory, nu_inventory, ds_inventory, np_inventory

app_name = "dashboard"


urlpatterns = [
    
    
    path("", index, name="index"),
    path("inventory/", inventory, name="inventory"),
    path("bc-invent/", bc_inventory, name="bcinventory"),
    path("nu_in/", nu_inventory, name="nuinventory"),
    path("ds-9cventory/", ds_inventory, name="dsinventory"),
    path("np-ivm/", np_inventory, name="npinventory"),


    
    
    
    path("add-bc/", addbc, name="addbc"),
    path("edit-bc/<pk>", editbc, name="editbc"),
    path("bc-list/", bclist, name="bclist"),
    path('delete-bc/<pk>', delete_bc, name='deletebc'),
    path("addbc-purchase/", addbcpurchase, name="addbcpurchase"),
    path("bcpurchase/", bcpurchaselist, name="bcplist"),
    path('delete-bcpurchase/<pk>', delete_bcpurchase, name='deletepl'),
    path("edit-bcpurchase/<pk>", edit_bcpurchase, name="editbcpurchase"),
    path("adbcsale/", addbcsale, name="addbcsale"),
    path("bcsalelist/", bcsalelist, name="bcsalelist"),
    path('delete-bcsale/<pk>', delete_bcsale, name='deletebcsale'),
    path("bcedit-sale/<pk>", bcedit_sale, name="bceditsale"),
    
    
    
    
    
    
    path("num-list/", numlist, name="numlist"),
    path("edit-num/<pk>/", editnum, name="editnum"),
    path('delete-num/<pk>', delete_num, name='deletenum'),
    path("add-number/", addnumber, name="addnum"),
    path("addnumpurchase/", addnpurchase, name="addnpurchase"),
    path("numberp-list/", npurchaselist, name="npurchaselist"),
    path('deletenp/<pk>', delete_npurchase, name='deleten'),
    path("numeditp/<pk>", edit_npurchase, name="editnpurchase"),
    path("80800-addsale/", addnsale, name="addnsale"),
    path("sales-80800/", nsalelist, name="nsalelist"),
    path('delete-nsale/<pk>', delete_nsale, name='deletensale'),
    path("nedit-sale/<pk>", nedit_sale, name="neditsale"),
    
    
    

    
    path("add-dc/", adddc, name="adddc"),
    path("dc-list/", dclist, name="dclist"),
    path("delete-dc/<pk>/", delete_dc, name="deletedc"),
    path("edit-dc/<pk>/", editdc, name="editdc"),
    path("ds-addpurchase/", add_dspurchase, name="adddspurchase"),
    path("ds-list/", dspurchaselist, name="dpurchaselist"),
    path('delete-dspurchase/<pk>', delete_dpurchase, name='deleted'),
    path("edit-dpurchase/<pk>", edit_dpurchase, name="edit-dp"),
    path("DS-9Caddsale/", adddsale, name="add_dsale"),
    path("dsales-list/", dsalelist, name="dsalelist"),
    path('delete-dsale/<pk>', delete_dsale, name='deletedsale'),
    path("dedit-sale/<pk>", dedit_sale, name="deditsale"),
    
    
    
    
    
    path("add-np/", addnp, name="addnp"),
    path("np-list/", nplist, name="nplist"),
    path("edit-np/<pk>/", editnp, name="editnp"),
    path('delete-np/<pk>', delete_np, name='deletenp'),
    path("np-addpurchase/", add_n7purchase, name="addnp_purchase"),
    path("np7-list/", n7purchaselist, name="np_purchaselist"),
    path('delete-n7purchase/<pk>', delete_n7purchase, name='delete_np'),
    path("editnp_purchase/<pk>", edit_n7purchase, name="edit_n7purchase"),
    path("add_npsale/", ad_np7sale, name="add_n7sales"),
    path("np_saleslist/", np_salelist, name="np_salelist"),
    path('delete-npsale/<pk>', delete_npsale, name='deletenpsale'),
    path("edit-npsale/<pk>", edit_npsale, name="editnpsale"),
    
    
    
    
    
    
    
    
    
    path("add-product/", addproduct, name="addproduct"),
    path("edit-product/<pk>", editproduct, name="editproduct"),
    path("product-list/", productlist, name="productlist"),
    path('delete/<pk>', delete_product, name='deleteproduct'),
    
    path("add-purchase/", addpurchase, name="addpurchase"),
    path("edit-purchase/<pk>", edit_purchase, name="editpurchase"),
    path("purchase-list/", purchaselist, name="purchaselist"),
    path('delete-purchase/<pk>', delete_purchase, name='deletepurchase'),
    
    path("add-sale/", addsale, name="addsale"),
    path("edit-sale/<pk>", edit_sale, name="editsale"),
    path("sale-list/", salelist, name="salelist"),
    path('delete-sale/<pk>', delete_sale, name='deletesale'),
    
    path("add-type/", addtype, name="addtype"),
    path("type/", type, name="type"),
    path("edit-type/<pk>", edit_type, name="edittype"),
    path('delete-type/<pk>', delete_type, name='deletetype'),
    
    path("login/", Login, name="login"),
    path("logout/", logoutView, name="logout"),
    
    path("notifications/", notifications, name="notifications"),
    path('admin-profile/', edit_admin_profile, name='edit_admin'),
    
    path("add-customer/", addcustomer, name="addcutomer"),
    path("customer-list/", customer_list, name="customerlist"),
    
    path("delete-customer/<pk>", delete_customer, name="deletecustomer"),
    path("edit-customer/<pk>", editcutomer, name="editcustomer"),
    
    
    
    
    
    
    

    
]