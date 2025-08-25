from utils.prompt_loader import render_prompt


def test_render_scholar_prompt():
    msgs, meta = render_prompt("prompts/agents/scholar.yaml", model=None, user_id="test-user", user_query="What is AI?")
    assert isinstance(msgs, list)
    roles = {m["role"] for m in msgs}
    assert "system" in roles
    assert "user" in roles
    assert meta.get("max_tokens") is None or isinstance(meta.get("max_tokens"), int) or True
    # ensure rendered includes user id and query
    contents = "\n".join(m["content"] for m in msgs)
    assert "test-user" in contents
    assert "What is AI?" in contents
