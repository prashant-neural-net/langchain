from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

text = """
    def backtrack(n, path):
    # Base case
    if len(path) == n:
        print(path)
        return

    # Choose 0
    path.append(0)
    backtrack(n, path)
    path.pop()       # backtrack

    # Choose 1
    path.append(1)
    backtrack(n, path)
    path.pop()       # backtrack


backtrack(3, [])"""

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=300,
    chunk_overlap=2,
)

result = splitter.split_text(text)

print(result[0])
