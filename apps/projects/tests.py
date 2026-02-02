"""
팀 매칭 알고리즘 테스트
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

from apps.projects.models import Season, Project
from apps.projects.services import TeamMatchingService
from apps.accounts.models import User, Role, UserRoleLevel
from apps.teams.models import Team, TeamMember


class TeamMatchingServiceTest(TestCase):
    """팀 매칭 서비스 테스트"""
    
    def setUp(self):
        """테스트 데이터 준비"""
        # Role 생성
        self.pm_role = Role.objects.create(code='PM', name='기획')
        self.fe_role = Role.objects.create(code='FRONTEND', name='프론트엔드')
        self.be_role = Role.objects.create(code='BACKEND', name='백엔드')
        
        # Season 생성 (진행 중)
        now = timezone.now()
        self.season = Season.objects.create(
            name="테스트 시즌",
            status="MATCHING",
            is_active=True,
            matching_start=now - timedelta(days=1),
            matching_end=now + timedelta(days=1),
            project_start=now + timedelta(days=2),
            project_end=now + timedelta(days=30),
        )
    
    def _create_user(self, username, role, level, passion_level=3):
        """테스트 사용자 생성"""
        user = User.objects.create_user(
            username=username,
            email=f'{username}@test.com',
            password='test1234',
            nickname=username
        )
        user.passion_level = passion_level
        user.save()
        UserRoleLevel.objects.create(user=user, role=role, level=level)
        return user
    
    def test_matching_success_exact_count(self):
        """✅ 정확한 인원 매칭"""
        # PM 2명, FE 4명, BE 4명 생성 (팀 2개)
        for i in range(2):
            self._create_user(f'pm_{i}', self.pm_role, 3)
        for i in range(4):
            self._create_user(f'fe_{i}', self.fe_role, 2)
        for i in range(4):
            self._create_user(f'be_{i}', self.be_role, 2)
        
        result = TeamMatchingService.run_matching(self.season.id)
        
        self.assertEqual(result['teams_created'], 2)
        self.assertEqual(result['total_users_matched'], 10)
        self.assertEqual(result['pm_matched'], 2)
        self.assertEqual(result['fe_matched'], 4)
        self.assertEqual(result['be_matched'], 4)
        self.assertEqual(result['total_unmatched'], 0)
    
    def test_matching_partial_unmatched(self):
        """✅ 일부 인원 매칭 실패"""
        # PM 3명, FE 5명, BE 5명 생성 (팀 2개 + 1명씩 남음)
        for i in range(3):
            self._create_user(f'pm_{i}', self.pm_role, 3)
        for i in range(5):
            self._create_user(f'fe_{i}', self.fe_role, 2)
        for i in range(5):
            self._create_user(f'be_{i}', self.be_role, 2)
        
        result = TeamMatchingService.run_matching(self.season.id)
        
        self.assertEqual(result['teams_created'], 2)
        self.assertEqual(result['total_users_matched'], 10)
        self.assertEqual(result['total_unmatched'], 3)
        self.assertEqual(result['unmatched']['pm'], 1)
        self.assertEqual(result['unmatched']['fe'], 1)
        self.assertEqual(result['unmatched']['be'], 1)
    
    def test_matching_insufficient_pm(self):
        """❌ PM 부족 (매칭 불가)"""
        # PM 0명, FE 5명, BE 5명
        for i in range(5):
            self._create_user(f'fe_{i}', self.fe_role, 2)
        for i in range(5):
            self._create_user(f'be_{i}', self.be_role, 2)
        
        with self.assertRaises(ValidationError) as context:
            TeamMatchingService.run_matching(self.season.id)
        
        self.assertIn('팀을 만들 수 없습니다', str(context.exception))
    
    def test_matching_no_applicants(self):
        """❌ 지원자 없음"""
        with self.assertRaises(ValidationError) as context:
            TeamMatchingService.run_matching(self.season.id)
        
        self.assertIn('지원자가 없습니다', str(context.exception))
    
    def test_matching_level_sorting(self):
        """✅ 역할 레벨 기준 정렬 확인"""
        # PM 2명 (레벨 1, 3)
        pm1 = self._create_user('pm_low', self.pm_role, 1)
        pm2 = self._create_user('pm_high', self.pm_role, 3)
        
        # FE 4명
        for i in range(4):
            self._create_user(f'fe_{i}', self.fe_role, 2)
        
        # BE 4명
        for i in range(4):
            self._create_user(f'be_{i}', self.be_role, 2)
        
        result = TeamMatchingService.run_matching(self.season.id)
        
        # 팀 생성 확인
        teams = Team.objects.all()
        self.assertEqual(teams.count(), 2)
        
        # 첫 번째 팀에 높은 레벨 PM이 배정되는지 확인
        first_team = teams.first()
        pm_member = first_team.members.filter(role=self.pm_role).first()
        self.assertEqual(pm_member.user.nickname, 'pm_high')
    
    def test_team_composition(self):
        """✅ 팀 구성 검증 (PM1, FE2, BE2)"""
        # PM 1명, FE 2명, BE 2명
        self._create_user('pm_1', self.pm_role, 2)
        self._create_user('fe_1', self.fe_role, 2)
        self._create_user('fe_2', self.fe_role, 2)
        self._create_user('be_1', self.be_role, 2)
        self._create_user('be_2', self.be_role, 2)
        
        result = TeamMatchingService.run_matching(self.season.id)
        
        team = Team.objects.first()
        members = team.members.all()
        
        pm_count = members.filter(role=self.pm_role).count()
        fe_count = members.filter(role=self.fe_role).count()
        be_count = members.filter(role=self.be_role).count()
        
        self.assertEqual(pm_count, 1)
        self.assertEqual(fe_count, 2)
        self.assertEqual(be_count, 2)

