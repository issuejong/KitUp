from django.shortcuts import render


# 메인 화면
def main_view(request):
    """
    메인 화면 (main.html)
    - 비로그인: 컨텐츠들 제목 섹션 - 로그인 후 이용해보세요.
    - 로그인: 각 섹션 클릭 시 해당하는 html로 이동
    """
    return render(request, "main.html")
