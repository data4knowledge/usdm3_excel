from unittest.mock import MagicMock, patch

from usdm3_excel.export.study_identifiers_sheet.identifiers_panel import (
    IdentifiersPanel,
)
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4.api.identifier import StudyIdentifier
from usdm4.api.organization import Organization
from usdm4.api.address import Address


class TestIdentifiersPanel:
    """Tests for the IdentifiersPanel class."""

    def test_init(self):
        """Test initialization of IdentifiersPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create an IdentifiersPanel instance
        panel = IdentifiersPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute(self):
        """Test the execute method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an IdentifiersPanel instance
        panel = IdentifiersPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_identifier = MagicMock(spec=StudyIdentifier)

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_version.studyIdentifiers = [mock_identifier]

        # Mock the _add_identifier method
        with patch.object(panel, "_add_identifier") as mock_add_identifier:
            # Call the execute method
            panel.execute(mock_study)

            # Verify that _add_identifier was called with the correct arguments
            mock_add_identifier.assert_called_once_with(
                [], mock_identifier, mock_version
            )

    def test_add_identifier(self):
        """Test the _add_identifier method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an IdentifiersPanel instance
        panel = IdentifiersPanel(ct_version)

        # Create mock objects
        collection = []
        mock_identifier = MagicMock(spec=StudyIdentifier)
        mock_version = MagicMock()
        mock_organization = MagicMock(spec=Organization)

        # Configure the mock objects
        mock_identifier.scopeId = "org123"
        mock_identifier.text = "Study-123"

        mock_version.organization.return_value = mock_organization

        # Set the attributes directly on the mock_organization
        mock_organization.type = MagicMock()
        mock_organization.legalAddress = MagicMock(spec=Address)

        mock_organization.model_dump.return_value = {
            "identifierScheme": "Scheme-123",
            "identifier": "Org-123",
            "name": "Test Organization",
            "type": mock_organization.type,
            "legalAddress": mock_organization.legalAddress,
        }

        # Mock the helper methods
        with (
            patch.object(
                panel, "_pt_from_code", return_value="Organization Type"
            ) as mock_pt_from_code,
            patch.object(
                panel,
                "_from_address",
                return_value="Address Line 1|City|State|12345|US",
            ) as mock_from_address,
        ):
            # Call the _add_identifier method
            panel._add_identifier(collection, mock_identifier, mock_version)

            # Verify that the helper methods were called with the correct arguments
            mock_pt_from_code.assert_called_once_with(mock_organization.type)
            mock_from_address.assert_called_once_with(mock_organization.legalAddress)

            # Verify that the collection was updated correctly
            assert len(collection) == 1
            assert collection[0]["organizationIdentifierScheme"] == "Scheme-123"
            assert collection[0]["organizationIdentifier"] == "Org-123"
            assert collection[0]["organizationName"] == "Test Organization"
            assert collection[0]["organizationType"] == "Organization Type"
            assert collection[0]["studyIdentifier"] == "Study-123"
            assert (
                collection[0]["organizationAddress"]
                == "Address Line 1|City|State|12345|US"
            )

    def test_from_address_with_address(self):
        """Test the _from_address method with a valid address."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an IdentifiersPanel instance
        panel = IdentifiersPanel(ct_version)

        # Create a mock address
        mock_address = MagicMock(spec=Address)
        mock_address.lines = ["123 Main St", "Suite 100"]
        mock_address.district = "District"
        mock_address.city = "City"
        mock_address.state = "State"
        mock_address.postalCode = "12345"

        # Set up the country attribute with nested mocks
        mock_country = MagicMock()
        mock_code = MagicMock()
        mock_code.code = "US"
        mock_country.code = mock_code
        mock_address.country = mock_country

        # Call the _from_address method
        result = panel._from_address(mock_address)

        # Verify the result
        assert result == "123 Main St|Suite 100|District|City|State|12345|US"

    def test_from_address_without_address(self):
        """Test the _from_address method with None address."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an IdentifiersPanel instance
        panel = IdentifiersPanel(ct_version)

        # Call the _from_address method with None
        result = panel._from_address(None)

        # Verify the result
        assert result == "|||||"

    def test_from_address_without_country(self):
        """Test the _from_address method with an address that has no country."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create an IdentifiersPanel instance
        panel = IdentifiersPanel(ct_version)

        # Create a mock address with no country
        mock_address = MagicMock(spec=Address)
        mock_address.lines = ["123 Main St"]
        mock_address.district = "District"
        mock_address.city = "City"
        mock_address.state = "State"
        mock_address.postalCode = "12345"
        mock_address.country = None

        # Call the _from_address method
        result = panel._from_address(mock_address)

        # Verify the result
        assert result == "123 Main St|District|City|State|12345|"
