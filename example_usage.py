"""
Example usage of Prompt Compression Token Pruning Skill.
"""

from client import PromptCompressor


def main():
    print("=== Prompt Compression Token Pruning Demonstration ===")
    compressor = PromptCompressor()

    long_prompt = (
        "Please kindly note that in order to successfully execute the database migration "
        "on the production cluster AWS eu-central-1, you must first verify that the backup "
        "snapshot snapshot-2026-09-01 has been fully verified and that active connections "
        "are below the threshold of 50 concurrent transactions."
    )

    print("Original Prompt (38 words):")
    print(long_prompt)

    res = compressor.compress(long_prompt, target_ratio=0.55)
    print(f"\nCompressed Prompt ({res['compressed_tokens']} tokens, {res['compression_ratio'] * 100:.1f}% ratio):")
    print(res["compressed_text"])
    print(f"Tokens Saved: {res['tokens_saved']}")


if __name__ == "__main__":
    main()
