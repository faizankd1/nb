def test_chat_uses_only_top_one_and_exposes_source_on_abstention(monkeypatch):
    import sys, types
    # Retrieval is mocked below; provide the optional ChromaDB import for minimal test environments.
    monkeypatch.setitem(sys.modules, "chromadb", types.ModuleType("chromadb"))
    import app.rag.chat as chat

    monkeypatch.setattr(chat, "list_docs", lambda owner_id: [
        {"document_id": "doc-1", "processing_status": "indexed", "indexing_status": "complete"}
    ])
    monkeypatch.setattr(chat.settings, "top_k", 1)
    monkeypatch.setattr(chat.settings, "min_similarity", 0.25)
    monkeypatch.setattr(chat, "search", lambda question, owner_id: [
        {"text": "Best chunk with answer", "metadata": {"document_id": "doc-1", "filename": "a.txt", "source_location": "page 1"}, "similarity": 0.91},
        {"text": "Second chunk", "metadata": {"document_id": "doc-1", "filename": "a.txt", "source_location": "page 2"}, "similarity": 0.80},
    ])
    monkeypatch.setattr(chat, "generate", lambda prompt: chat.ABSTENTION)

    result = chat.answer("What is the answer?", owner_id="local")
    assert result["status"] == "insufficient_evidence"
    assert result["retrieval"]["selected_chunks"] == 1
    assert len(result["sources"]) == 1
    assert result["sources"][0]["supporting_text"] == "Best chunk with answer"

def test_question_normalization_preserves_spaces_and_corrects_known_typos(monkeypatch):
    import sys, types
    monkeypatch.setitem(sys.modules, "chromadb", types.ModuleType("chromadb"))
    import app.rag.chat as chat

    assert chat.normalize_question("  What  informtion is in teh documnt? ") == "What information is in the document?"

def test_multiple_explicit_questions_are_kept_separate(monkeypatch):
    import sys, types
    monkeypatch.setitem(sys.modules, "chromadb", types.ModuleType("chromadb"))
    import app.rag.chat as chat

    assert chat.split_questions("What is the date? Who signed it?") == ["What is the date", "Who signed it"]

def test_verifier_rejects_an_unsupported_draft(monkeypatch):
    import sys, types
    monkeypatch.setitem(sys.modules, "chromadb", types.ModuleType("chromadb"))
    import app.rag.chat as chat
    monkeypatch.setattr(chat.settings, "verify_answers", True)
    monkeypatch.setattr(chat, "generate", lambda prompt: "UNSUPPORTED")

    assert not chat._verify_answer("question", "evidence", "draft")

def test_verifier_can_be_disabled(monkeypatch):
    import sys, types
    monkeypatch.setitem(sys.modules, "chromadb", types.ModuleType("chromadb"))
    import app.rag.chat as chat
    monkeypatch.setattr(chat.settings, "verify_answers", False)
    monkeypatch.setattr(chat, "generate", lambda prompt: (_ for _ in ()).throw(AssertionError("not called")))

    assert chat._verify_answer("question", "evidence", "draft")
