import ast
import pathlib
import webvtt
import chardet

SRC_PATH = (
    pathlib.Path(__file__).resolve().parents[5]
    / 'core/workflow/nodes/document_extractor/node.py'
)
source = SRC_PATH.read_text()
module_ast = ast.parse(source)
func_map = {node.name: node for node in module_ast.body if isinstance(node, ast.FunctionDef)}

def load_function(name):
    ns = {'webvtt': webvtt, 'chardet': chardet, 'TextExtractionError': Exception}
    exec(ast.unparse(func_map['_extract_text_from_plain_text']), ns)
    exec(ast.unparse(func_map[name]), ns)
    return ns[name]


def test_extract_text_from_vtt_handles_none_speaker():
    extract = load_function('_extract_text_from_vtt')
    vtt_content = """WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n<v Speaker 1> Hello\n\n00:00:02.500 --> 00:00:03.000\n<v> um\n\n00:00:03.500 --> 00:00:04.000\n<v Speaker 1> world\n""".encode()
    result = extract(vtt_content)
    assert result.splitlines() == [
        'Speaker 1 " Hello"',
        ' " um"',
        'Speaker 1 " world"',
    ]
