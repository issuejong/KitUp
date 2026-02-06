import json
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'JSON 파일에서 가이드 데이터를 로드합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='기존 가이드 데이터를 먼저 삭제합니다',
        )

    def handle(self, *args, **options):
        # 기존 데이터 삭제 옵션
        if options['reset']:
            from apps.guides.models import GuideCard, GuideTask
            GuideCard.objects.all().delete()
            GuideTask.objects.all().delete()
            self.stdout.write(self.style.WARNING('기존 가이드 데이터를 삭제했습니다'))

        # fixture 로드
        try:
            call_command('loaddata', 'guides')
            self.stdout.write(
                self.style.SUCCESS('✅ 가이드 데이터를 성공적으로 로드했습니다!')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ 오류: {e}'))
