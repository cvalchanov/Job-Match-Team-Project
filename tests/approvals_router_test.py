import unittest
from unittest.mock import Mock
from data.models import Admin, AdminApprovals, Company, Skill
from routers import approvals as approvals_router
from common.responses import BadRequest, NotFound, Unauthorized, NoContent

mock_approval_service = Mock('services.approval_services')
mock_auth = Mock()
approvals_router.approval_service = mock_approval_service
approvals_router.get_user_or_raise_401 = mock_auth

def fake_admin(id=1, username='admin', password='password'):
    mock_admin = Mock(spec=Admin)
    mock_admin.id = id
    mock_admin.username = username
    mock_admin.password = password
    return mock_admin

def fake_approval(id=1, type='type', name='name', category_id=1):
    mock_approval = Mock(spec=AdminApprovals)
    mock_approval.id = id
    mock_approval.type = type
    mock_approval.name = name
    mock_approval.category_id = category_id
    return mock_approval

def fake_company(id=1, username='comp', password='password', name='name', info='info', city_id=1):
    mock_company = Mock(spec=Company)
    mock_company.id = id
    mock_company.username = username
    mock_company.password = password
    mock_company.name = name
    mock_company.info = info
    mock_company.city_id = city_id
    return mock_company

class ApprovalsRouter_Should(unittest.TestCase):

    def setUp(self):
        mock_approval_service.reset_mock()
        mock_auth.reset_mock()

    def test_getApprovals_returns_listOf_AdminApprovals_when_dataPresent(self):
        admin = fake_admin()
        approval = fake_approval()
        mock_approval_service.all = lambda type: [approval]
        mock_auth.return_value = admin

        self.assertEqual([approval], approvals_router.get_approvals())

    def test_getApprovals_returns_Unauthorized_when_user_notAdmin(self):
        company = fake_company()
        mock_auth.return_value = company
        
        self.assertEqual(Unauthorized, type(approvals_router.get_approvals()))

    def test_getApprovals_return_BadRequest_when_noUser(self):
        mock_auth.return_value = None

        self.assertEqual(BadRequest, type(approvals_router.get_approvals()))

    def test_getApprovalById_returns_Approval_when_data(self):
        admin = fake_admin()
        approval = fake_approval()
        mock_auth.return_value = admin
        mock_approval_service.get_by_id = lambda id: approval

        self.assertEqual(approval, approvals_router.get_approval_by_id(id=1))

    def test_getApprovalById_returns_NotFound_when_noData(self):
        admin = fake_admin()
        mock_auth.return_value = admin
        mock_approval_service.get_by_id = lambda id: None

        self.assertEqual(NotFound, type(approvals_router.get_approval_by_id(id=1)))

    def test_getApprovalById_returns_Unauthorized_ifUser_notAdmin(self):
        company = fake_company()
        mock_auth.return_value = company

        self.assertEqual(Unauthorized, type(approvals_router.get_approval_by_id(id=1)))

    def test_getApprovalById_returns_BadRequest_when_noUser(self):
        mock_auth.return_value = None

        self.assertEqual(BadRequest, type(approvals_router.get_approval_by_id(id=1)))

    def test_createApproval_returns_Approval_when_successfull(self):
        company = fake_company()
        app = fake_approval()
        mock_auth.return_value = company
        mock_approval_service.create = lambda approval: app

        self.assertEqual(app, approvals_router.create_approval(approval=app))

    def test_createApproval_returns_BadRequest_when_creationFailed(self):
        company = fake_company()
        app = fake_approval()
        mock_auth.return_value = company
        mock_approval_service.create = lambda approval: None

        self.assertEqual(BadRequest, type(approvals_router.create_approval(approval=app)))

    def test_createApproval_returns_Unauthorized_when_noUser(self):
        app = fake_approval()

        mock_auth.return_value = None

        self.assertEqual(Unauthorized, type(approvals_router.create_approval(approval=app)))

    def test_approve_returns_object_when_successfull(self):
        admin = fake_admin()
        app = fake_approval()
        skill = Skill(id=1, name='skill', category_id=1)
        mock_auth.return_value = admin
        mock_approval_service.get_by_id = lambda id: app
        mock_approval_service.approve = lambda approval: skill

        self.assertEqual(skill, approvals_router.approve(id=1))

    def test_approve_returns_Unauthorized_when_userNotAdmin(self):
        company = fake_company()
        app = fake_approval()
        mock_auth.return_value = company
        mock_approval_service.get_by_id = lambda id: app

        self.assertEqual(Unauthorized, type(approvals_router.approve(id=1)))

    def test_approve_returns_BadRequest_when_noUser_or_noApproval(self):
        mock_auth.return_value = None
        mock_approval_service.get_by_id = lambda id: None

        self.assertEqual(BadRequest, type(approvals_router.approve(id=1)))

    def test_deleteApproval_returns_NoContent_when_successfullyDeleted(self):
        admin = fake_admin()
        app = fake_approval()
        mock_auth.return_value = admin
        mock_approval_service.get_by_id = lambda id: app
        mock_approval_service.delete = lambda approval: None

        self.assertEqual(NoContent, type(approvals_router.delete_approval(id=1)))

    def test_deleteApproval_returns_Unauthorized_when_userNotAdmin(self):
        company = fake_company()
        app = fake_approval()
        mock_auth.return_value = company
        mock_approval_service.get_by_id = lambda id: app

        self.assertEqual(Unauthorized, type(approvals_router.delete_approval(id=1)))

    def test_deleteApproval_returns_BadRequest_when_noUser_or_NoApproval(self):
        mock_auth.return_value = None
        mock_approval_service.get_by_id = lambda id: None

        self.assertEqual(BadRequest, type(approvals_router.delete_approval(id=1)))
