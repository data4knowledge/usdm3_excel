from .content_panel import DocumentContentPanel
from usdm4.api.study import Study
from usdm4.api.study_definition_document_version import StudyDefinitionDocumentVersion
from usdm4.api.narrative_content import NarrativeContent, NarrativeContentItem
from usdm3_excel.export.base.base_sheet import BaseSheet


class StudyDocumentContentSheet(BaseSheet):
    SHEET_NAME = "studyDesignContent"

    def save(self, study: Study):
        op = contentPanel(self.ct_version)
        result = op.execute(study)
        last_row = self.etw.add_table(result, self.SHEET_NAME)
        self.etw.format_cells(
            self.SHEET_NAME,
            (2, 1, last_row, 2),
            wrap_text=True,
            vertical_alignment="top",
        )
        self.etw.format_cells(
            self.SHEET_NAME,
            (1, 1, 1, 2),
            font_style="bold",
            background_color=self.HEADING_BG,
        )
        self.etw.set_column_width(self.SHEET_NAME, 1, 20.0)
        self.etw.set_column_width(self.SHEET_NAME, 2, 100.0)
