from app.agent.state import QueryState

SUPPORTED_REGIONS = ("华东", "华南", "西南", "华北")


def extract_parameters(state: QueryState) -> QueryState:
    for region_name in SUPPORTED_REGIONS:
        if region_name in state.question:
            state.parameters["region_name"] = region_name
            break

    return state