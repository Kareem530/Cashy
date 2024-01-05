JAZZMIN_SETTINGS = {
    "site_title": "Cashy Admin Portal",
    "site_header": "Admin Portal",
    "site_brand": "Admin Portal",
    "welcome_sign": "Welcome to the Cashy Admin Portal",
    "copyright": "Cashy",
    "search_model": ["accounts.User","bills.BillCompany"],
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "accounts.User"}
    ],
    "usermenu_links": [
        {"model": "accounts.user"}
    ],
}