import requests
from anthropic import Anthropic

anthropic = Anthropic()

class Pipeline:
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.raw_data = []
        self.features = []
        self.abstracts = []

    def fetch_sources(self):
        if 'sources' in self.config and not self.config['sources'] == None:
            for source in self.config['sources']:
                print(f"{self.name} - Fetching source: {source}")
                response = requests.get(source)
                # print(response.text)
                self.raw_data.append(response.text)

    def query_all_source_data_with_template(self, template_path):
        with open(template_path, 'r') as f:
            prompt_template = f.read()
        # print(f"{self.name} - Applying prompt template: \n {prompt_template}")
        completions = []
        for source_record in self.raw_data:
            prompt = prompt_template.format(data=source_record)
            # print(prompt)
            completion = anthropic.completions.create(
                model="claude-2.1",
                max_tokens_to_sample=600,
                prompt=prompt,
            )
            completions.append(completion.completion)
        return completions
    def extract_features(self):
        if 'features' in self.config and not self.config['features'] == None:
            for feature in self.config['features']:
                print(f"{self.name} - Processing feature: {feature}")
                completions = self.query_all_source_data_with_template(feature)
                # print(completion)
                self.features.extend(completions)


    def query_aggregate_data_with_template(self, template_path):
        with open(template_path, 'r') as f:
            prompt_template = f.read()
        # print(f"{self.name} - Applying prompt template: \n {prompt_template}")
        prompt = prompt_template.format(data="\n---\n".join(self.features))
        # print(prompt)
        completion = anthropic.completions.create(
            model="claude-2.1",
            max_tokens_to_sample=600,
            prompt=prompt,
        )
        return completion.completion

    def get_abstracts(self):
        if 'abstractions' in self.config and not self.config['abstractions'] == None:
            for abstraction in self.config['abstractions']:
                print(f"{self.name} - Processing abstraction: {abstraction}")
                completion = self.query_aggregate_data_with_template(abstraction)
                # print(completion)
                self.abstracts.append(completion)

    def run(self):
        self.fetch_sources()
        self.extract_features()
        self.get_abstracts()
        # for abstract in self.abstracts:
        #     print(abstract)
        return {
            "raw_data": self.raw_data,
            "features": self.features,
            "abstracts": self.abstracts
        }

