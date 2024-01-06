from rest_framework.pagination import PageNumberPagination

class HistoryPagination(PageNumberPagination):
    page_size = 3
    max_page_size = 20
