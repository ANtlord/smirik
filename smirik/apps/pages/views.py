from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Page

class PageView(DetailView):
    model = Page
    template_name = "pages/simple.html"

    def get_object(self):
        page = get_object_or_404(Page, path=self.request.path)
        self.page = page
        return page

class HomepageView(PageView):
    template_name = "pages/homepage.html"
    def get_context_data(self, **kwagrs):
        ctx = super(HomepageView, self).get_context_data(**kwagrs)
        return ctx
