from dataclasses import dataclass
from typing import List, Optional


@dataclass
class QAPair:
    id: str
    chapter: str
    question_index: int
    question_raw: str
    answer_raw: str
    question_norm: Optional[str]
    answer_norm: Optional[str]
    source: str
    split: str


@dataclass
class Segment:
    id: str
    qa_id: str
    chapter: str
    role: str  # "Q" or "A"
    segment_index: int
    segment_raw: str
    segment_norm: Optional[str]
    prev_segment_id: Optional[str]
    next_segment_id: Optional[str]


@dataclass
class Morpheme:
    surface: str
    type: str  # "root", "suffix", "blend", etc.


@dataclass
class MorphToken:
    token_index: int
    surface: str
    lemma: str
    morphemes: List[Morpheme]


@dataclass
class MorphemeAnnotation:
    segment_id: str
    tokens: List[MorphToken]


@dataclass
class QNLPPair:
    pair_id: str
    qa_id: str
    question: str
    answer: str
    label: int
    pair_type: str  # "authentic", "mismatched_fw", etc.
