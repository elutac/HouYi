import argparse
import openai
import json
import pathlib
from intention.content_manipulation import ContentManipulation
from harness.connector_harness import ConnectorHarness
from iterative_prompt_optimization import IterativePromptOptimizer

# Load config file from root path
config_file_path = pathlib.Path(__file__).parent / "config.json"
# Read config file
config = json.load(open(config_file_path))

# Define constants for optimization process
max_iteration = 50
max_crossover = 0.1
max_mutation = 0.5
max_population = 10

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint_url", required=True)
    parser.add_argument("--site_url", required=True)
    parser.add_argument("--application_document", required=True)
    parser.add_argument("--name", default="target_app")
    parser.add_argument("--input_type", default="text")
    args = parser.parse_args()

    openai.api_key = config["openai_key"]

    application_harness = ConnectorHarness(
        name=args.name,
        site_url=args.site_url,
        application_document=args.application_document,
        endpoint_url=args.endpoint_url,
        input_type=args.input_type
    )

    intention = ContentManipulation()

    iterative_prompt_optimizer = IterativePromptOptimizer(
        intention,
        application_harness,
        max_iteration,
        max_crossover,
        max_mutation,
        max_population,
    )

    iterative_prompt_optimizer.optimize()
    best = iterative_prompt_optimizer.best_chromosome

    result = {
        "injected_prompt": f"{best.framework}{best.separator}{best.disruptor}",
        "fitness_score": best.fitness_score,
        "llm_response": best.llm_response,
        "success": best.is_successful
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
