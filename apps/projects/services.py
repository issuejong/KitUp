"""
팀 매칭 알고리즘 및 관련 서비스
"""
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.accounts.models import User, Role, UserRoleLevel
from apps.projects.models import Season, Project
from apps.teams.models import Team, TeamMember


class TeamMatchingService:
    """팀 매칭 알고리즘 서비스"""
    
    TEAM_SIZE = 5
    PM_COUNT_PER_TEAM = 1
    FE_COUNT_PER_TEAM = 2
    BE_COUNT_PER_TEAM = 2
    
    @staticmethod
    def run_matching(season_id):
        """
        팀 매칭 실행
        
        Args:
            season_id: Season ID
            
        Returns:
            dict: 매칭 결과 통계
            
        Raises:
            ValidationError: 지원자 부족 등 조건 미충족
        """
        season = Season.objects.get(id=season_id)
        
        # 1️⃣ passion_level이 설정된 지원자만 필터링
        applicants = User.objects.filter(
            passion_level__isnull=False
        ).select_related()
        
        if not applicants.exists():
            raise ValidationError("팀매칭 지원자가 없습니다.")
        
        # 2️⃣ 역할별로 그룹화
        pm_candidates = TeamMatchingService._get_role_candidates(
            applicants, 'PM'
        )
        fe_candidates = TeamMatchingService._get_role_candidates(
            applicants, 'FRONTEND'
        )
        be_candidates = TeamMatchingService._get_role_candidates(
            applicants, 'BACKEND'
        )
        
        # 3️⃣ 가능한 최대 팀 개수 계산
        # PM 기준, FE 기준, BE 기준 중 최소값
        max_teams_by_pm = len(pm_candidates) // TeamMatchingService.PM_COUNT_PER_TEAM
        max_teams_by_fe = len(fe_candidates) // TeamMatchingService.FE_COUNT_PER_TEAM
        max_teams_by_be = len(be_candidates) // TeamMatchingService.BE_COUNT_PER_TEAM
        
        num_teams = min(max_teams_by_pm, max_teams_by_fe, max_teams_by_be)
        
        if num_teams == 0:
            raise ValidationError(
                f"팀을 만들 수 없습니다. (최소 조건: PM {TeamMatchingService.PM_COUNT_PER_TEAM}명, "
                f"FE {TeamMatchingService.FE_COUNT_PER_TEAM}명, BE {TeamMatchingService.BE_COUNT_PER_TEAM}명) "
                f"현재: PM {len(pm_candidates)}명, FE {len(fe_candidates)}명, BE {len(be_candidates)}명"
            )
        
        # 4️⃣ 트랜잭션 내에서 팀 생성 및 멤버 배정
        with transaction.atomic():
            teams_created = []
            pm_idx = 0
            fe_idx = 0
            be_idx = 0
            
            for team_num in range(num_teams):
                # 프로젝트 생성
                project = Project.objects.create(
                    title=f"{season.name} 팀 {team_num + 1}",
                    description=f"자동 매칭된 팀 프로젝트",
                    status='MATCHED',
                )
                
                # 팀 생성
                team = Team.objects.create(
                    project=project,
                    name=f"Team {team_num + 1}",
                )
                
                # PM 배정
                for _ in range(TeamMatchingService.PM_COUNT_PER_TEAM):
                    if pm_idx < len(pm_candidates):
                        pm_user = pm_candidates[pm_idx]
                        TeamMember.objects.create(
                            team=team,
                            user=pm_user,
                            role=Role.objects.get(code='PM'),
                        )
                        pm_idx += 1
                
                # FE 배정
                for _ in range(TeamMatchingService.FE_COUNT_PER_TEAM):
                    if fe_idx < len(fe_candidates):
                        fe_user = fe_candidates[fe_idx]
                        TeamMember.objects.create(
                            team=team,
                            user=fe_user,
                            role=Role.objects.get(code='FRONTEND'),
                        )
                        fe_idx += 1
                
                # BE 배정
                for _ in range(TeamMatchingService.BE_COUNT_PER_TEAM):
                    if be_idx < len(be_candidates):
                        be_user = be_candidates[be_idx]
                        TeamMember.objects.create(
                            team=team,
                            user=be_user,
                            role=Role.objects.get(code='BACKEND'),
                        )
                        be_idx += 1
                
                teams_created.append(team)
        
        # 매칭되지 않은 인원 계산
        unmatched = {
            'pm': len(pm_candidates) - pm_idx,
            'fe': len(fe_candidates) - fe_idx,
            'be': len(be_candidates) - be_idx,
        }
        
        return {
            'teams_created': len(teams_created),
            'total_users_matched': (
                pm_idx +
                fe_idx +
                be_idx
            ),
            'pm_matched': pm_idx,
            'fe_matched': fe_idx,
            'be_matched': be_idx,
            'unmatched': unmatched,
            'total_unmatched': sum(unmatched.values()),
        }
    
    @staticmethod
    def _get_role_candidates(applicants, role_code):
        """
        특정 역할의 지원자를 역할 레벨 기준으로 정렬
        
        Args:
            applicants: User QuerySet
            role_code: 'PM' | 'FRONTEND' | 'BACKEND'
            
        Returns:
            list: 정렬된 User 객체 리스트 (역할 레벨 내림차순)
        """
        role = Role.objects.get(code=role_code)
        
        candidates = []
        for user in applicants:
            # 해당 역할의 레벨 조회
            role_level = UserRoleLevel.objects.filter(
                user=user,
                role=role
            ).first()
            
            if role_level:
                candidates.append({
                    'user': user,
                    'level': role_level.level,
                })
        
        # 역할 레벨 내림차순 정렬 (좋은 사람 우선)
        candidates.sort(key=lambda x: x['level'], reverse=True)
        
        return [c['user'] for c in candidates]
