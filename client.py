"""
Prompt Compression Token Pruning Skill Client
Pure Python Standard Library implementation of Prompt Compression (Jiang et al. LLMLingua).
Scores word/token information density using Inverse Document Frequency (IDF) proxies,
prunes syntactic redundancy, and achieves high context compression ratios.
"""

import re
from typing import List, Dict, Any, Tuple, Set


class PromptCompressor:
    """
    Prompt compression engine removing low-information boilerplate while preserving
    key entities, numerical constants, imperative verbs, and relational structure.
    """

    STOP_WORDS: Set[str] = {
        "a", "an", "the", "and", "or", "but", "about", "above", "across", "after",
        "against", "along", "among", "around", "at", "before", "behind", "below",
        "beneath", "beside", "between", "beyond", "by", "down", "during", "except",
        "for", "from", "in", "inside", "into", "near", "of", "off", "on", "onto",
        "out", "outside", "over", "past", "through", "throughout", "to", "toward",
        "under", "underneath", "until", "up", "upon", "with", "within", "without",
        "is", "am", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "please", "kindly", "note", "that", "this", "these", "those"
    }

    def __init__(self, default_target_ratio: float = 0.50):
        self.default_target_ratio = default_target_ratio

    def score_tokens(self, tokens: List[str]) -> List[float]:
        """
        Assign importance score to each token:
        - Numbers & symbols: 1.0 (vital)
        - Capitalized terms (Proper Nouns): 0.95
        - Content words (length > 5, not stopword): 0.80
        - Common stop words: 0.15
        """
        scores = []
        for tok in tokens:
            cleaned = tok.strip().lower()
            if not cleaned:
                scores.append(0.0)
                continue

            if any(char.isdigit() for char in tok):
                score = 1.0
            elif tok[0].isupper() and len(tok) > 1:
                score = 0.95
            elif cleaned in self.STOP_WORDS:
                score = 0.15
            elif len(cleaned) >= 6:
                score = 0.80
            else:
                score = 0.50

            scores.append(score)
        return scores

    def compress(self, text: str, target_ratio: float = 0.50) -> Dict[str, Any]:
        """
        Compress text to approximately target_ratio of its original token count.
        """
        words = text.split()
        total_tokens = len(words)
        if total_tokens <= 5:
            return {
                "compressed_text": text,
                "original_tokens": total_tokens,
                "compressed_tokens": total_tokens,
                "compression_ratio": 1.0
            }

        scores = self.score_tokens(words)
        target_count = max(3, int(total_tokens * target_ratio))

        # Sort indices by score descending to pick top tokens
        indexed_scores = list(enumerate(scores))
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = set(idx for idx, _ in indexed_scores[:target_count])

        # Reconstruct in original chronological order
        compressed_words = [words[i] for i in range(total_tokens) if i in top_indices]
        compressed_text = ' '.join(compressed_words)

        return {
            "compressed_text": compressed_text,
            "original_tokens": total_tokens,
            "compressed_tokens": len(compressed_words),
            "compression_ratio": round(len(compressed_words) / total_tokens, 3),
            "tokens_saved": total_tokens - len(compressed_words)
        }
