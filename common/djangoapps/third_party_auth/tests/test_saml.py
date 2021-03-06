"""
Unit tests for third_party_auth SAML auth providers
"""


import mock

from common.djangoapps.third_party_auth.saml import EdXSAMLIdentityProvider, get_saml_idp_class
from common.djangoapps.third_party_auth.tests.data.saml_identity_provider_mock_data import (
    expected_user_details,
    mock_attributes,
    mock_conf
)
from common.djangoapps.third_party_auth.tests.testutil import SAMLTestCase


class TestEdXSAMLIdentityProvider(SAMLTestCase):
    """
        Test EdXSAMLIdentityProvider.
    """
    @mock.patch('common.djangoapps.third_party_auth.saml.log')
    def test_get_saml_idp_class_with_fake_identifier(self, log_mock):
        error_mock = log_mock.error
        idp_class = get_saml_idp_class('fake_idp_class_option')
        error_mock.assert_called_once_with(
            u'[THIRD_PARTY_AUTH] Invalid EdXSAMLIdentityProvider subclass--'
            u'using EdXSAMLIdentityProvider base class. Provider: {provider}'.format(provider='fake_idp_class_option')
        )
        self.assertIs(idp_class, EdXSAMLIdentityProvider)

    def test_get_user_details(self):
        """ test get_attr and get_user_details of EdXSAMLIdentityProvider"""
        edx_saml_identity_provider = EdXSAMLIdentityProvider('demo', **mock_conf)
        self.assertEqual(edx_saml_identity_provider.get_user_details(mock_attributes), expected_user_details)
