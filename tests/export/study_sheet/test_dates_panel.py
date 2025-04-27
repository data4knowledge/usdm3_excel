from unittest.mock import MagicMock, patch
from datetime import date

from usdm3_excel.export.study_sheet.dates_panel import DatesPanel
from usdm4_excel.export.base.ct_version import CTVersion


class TestDatesPanel:
    """Tests for the DatesPanel class."""

    def test_init(self):
        """Test initialization of DatesPanel."""
        # Create a CTVersion instance
        ct_version = CTVersion()
        ct_version.add("test", "1.0.0")

        # Create a DatesPanel instance
        panel = DatesPanel(ct_version)

        # Verify that the CTVersion instance is stored correctly
        assert panel.ct_version is ct_version
        assert panel.ct_version.versions["test"] == "1.0.0"

    def test_execute(self):
        """Test the execute method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a DatesPanel instance
        panel = DatesPanel(ct_version)

        # Create mock objects
        mock_study = MagicMock()
        mock_version = MagicMock()
        mock_amendment = MagicMock()
        mock_document = MagicMock()
        mock_doc_version = MagicMock()

        # Create mock date values
        mock_study_date = MagicMock()
        mock_amendment_date = MagicMock()
        mock_doc_date = MagicMock()

        # Configure the mock objects
        mock_study.versions = [mock_version]
        mock_study.documentedBy = [mock_document]

        mock_version.dateValues = [mock_study_date]
        mock_version.amendments = [mock_amendment]

        mock_amendment.dateValues = [mock_amendment_date]

        mock_document.versions = [mock_doc_version]
        mock_doc_version.dateValues = [mock_doc_date]

        # Mock the _add_date method
        with patch.object(panel, "_add_date") as mock_add_date:
            # Call the execute method
            panel.execute(mock_study)

            # Verify that _add_date was called with the correct arguments
            mock_add_date.assert_any_call([], mock_study_date, "study_version")
            mock_add_date.assert_any_call([], mock_amendment_date, "amendment")
            mock_add_date.assert_any_call([], mock_doc_date, "protocol_document")

    def test_add_date(self):
        """Test the _add_date method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a DatesPanel instance
        panel = DatesPanel(ct_version)

        # Create a mock collection and date
        collection = []
        mock_date = MagicMock()
        mock_date.model_dump.return_value = {
            "name": "Test Date",
            "description": "Test Description",
            "label": "Test Label",
            "type": "Test Type",
            "dateValue": date(2023, 1, 1),
            "geographicScopes": [],
        }

        # Mock the helper methods
        with (
            patch.object(panel, "_pt_from_code", return_value="Decoded Type") as mock_pt_from_code,
            patch.object(panel, "_date_from_date", return_value="01/01/2023") as mock_date_from_date,
            patch.object(panel, "_scopes", return_value="Global") as mock_scopes,
        ):
            # Call the _add_date method
            panel._add_date(collection, mock_date, "test_category")

            # Verify that the helper methods were called with the correct arguments
            mock_pt_from_code.assert_called_once_with(mock_date.type)
            mock_date_from_date.assert_called_once_with(mock_date.dateValue)
            mock_scopes.assert_called_once_with(mock_date.geographicScopes)

            # Verify that the collection was updated correctly
            assert len(collection) == 1
            assert collection[0]["category"] == "test_category"
            assert collection[0]["type"] == "Decoded Type"
            assert collection[0]["date"] == "01/01/2023"
            assert collection[0]["scopes"] == "Global"

    def test_date_from_date(self):
        """Test the _date_from_date method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a DatesPanel instance
        panel = DatesPanel(ct_version)

        # Call the _date_from_date method with a test date
        test_date = date(2023, 1, 1)
        result = panel._date_from_date(test_date)

        # Verify the result
        assert result == "01/01/2023"

    def test_scopes(self):
        """Test the _scopes method."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a DatesPanel instance
        panel = DatesPanel(ct_version)

        # Create mock scopes
        mock_global_scope = MagicMock()
        mock_global_scope.type.decode = "Global"

        mock_country_scope = MagicMock()
        mock_country_scope.type.decode = "Country"
        mock_country_scope.code.standardCode.decode = "United States"

        # Call the _scopes method with the mock scopes
        result = panel._scopes([mock_global_scope, mock_country_scope])

        # Verify the result
        assert result == "Global, Country: United States"

    def test_scopes_empty(self):
        """Test the _scopes method with no scopes."""
        # Create a CTVersion instance
        ct_version = CTVersion()

        # Create a DatesPanel instance
        panel = DatesPanel(ct_version)

        # Call the _scopes method with an empty list
        result = panel._scopes([])

        # Verify the result
        assert result == ""
