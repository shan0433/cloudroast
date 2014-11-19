from cafe.drivers.unittest.datasets import DatasetList
from cafe.drivers.unittest.decorators import tags, DataDrivenFixture, \
    data_driven_test
from cafe.drivers.unittest.fixtures import BaseTestFixture

from cloudcafe.identity.common.constants import (
    IdentityUserConstants, InvalidAttributes)
from cloudcafe.identity.v3.composites import IdentityV3Composite
from cloudcafe.identity.v3.config import IdentityAdmin, UserAdmin
from cloudroast.identity.v3.tokens.data_example import TestScenario


@DataDrivenFixture
class TestAuth(BaseTestFixture):
    """

    """

    USER_ID, PASSWORD, USER_DOMAIN_ID, USER_DOMAIN_NAME, DOMAIN_ID, DOMAIN_NAME, PROJECT_ID, PROJECT_NAME, EXPECTED_RESPONSE = ('user_id', 'password', 'user_domain_id', 'user_domain_name', 'domain_id', 'domain_name', 'project_id', 'project_name', 'expected_response')

    invalid_dict = {
        IdentityUserConstants.USER_ADMIN:
            [[USER_ID, InvalidAttributes.DOES_NOT_EXIST, DOMAIN_ID, DOMAIN_NAME, PROJECT_ID, PROJECT_NAME, 401],
             [InvalidAttributes.DOES_NOT_EXIST, PASSWORD, DOMAIN_ID, DOMAIN_NAME, PROJECT_ID, PROJECT_NAME, 401],
             [USER_ID, PASSWORD, DOMAIN_ID, DOMAIN_NAME, InvalidAttributes.DOES_NOT_EXIST, PROJECT_NAME, 401],
             [USER_ID, PASSWORD, DOMAIN_ID, DOMAIN_NAME, InvalidAttributes.INCORRECT, PROJECT_NAME, 401],
             [USER_ID, PASSWORD, DOMAIN_ID, DOMAIN_NAME, PROJECT_ID, InvalidAttributes.DOES_NOT_EXIST, 401],
             [USER_ID, PASSWORD, DOMAIN_ID, InvalidAttributes.DOES_NOT_EXIST, PROJECT_ID, PROJECT_NAME, 401],
             [USER_ID, PASSWORD, InvalidAttributes.DOES_NOT_EXIST, DOMAIN_NAME, PROJECT_ID, PROJECT_NAME, 401],
             [USER_ID, PASSWORD, DOMAIN_ID, DOMAIN_NAME, PROJECT_ID, InvalidAttributes.INCORRECT, 401],
             [USER_ID, PASSWORD, DOMAIN_ID, InvalidAttributes.INCORRECT, PROJECT_ID, PROJECT_NAME, 401],
             [USER_ID, PASSWORD, InvalidAttributes.INCORRECT, DOMAIN_NAME, PROJECT_ID, PROJECT_NAME, 401]]}

    invalid_dataset_list = DatasetList()
    for client_type, user_data in (invalid_dict.iteritems()):
        for data in user_data:
            suffix_test_name = (
                'user_{0}_password_{1}_domain_id_{2}_domain_name_{3}_project_id_{4}_project_name_{5}'.format(
                    data[0], data[1], data[2], data[3], data[4], data[5]))
            data_type_for_test = {
                'data_object': TestScenario(user_id=data[0], password=data[1],
                              domain_id=data[2], domain_name=data[3],
                              project_id=data[4], project_name=data[5],
                              expected_response=data[6])}

            invalid_dataset_list.append_new_dataset(
                suffix_test_name, data_type_for_test)

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the tests. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(TestAuth, cls).setUpClass()
        cls.user_config = UserAdmin
        cls.v3_composite = IdentityV3Composite(cls.user_config)

        cls.user_map_domain_1 = {
            cls.USER_ID: cls.v3_composite.user_config.user_id,
            cls.PASSWORD: cls.v3_composite.user_config.password,
            cls.DOMAIN_ID: cls.v3_composite.user_config.domain_id,
            cls.DOMAIN_NAME: cls.v3_composite.user_config.domain_name,
            cls.PROJECT_ID: cls.v3_composite.user_config.domain_id,
            cls.PROJECT_NAME: cls.v3_composite.user_config.domain_name}

        cls.user_config = IdentityAdmin
        cls.composite = IdentityV3Composite(cls.user_config)
        cls.user_map_domain_2 = {
            cls.USER_ID: cls.composite.user_config.user_id,
            cls.PASSWORD: cls.composite.user_config.password,
            cls.DOMAIN_ID: cls.composite.user_config.domain_id,
            cls.DOMAIN_NAME: cls.composite.user_config.domain_name,
            cls.PROJECT_ID: cls.composite.user_config.domain_id,
            cls.PROJECT_NAME: cls.composite.user_config.domain_name}

    @tags('negative', type='regression')
    @data_driven_test(invalid_dataset_list)
    def ddtest_auth_name_password_domain_id(self, data_object):
        """
        Authentication with username, password and the domain id of the user
        """

        data_object.populate_data([self.user_map_domain_1,
                                   self.user_map_domain_2])

        if not data_object.project_name_valid:
            resp = self.v3_composite.tokens_client.authenticate(
                user_id=data_object.user_id,
                password=data_object.password,
                project_id=data_object.project_id, scope=data_object.scope)
            self.assertEqual(resp.status_code, data_object.expected_response)

        if not data_object.project_id_valid:
            if not data_object.domain_name_valid:
                resp = self.v3_composite.tokens_client.authenticate(
                    user_id=data_object.user_id, password=data_object.password,
                    project_name=data_object.project_name,
                    project_domain_id=data_object.domain_id, scope=True)
                self.assertEqual(resp.status_code,
                                 data_object.expected_response)

            if not data_object.domain_id_valid:
                resp = self.v3_composite.tokens_client.authenticate(
                    user_id=data_object.user_id, password=data_object.password,
                    project_name=data_object.project_name,
                    project_domain_name=data_object.domain_name, scope=True)
                self.assertEqual(resp.status_code,
                                 data_object.expected_response)
