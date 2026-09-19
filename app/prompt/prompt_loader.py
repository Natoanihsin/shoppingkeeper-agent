from pathlib import Path

PROMPT_DIRECTORY = Path(__file__).parents[2] / "prompts"


def load_prompt(file_name: str) -> str:
    prompt_path = PROMPT_DIRECTORY / file_name

    if not prompt_path.is_file():
        raise FileNotFoundError(
            f"找不到提示词文件：{prompt_path}"
        )

    return prompt_path.read_text(encoding="utf-8")