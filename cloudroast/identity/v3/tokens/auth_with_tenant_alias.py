from cafe.drivers.unittest.datasets import DatasetList
from cafe.drivers.unittest.decorators import DataDrivenClass
from cafe.drivers.unittest.decorators import tags
from cafe.drivers.unittest.fixtures import BaseTestFixture
from raxcafe.identity.config import DefaultUser
from raxcafe.identity.config import IdentityAdmin
from raxcafe.identity.config import ServiceAdmin
from raxcafe.identity.config import UserAdmin
from raxcafe.identity.config import UserManage
from raxcafe.identity.v3.composites import IdentityV3Composite


class ValidateDataset(DatasetList):
    def __init__(self):
        test_cases = [
            {"name": "ServiceAdmin", "data": {
                "not_found_exp_resp": 404,
                "invalid_token_exp_resp": 401,
                "user_config": ServiceAdmin}},
            {"name": "IdentityAdmin", "data": {
                "not_found_exp_resp": 404,
                "invalid_token_exp_resp": 401,
                "user_config": IdentityAdmin}},
            {"name": "UserAdmin", "data": {
                "not_found_exp_resp": 404,
                "invalid_token_exp_resp": 401,
                "user_config": UserAdmin}},
            {"name": "UserManage", "data": {
                "not_found_exp_resp": 404,
                "invalid_token_exp_resp": 401,
                "user_config": UserManage}},
            {"name": "DefaultUser", "data": {
                "not_found_exp_resp": 404,
                "invalid_token_exp_resp": 401,
                "user_config": DefaultUser}}]
        for test_case in test_cases:
            self.append_new_dataset(test_case["name"], test_case["data"])


@DataDrivenClass(ValidateDataset())
class TestNegativeToken(BaseTestFixture):
    """Test Class for validate test cases."""
    user_config = None

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the tests. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(TestNegativeToken, cls).setUpClass()
        cls.v3_composite = IdentityV3Composite(cls.user_config)

    @tags('negative', type='regression')
    def test_auth_with_tenant(self):
        """ Validate bad token """

        resp = self.v3_composite.tokens_client.validate_token(bad_token)
        status_code = resp.status_code
        self.assertEqual(status_code, self.not_found_exp_resp)

    @tags('negative', type='regression')
    def test_get_service_catalog_with_invalid_token(self):
        """ Test catalog with invalid token """
        self.v3_composite.catalog_client.token = 'bad token'
        resp = self.v3_composite.catalog_client.get_catalog()
        self.assertEqual(resp.status_code, self.invalid_token_exp_resp)

    @tags('negative', type='regression')
    def test_validate_with_bad_token(self):
        """ Validate token with invalid token """
        self.v3_composite.tokens_client.token = 'bad token'
        validate_token_resp = self.v3_composite.tokens_client.validate_token(
            self.v3_composite.token)
        status_code = validate_token_resp.status_code
        self.assertEqual(status_code, self.invalid_token_exp_resp)
