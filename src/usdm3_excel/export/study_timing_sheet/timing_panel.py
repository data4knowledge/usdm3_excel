from usdm4.api.study import Study
from usdm4.api.timing import Timing
from usdm4.api.schedule_timeline import ScheduleTimeline
from usdm3_excel.export.base.collection_panel import CollectionPanel


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

    def _add_timing(self, collection: list, item: Timing, timeline: ScheduleTimeline):
        data = item.model_dump()
        data["type"] = self._pt_from_code(item.type)
        from_tp = timeline.find_timepoint(item.relativeFromScheduledInstanceId)
        data["from"] = from_tp.name if from_tp else ""
        to_tp = timeline.find_timepoint(item.relativeToScheduledInstanceId)
        data["to"] = to_tp.name if to_tp else ""
        data["timingValue"] = item.valueLabel
        data["window"] = item.windowLabel
        data["toFrom"] = self._pt_from_code(item.relativeToFrom)
        collection.append(data)
