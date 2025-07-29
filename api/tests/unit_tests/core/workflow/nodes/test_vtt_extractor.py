import ast
import pathlib

import chardet
import webvtt

SRC_PATH = pathlib.Path(__file__).resolve().parents[5] / "core/workflow/nodes/document_extractor/node.py"
source = SRC_PATH.read_text()
module_ast = ast.parse(source)
func_map = {node.name: node for node in module_ast.body if isinstance(node, ast.FunctionDef)}


def load_function(name):
    ns = {"webvtt": webvtt, "chardet": chardet, "TextExtractionError": Exception}
    exec(ast.unparse(func_map["_extract_text_from_plain_text"]), ns)  # noqa: S102
    exec(ast.unparse(func_map[name]), ns)  # noqa: S102
    return ns[name]


def test_extract_text_from_vtt_handles_none_speaker():
    extract = load_function("_extract_text_from_vtt")
    vtt_content = (
        b"WEBVTT\n\n"
        b"00:00:01.000 --> 00:00:02.000\n"
        b"<v Speaker 1> Hello\n\n"
        b"00:00:02.500 --> 00:00:03.000\n"
        b"<v> um\n\n"
        b"00:00:03.500 --> 00:00:04.000\n"
        b"<v Speaker 1> world\n"
    )
    result = extract(vtt_content)
    assert result.splitlines() == [
        'Speaker 1 " Hello"',
        ' " um"',
        'Speaker 1 " world"',
    ]
