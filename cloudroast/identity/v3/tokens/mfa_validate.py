from cafe.drivers.unittest.decorators import tags
from cafe.drivers.unittest.fixtures import BaseTestFixture
from cafe.drivers.unittest.datasets import DatasetList
from cafe.drivers.unittest.decorators import (
    tags, DataDrivenClass, data_driven_test)
from raxcafe.identity.v3.composites import IdentityV3Composite
from raxcafe.identity.v2_0.composites import IdentityV2Composite
from raxcafe.identity.config import (
    ServiceAdmin, IdentityAdmin, UserAdmin, UserManage, DefaultUser)


class UserDataset(DatasetList):

    def __init__(self):
        test_cases = [
            {"name": "ServiceAdmin", "data": {
                "get_service_catalog_resp": 200,
                "user_config": ServiceAdmin}},
            # {"name": "IdentityAdmin", "data": {
            #     "get_service_catalog_resp": 200,
            #     "user_config": IdentityAdmin}},
            {"name": "UserAdmin", "data": {
                "get_service_catalog_resp": 403,
                "user_config": UserAdmin}},
            {"name": "UserManage", "data": {
                "get_service_catalog_resp": 403,
                "user_config": UserManage}},
            {"name": "DefaultUser", "data": {
                "get_service_catalog_resp": 403,
                "user_config": DefaultUser}}]
        for test_case in test_cases:
            self.append_new_dataset(test_case["name"], test_case["data"])


@DataDrivenClass(UserDataset())
class MfaValidate(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the tests. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        user_config = None
        get_service_catalog_resp = None

        super(MfaValidate, cls).setUpClass()
        cls.v3_composite = IdentityV3Composite(cls.user_config)
        cls.v2_composite = IdentityV2Composite(IdentityAdmin)
        # cls.v2_composite.load_extensions()

    @tags('positive', type='regression')
    def test_auth_username_password(self):
        """
        Authentication with username and password
        """
        # resp = self.v2_composite.token_client.authenticate(
        #     username=self.v2_composite.user_config.username,
        #     password=self.v2_composite.user_config.password,)
        # self.assertEqual(resp.status_code, 200)
        token = self.v2_composite.token


        # validator = IdentityV3Composite(user_config)
        validate_token_resp = self.v3_composite.tokens_client.validate_token(token)
        self.assertEqual(validate_token_resp.status_code, self.get_service_catalog_resp)
