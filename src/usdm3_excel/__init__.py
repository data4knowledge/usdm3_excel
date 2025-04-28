import json
from usdm3_excel.export.study_sheet.study_sheet import StudySheet
from usdm3_excel.export.study_identifiers_sheet.study_identifiers_sheet import (
    StudyIdentifiersSheet,
)
from usdm3_excel.export.study_content_sheet.study_content_sheet import (
    StudyContentSheet,
)
from usdm4_excel.export.study_activities_sheet.study_activities_sheet import (
    StudyActivitiesSheet,
)
from usdm4_excel.export.study_encounters_sheet.study_encounters_sheet import (
    StudyEncountersSheet,
)
from usdm4_excel.export.study_epochs_sheet.study_epochs_sheet import (
    StudyEpochsSheet,
)
from usdm4_excel.export.study_arms_sheet.study_arms_sheet import (
    StudyArmsSheet,
)
from usdm3_excel.export.study_design_sheet.study_design_sheet import (
    StudyDesignSheet,
)
from usdm3_excel.export.study_timeline_sheet.study_timeline_sheet import (
    StudyTimelineSheet,
)
from usdm4_excel.export.study_procedures_sheet.study_procedures_sheet import (
    StudyProceduresSheet
)
from usdm4_excel.export.configuration_sheet.configuration_sheet import (
    ConfigurationSheet
)
from usdm3_excel.export.study_timing_sheet.study_timing_sheet import StudyTimingSheet
from usdm4_excel.export.base.ct_version import CTVersion
from usdm4_excel.excel_table_writer.excel_table_writer import ExcelTableWriter
from usdm4 import USDM4
from usdm4.api.wrapper import Wrapper
from usdm4.api.code import Code


class USDM3Excel:
    def to_excel(self, usdm_filepath: str, excel_filepath: str):
        ct_version = CTVersion()
        etw = ExcelTableWriter(excel_filepath, default_sheet_name="study")
        with open(usdm_filepath) as f:
            data = json.load(f)
        usdm = USDM4()
        wrapper: Wrapper = usdm.from_json(data)
        study = wrapper.study

        # Add expected sheets
        etw.add_table([["name", "description", "label", "transitionStartRule", "transitionEndRule"]],"studyDesignElements")
        etw.add_table([["name", "description", "label", "codes"]],"studyDesignIndications")
        etw.add_table([["name", "description", "label", "codes", "role", "type", "pharmacologicalClass", "productDesignation", "minimumResponseDuration", "administrationName", "administrationDescription", "administrationLabel", "administrationRoute", "administrationDose", "administrationFrequency", "administrationDurationDescription", "administrationDurationWillVary", "administrationDurationWillVaryReason", "administrationDurationQuantity"]],"studyDesignInterventions")
        etw.add_table([
            ["level", "name", "description", "label", "plannedCompletionNumber", "plannedEnrollmentNumber", "plannedAge", "plannedSexOfParticipants", "includesHealthySubjects"],
            ["Main", "POP1", "Patients with Probable Mild to Moderate Alzheimer's Disease", "", "300", "300", "18..100 years", "BOTH", "N"]],"studyDesignPopulations")
        etw.add_table([["xref", "summaryMeasure", "populationDescription", "intercurrentEventName", "intercurrentEventDescription", "intercurrentEventStrategy", "treatmentXref", "endpointXref"]],"studyDesignEstimands")
        etw.add_table([["objectiveName", "objectiveDescription", "objectiveLabel", "objectiveText", "objectiveLevel", "endpointName", "endpointDescription", "endpointLabel", "endpointText", "endpointPurpose", "endpointLevel"]],"studyDesignOE")
        etw.add_table([
            ["category", "identifier", "name", "description", "label", "text", "dictionary"],
            ["Inclusion", "01", "IN01", "", "Label", "<p>Inclusion criteria text</p>", ""],
            ["Exclusion", "01", "EX01", "", "Label", "<p>Exclusion criteria text</p>", ""]
            ],"studyDesignEligibilityCriteria")



        # Add expected content, if missing
        clinic = Code(**{'uuid': 'uuid', 'id': '0', 'code': '1', 'codeSystem': '2', 'codeSystemVersion': '3', 'decode': 'CLINIC', 'instanceType': 'Code'})
        in_person = Code(**{'uuid': 'uuid', 'id': '0', 'code': '1', 'codeSystem': '2', 'codeSystemVersion': '3', 'decode': 'In Person', 'instanceType': 'Code'})
        print("clinic", clinic)
        # print("study.versions[0].studyDesigns[0]", study.versions[0].studyDesigns[0])
        for encounter in study.versions[0].studyDesigns[0].encounters:
            if encounter.environmentalSettings == []:
                encounter.environmentalSettings = [clinic]
            if encounter.contactModes == []:
                encounter.contactModes = [in_person]
        # for a in study.versions[0].studyDesigns[0].scheduleTimelines:
        #     print("a",a)
            # if encounter.environmentalSettings == []:
            #     encounter.environmentalSettings = [clinic]
        for klass in [
            StudySheet,
            StudyIdentifiersSheet,
            StudyContentSheet,
            StudyActivitiesSheet,
            StudyTimingSheet,
            StudyEncountersSheet,
            StudyEpochsSheet,
            StudyArmsSheet,
            StudyDesignSheet,
            StudyTimelineSheet,
            StudyProceduresSheet,
            ConfigurationSheet
        ]:
            klass(ct_version, etw).save(study)
        etw.save()
