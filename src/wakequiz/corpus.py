"""
Corpus construction for FW Book I Chapter 6

Extracts structured Q/A pairs from raw text and generates negative
pairs for QNLP training (mismatched, shuffled, cross-chapter).
"""

import json
import random
from pathlib import Path
from typing import List, Tuple

from .data_types import QAPair, Segment, QNLPPair


def load_chapter_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_qa_pairs(
    text: str,
    chapter: str = "I.6",
    source: str = "manual",
) -> List[QAPair]:
    raise NotImplementedError(
        "Provide extracted chapter text with question boundaries. "
        "See data/raw/fw_book1_ch6.txt"
    )


def segment_qa_pair(pair: QAPair) -> Tuple[List[Segment], List[Segment]]:
    """
    Split a macro Q/A pair into sentence-level micro segments.

    Returns (question_segments, answer_segments).
    """
    q_sents = _split_sentences(pair.question_raw)
    a_sents = _split_sentences(pair.answer_raw)

    q_segments = []
    for i, sent in enumerate(q_sents):
        seg_id = f"{pair.id}_Q_{i:03d}"
        q_segments.append(Segment(
            id=seg_id,
            qa_id=pair.id,
            chapter=pair.chapter,
            role="Q",
            segment_index=i,
            segment_raw=sent,
            segment_norm=None,
            prev_segment_id=q_segments[-1].id if q_segments else None,
            next_segment_id=None,
        ))
        if len(q_segments) > 1:
            q_segments[-2].next_segment_id = seg_id

    a_segments = []
    for i, sent in enumerate(a_sents):
        seg_id = f"{pair.id}_A_{i:03d}"
        a_segments.append(Segment(
            id=seg_id,
            qa_id=pair.id,
            chapter=pair.chapter,
            role="A",
            segment_index=i,
            segment_raw=sent,
            segment_norm=None,
            prev_segment_id=a_segments[-1].id if a_segments else None,
            next_segment_id=None,
        ))
        if len(a_segments) > 1:
            a_segments[-2].next_segment_id = seg_id

    return q_segments, a_segments


def generate_negative_pairs(
    authentic_pairs: List[QAPair],
    seed: int = 42,
) -> List[QNLPPair]:
    """
    Generate negative Q/A pairs for QNLP training.

    Strategies:
    - mismatched_fw: real Q + wrong A from a different question
    - shuffled: real Q + A with sentences randomly reordered
    """
    rng = random.Random(seed)
    negatives = []
    pair_counter = 0

    for i, pair in enumerate(authentic_pairs):
        # mismatched: pair each Q with every other A
        other_pairs = [p for j, p in enumerate(authentic_pairs) if j != i]
        for other in other_pairs:
            negatives.append(QNLPPair(
                pair_id=f"neg_{pair_counter:04d}",
                qa_id=pair.id,
                question=pair.question_raw,
                answer=other.answer_raw,
                label=0,
                pair_type="mismatched_fw",
            ))
            pair_counter += 1

        # shuffled: randomise sentence order within the answer
        a_sents = _split_sentences(pair.answer_raw)
        if len(a_sents) > 1:
            shuffled = a_sents.copy()
            rng.shuffle(shuffled)
            # only keep if order actually changed
            if shuffled != a_sents:
                negatives.append(QNLPPair(
                    pair_id=f"neg_{pair_counter:04d}",
                    qa_id=pair.id,
                    question=pair.question_raw,
                    answer=" ".join(shuffled),
                    label=0,
                    pair_type="shuffled",
                ))
                pair_counter += 1

    return negatives


def build_qnlp_dataset(
    authentic_pairs: List[QAPair],
    seed: int = 42,
) -> List[QNLPPair]:
    """
    Build the full QNLP training dataset: authentic + negative pairs.
    """
    # authentic positives
    positives = [
        QNLPPair(
            pair_id=f"pos_{i:04d}",
            qa_id=pair.id,
            question=pair.question_raw,
            answer=pair.answer_raw,
            label=1,
            pair_type="authentic",
        )
        for i, pair in enumerate(authentic_pairs)
    ]

    # negatives
    negatives = generate_negative_pairs(authentic_pairs, seed=seed)

    dataset = positives + negatives
    random.Random(seed).shuffle(dataset)
    return dataset


def save_jsonl(items, path: Path):
    """Save a list of dataclass instances as JSONL."""
    from dataclasses import asdict
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(asdict(item), ensure_ascii=False) + "\n")


def load_jsonl(path: Path, cls):
    """Load JSONL into a list of dataclass instances."""
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            items.append(cls(**data))
    return items


def _split_sentences(text: str) -> List[str]:
    """ Crude sentence splitter for Wake text."""
    import re
    sents = re.split(r'(?<=[.?!])\s+', text.strip())
    return [s.strip() for s in sents if s.strip()]
