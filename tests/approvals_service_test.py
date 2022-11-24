import unittest
from unittest.mock import Mock
from data.models import AdminApprovals, Skill, SkillCategory, Location, ApprovalType
from services import approval_service
from mariadb import IntegrityError

mock_skill_service = Mock('services.skill_service')
mock_location_service = Mock('services.location_service')
mock_delete = Mock()
approval_service.location_service = mock_location_service
approval_service.skill_service = mock_skill_service
approval_service.delete = mock_delete

class ApprovalService_Should(unittest.TestCase):

    def setUp(self):
        mock_skill_service.reset_mock()
        mock_location_service.reset_mock()

    def test_all_returns_list_ofApprovals_whenData(self):
        get_data_func = lambda q: [(1, 'type1', 'name1', 1), (2, 'type2', 'name2', 2)]
        expected = [AdminApprovals(id=1, type='type1', name='name1', category_id=1),
                    AdminApprovals(id=2, type='type2', name='name2', category_id=2)]
        result = approval_service.all(get_data_func=get_data_func)

        self.assertEqual(expected, result)
        self.assertEqual(expected[0], result[0])
        self.assertEqual(expected[1], result[1])
        self.assertEqual(2, len(result))

    def test_all_returns_emptyList_when_noData(self):
        get_data_func = lambda q: []

        self.assertEqual([], approval_service.all(get_data_func=get_data_func))

    def test_getById_returns_Approval_whenData(self):
        get_data_func = lambda q, id: [(1, 'type1', 'name1', 1)]
        expected = AdminApprovals(id=1, type='type1', name='name1', category_id=1)
        result = approval_service.get_by_id(id=1, get_data_func=get_data_func)

        self.assertEqual(expected, result)

    def test_getById_returns_None_when_noData(self):
        get_data_func = lambda q, id: []

        self.assertEqual(None, approval_service.get_by_id(id=1, get_data_func=get_data_func))

    def test_create_returns_Approval_when_successfully_created(self):
        app = AdminApprovals(type='type1', name='name1', category_id=1)
        insert_data_func = lambda q, a: 1
        expected = AdminApprovals(id=1, type='type1', name='name1')
        result = approval_service.create(approval=app, insert_data_func=insert_data_func)

        self.assertEqual(expected, result)

    def test_create_returns_None_when_IntegrityError(self):
        app = AdminApprovals(type='type1', name='name1', category_id=1)        
        def insert_data_func(q,a):
            raise IntegrityError

        self.assertEqual(None, approval_service.create(approval=app, insert_data_func=insert_data_func))

    def test_update_returns_updatedApproval(self):
        app1 = AdminApprovals(id=1, type='type1', name='name1', category_id=1)
        app2 = AdminApprovals(id=2, type='type2', name='name2', category_id=2)

        update_data_func = lambda q,a: None

        expected = AdminApprovals(id=app1.id, type=app2.type, name=app2.name, category_id=app2.category_id)
        result = approval_service.update(old=app1, new=app2, update_data_func=update_data_func)

        self.assertEqual(expected, result)

    def test_approve_returns_skillCategory_when_approvalType_isSkillCategory(self):
        skill_category = SkillCategory(id=1, name='name')
        app = AdminApprovals(id=1, type=ApprovalType.SKILL_CATEGORY, name='name')
        mock_skill_service.create_skill_category = lambda name: skill_category
        mock_delete.return_value = None

        self.assertEqual(skill_category, approval_service.approve(approval=app))

    def test_approve_returns_skill_when_approvalType_isSkill(self):
        skill = Skill(id=1, name='name', category_id=1)
        app = AdminApprovals(id=1, type=ApprovalType.SKILL, name='name', category_id=1)
        mock_skill_service.create_skill = lambda name, skill_category_id: skill
        mock_delete.return_value = None

        self.assertEqual(skill, approval_service.approve(approval=app))

    def test_approve_returns_location_when_approvalType_isLocation(self):
        location = Location(id=1, name='name')
        app = AdminApprovals(id=1, type=ApprovalType.CITY, name='name')
        mock_location_service.create_location = lambda name: location
        mock_delete.return_value = None

        self.assertEqual(location, approval_service.approve(approval=app))