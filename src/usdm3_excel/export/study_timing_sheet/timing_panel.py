from usdm4.api.study import Study
from usdm4.api.timing import Timing
from usdm4.api.schedule_timeline import ScheduleTimeline
from usdm4_excel.export.base.collection_panel import CollectionPanel


class TimingPanel(CollectionPanel):
    def execute(self, study: Study) -> list[list[dict]]:
        collection = []
        for version in study.versions:
            for design in version.studyDesigns:
                for timeline in design.scheduleTimelines:
                    for item in timeline.timings:
                        self._add_timing(collection, item, timeline)
        return super().execute(
            collection,
            [
                "name",
                "description",
                "label",
                "type",
                "from",
                "to",
                "timingValue",
                "toFrom",
                "window",
            ],
        )

    def type_to_v3(self, pt: str) -> str:
        if pt == "Fixed Reference":
            return "Fixed"
        return pt

    def toFrom_to_v3(self, pt: str) -> str:
        if pt == "Start to Start":
            return "S2S"
        return pt

    def timingValue_to_v3(self, pt: str) -> str:
        if pt == "TBD":
            return "1 day"
        return pt

    def _add_timing(self, collection: list, item: Timing, timeline: ScheduleTimeline):
        data = item.model_dump()
        data["type"] = self.type_to_v3(self._pt_from_code(item.type))
        from_tp = timeline.find_timepoint(item.relativeFromScheduledInstanceId)
        data["from"] = from_tp.name if from_tp else ""
        to_tp = timeline.find_timepoint(item.relativeToScheduledInstanceId)
        # print("to_tp", to_tp, "should not be blank")
        data["to"] = to_tp.name if to_tp else ""
        data["timingValue"] = self.timingValue_to_v3(item.valueLabel)
        data["window"] = item.windowLabel
        data["toFrom"] = self.toFrom_to_v3(self._pt_from_code(item.relativeToFrom))
        collection.append(data)
