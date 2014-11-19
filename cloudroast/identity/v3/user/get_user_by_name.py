from cafe.drivers.unittest.datasets import DatasetList
from cafe.drivers.unittest.decorators import (
    tags, DataDrivenClass)
from cafe.drivers.unittest.fixtures import BaseTestFixture

from raxcafe.identity.config import (
    ServiceAdmin, IdentityAdmin, UserAdmin, UserManage, DefaultUser)
from raxcafe.identity.v3.composites import IdentityV3Composite
from raxcafe.identity.v2_0.composites import IdentityV2Composite


class UserDataset(DatasetList):

    def __init__(self):
        test_cases = [
            {"name": "v3ServiceAdmin", "data": {
                "get_user_name_resp": 200, "client": "v3",
                "user_config": ServiceAdmin}},
            {"name": "v3IdentityAdmin", "data": {
                "get_user_name_resp": 200, "client": "v3",
                "user_config": IdentityAdmin}},
            {"name": "v3UserAdmin", "data": {
                "get_user_name_resp": 200, "client": "v3",
                "user_config": UserAdmin}},
            {"name": "v3UserManage", "data": {
                "get_user_name_resp": 200, "client": "v3",
                "user_config": UserManage}},
            {"name": "v3DefaultUser", "data": {
                "get_user_name_resp": 200, "client": "v3",
                "user_config": DefaultUser}},
            {"name": "ServiceAdmin", "data": {
                "get_user_name_resp": 200, "client": "v2",
                "user_config": ServiceAdmin}},
            {"name": "IdentityAdmin", "data": {
                "get_user_name_resp": 200, "client": "v2",
                "user_config": IdentityAdmin}},
            {"name": "UserAdmin", "data": {
                "get_user_name_resp": 200, "client": "v2",
                "user_config": UserAdmin}},
            {"name": "UserManage", "data": {
                "get_user_name_resp": 200, "client": "v2",
                "user_config": UserManage}},
            {"name": "DefaultUser", "data": {
                "get_user_name_resp": 200, "client": "v2",
                "user_config": DefaultUser}}]
        for test_case in test_cases:
            self.append_new_dataset(test_case["name"], test_case["data"])


@DataDrivenClass(UserDataset())
class TestGetUserById(BaseTestFixture):
    """

    """
    user_config = None

    @classmethod
    def setUpClass(cls):
        """

        """
        super(TestGetUserById, cls).setUpClass()
        cls.clients = {}
        cls.v3_composite = IdentityV3Composite(cls.user_config)
        cls.v2_composite = IdentityV2Composite(cls.user_config)
        cls.v2_composite.load_extensions()
        cls.clients['v3'] = cls.v3_composite
        cls.clients['v2'] = cls.v2_composite

    @tags('positive', type='regression')
    def test_get_user_by_id(self):
        v2_client = self.v2_composite
        v2_client.user_client.token = self.clients[self.client].token
        resp = v2_client.user_client.get_user_by_name(
                name=v2_client.user_config.username)
        self.assertEqual(resp.status_code, self.get_user_name_resp)


    # @tags('positive', type='regression')
    # def test_get_user_by_name(self):
    #     #token = self.v3_composite.token
    #     resp = self.v3_composite.user_client.get_user_by_name(
    #        name=self.v3_composite.user_config.username)
    #     self.assertEqual(resp.status_code, 200)
