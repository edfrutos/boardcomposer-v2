from boardcomposer.ai import strip_json_fence


def test_strip_json_fence_removes_a_json_labelled_fence():
    raw = '```json\n{"a": 1}\n```'

    assert strip_json_fence(raw) == '{"a": 1}'


def test_strip_json_fence_removes_a_bare_fence():
    raw = '```\n{"a": 1}\n```'

    assert strip_json_fence(raw) == '{"a": 1}'


def test_strip_json_fence_leaves_unfenced_json_untouched():
    raw = '{"a": 1}'

    assert strip_json_fence(raw) == '{"a": 1}'


def test_strip_json_fence_trims_surrounding_whitespace():
    raw = '\n  ```json\n{"a": 1}\n```  \n'

    assert strip_json_fence(raw) == '{"a": 1}'
