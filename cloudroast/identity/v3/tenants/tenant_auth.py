from cafe.drivers.unittest.decorators import tags
from cafe.drivers.unittest.fixtures import BaseTestFixture
from raxcafe.identity.v3.composites import IdentityV3Composite
from raxcafe.identity.v2_0.composites import IdentityV2Composite
from raxcafe.identity.config import ServiceAdmin, IdentityAdmin


class CreateTenant(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the tests. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(CreateTenant, cls).setUpClass()
        cls.v2_composite = IdentityV2Composite(IdentityAdmin)
        cls.v2_composite.load_extensions()

        cls.tenant_alias = ["{tenfant}", "Nast_{tenant}", '']

    @tags('positive', type='regression')
    def test_get_tenant_by_id(self):

        # for tenant in self.tenant_alias:
        #     resp = self.v2_composite.tenant_client.add_tenant(
        #         tenant_id="5352985", name=tenant, enabled=True,
        #            description="some_desc")
        #     self.assertEqual(resp.status_code, 409)

        resp = self.v2_composite.user_client.get_user_by_name(
            name="keystone_user_admin")
        self.assertEqual(resp.status_code, 200)


