from dataclasses import dataclass

@dataclass
class Metadata:
    datetime: str
    query: str
    job_id: str