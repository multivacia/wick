import { R3eExperimentScreenView } from "./R3eExperimentScreenView";
import { loadR3eExperimentScreenData } from "./loadR3eExperimentScreenData";

export function R3eExperimentScreen() {
  return <R3eExperimentScreenView data={loadR3eExperimentScreenData()} />;
}
