from cloudcafe.identity.common.constants import (
    IdentityUserConstants, InvalidAttributes)

class TestScenario(object):

    USER_ID = IdentityUserConstants.USER_ID
    USERNAME = IdentityUserConstants.USERNAME
    PASSWORD = IdentityUserConstants.PASSWORD
    PROJECT_ID = IdentityUserConstants.PROJECT_ID
    PROJECT_NAME = IdentityUserConstants.PROJECT_NAME
    DOMAIN_ID = IdentityUserConstants.DOMAIN_ID
    DOMAIN_NAME = IdentityUserConstants.DOMAIN_NAME
    USER_DOMAIN_ID = IdentityUserConstants.USER_DOMAIN_ID
    USER_DOMAIN_NAME = IdentityUserConstants.USER_DOMAIN_NAME

    def __init__(self, password, user_id=None, username=None, project_id=None, project_name=None, user_domain_id=None,
                 user_domain_name=None, domain_name=None, domain_id=None, scope=True, expected_response=401):

        self.user_id = user_id
        self.password = password
        self.expected_response = expected_response
        self.scope = scope

        self.attr_mapping = {
                             # self.USERNAME: {'username': username},
                             self.PASSWORD: {'password': password},
                             self.PROJECT_ID: {'project_id': project_id},
                             self.PROJECT_NAME: {'project_name': project_name},
                             # self.USER_DOMAIN_ID: {'user_domain_id': user_domain_id},
                             # self.USER_DOMAIN_NAME: {'user_domain_name': user_domain_name},
                             self.USER_ID: {'user_id': user_id},
                             self.DOMAIN_ID: {'domain_id': domain_id},
                             self.DOMAIN_NAME: {'domain_name': domain_name}}

    def populate_data(self, domain_data_lists):

        for attr_const, attr_info in self.attr_mapping.iteritems():

            data_name = attr_info.keys()[0]
            if attr_info[data_name] == InvalidAttributes.INCORRECT:
                value = domain_data_lists[1][attr_const]
                valid = False
            elif attr_info[data_name] == InvalidAttributes.DOES_NOT_EXIST:
                value = attr_info[data_name]
                valid = False
            else:
                value = domain_data_lists[0][attr_const]
                valid = True

            setattr(self, data_name, value)
            setattr(self, '{0}_valid'.format(data_name), valid)
            setattr(self, '{0}_state'.format(data_name),
                    self.attr_mapping[attr_const][data_name])

        self.adjust_for_project_id_exceptions()
        self.adjust_for_project_name_exceptions()

        # self.adjust_for_user_domain_exceptions()
        # self.adjust_for_username_exceptions()
        # self.adjust_for_some_other_exceptions()

    def __repr__(self):
        msg = "This is a data object for ", self.project_name
        return msg

    def adjust_for_project_id_exceptions(self):
        # Project id validations
        if self.project_id_valid:
            if (self.user_id_state == InvalidAttributes.DOES_NOT_EXIST or
                    self.password_state == InvalidAttributes.DOES_NOT_EXIST):
                self.project_name_valid = False
                self.project_id_valid = False
                self.domain_name_valid = False
                self.domain_id_valid = False
        else:
            if (self.project_id_state == InvalidAttributes.DOES_NOT_EXIST or
                        self.project_id_state == InvalidAttributes.INCORRECT):
                self.project_name_valid = False

    def adjust_for_project_name_exceptions(self):
        # Project name validations
        if self.project_name_valid:
            if self.domain_name_valid:
                if (self.domain_id_state == InvalidAttributes.DOES_NOT_EXIST or
                        self.domain_id_state == InvalidAttributes.INCORRECT):
                    self.project_id_valid = False
                    self.domain_name_valid = False
                    self.domain_id_valid = True
            if self.domain_id_valid:
                if (self.domain_name_state == InvalidAttributes.DOES_NOT_EXIST
                    or self.domain_name_state == InvalidAttributes.INCORRECT):
                    self.project_id_valid = False
                    self.domain_name_valid = True
                    self.domain_id_valid = False
        else:
            if self.domain_id_valid:
                if (self.project_name_state == InvalidAttributes.DOES_NOT_EXIST
                    or self.project_name_state == InvalidAttributes.INCORRECT):
                    self.project_name_valid = True
                    self.project_id_valid = False
                    self.domain_name_valid = False
                    self.domain_id_valid = False

    def adjust_for_user_domain_exceptions(self):

        # Userid and password combinations
        if (self.user_id_state == InvalidAttributes.DOES_NOT_EXIST
            or self.password_state == InvalidAttributes.DOES_NOT_EXIST):
            self.user_domain_name_valid = False
            self.user_domain_id_valid = False

        if self.user_domain_id_state in [InvalidAttributes.DOES_NOT_EXIST,
                                         InvalidAttributes.INCORRECT]:
            self.user_domain_name_valid = False
            self.user_domain_id_valid = True

        if self.user_domain_name_state in [InvalidAttributes.DOES_NOT_EXIST,
                                           InvalidAttributes.INCORRECT]:
            self.user_domain_name_valid = True
            self.user_domain_id_valid = False

    def adjust_for_username_exceptions(self):

        # Username and password combinations
        if (self.username_state == InvalidAttributes.DOES_NOT_EXIST
            or self.password_state == InvalidAttributes.DOES_NOT_EXIST):
            self.user_domain_name_valid = False
            self.user_domain_id_valid = False

        if self.user_domain_id_state in [InvalidAttributes.DOES_NOT_EXIST,
                                         InvalidAttributes.INCORRECT]:
            self.user_domain_name_valid = False
            self.user_domain_id_valid = True

        if self.user_domain_name_state in [InvalidAttributes.DOES_NOT_EXIST,
                                           InvalidAttributes.INCORRECT]:
            self.user_domain_name_valid = True
            self.user_domain_id_valid = False


    def adjust_for_some_other_exceptions(self):
        pass
