from django.views.generic import TemplateView

# 테스트용 기본 템플릿
class initial_view(TemplateView):
    template_name = "initial.html"
