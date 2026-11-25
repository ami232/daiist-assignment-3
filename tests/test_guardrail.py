"""Tests for the citation guardrail in agent.py (no API calls)."""

from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

import agent
from agent import REFUSAL, verify_citations

BLOQUE = "Result 1 [LAU, Artículo 36, p. 25]\nArtículo 36. Fianza. 1. A la celebración del contrato..."


def test_cita_devuelta_pasa():
    respuesta = "La fianza es de una mensualidad [LAU, Artículo 36, p. 25]."
    assert verify_citations(respuesta, [BLOQUE]) == respuesta


def test_cita_inventada_da_negativa():
    respuesta = "La fianza es de una mensualidad [LAU, Artículo 99, p. 70]."
    assert verify_citations(respuesta, [BLOQUE]) == REFUSAL


def test_respuesta_sin_citas_da_negativa():
    assert verify_citations("La fianza es de una mensualidad.", [BLOQUE]) == REFUSAL


def test_negativa_pasa_sin_tocar():
    assert verify_citations(REFUSAL, []) == REFUSAL


def test_cita_con_otra_pagina_da_negativa():
    """Decisión: se compara la cita completa, página incluida."""
    respuesta = "La fianza es de una mensualidad [LAU, Artículo 36, p. 26]."
    assert verify_citations(respuesta, [BLOQUE]) == REFUSAL


def test_el_agente_aplica_el_guardrail_y_guarda_la_respuesta_original():
    inventada = "La fianza es de tres mensualidades [LAU, Artículo 99, p. 70].\n" + agent.DISCLAIMER
    messages = [
        HumanMessage("¿Cuánta fianza?"),
        AIMessage("", tool_calls=[{"name": "search", "args": {"query": "fianza"}, "id": "1"}]),
        ToolMessage(BLOQUE, name="search", tool_call_id="1"),
        AIMessage(inventada),
    ]
    result = agent.summarise(messages, seconds=1.0)
    assert result["answer"] == REFUSAL
    assert result["raw_answer"] == inventada
    assert "LAU, Artículo 99, p. 70" in result["guardrail"]


def test_las_frases_fijas_de_agents_md_coinciden_con_el_codigo():
    rules = (Path(agent.ROOT) / "AGENTS.md").read_text(encoding="utf-8")
    for fixed in (agent.REFUSAL, agent.PARTIAL_PREFIX, agent.DISCLAIMER):
        assert fixed in rules


def test_el_mensaje_de_estado_de_add_document_no_pasa_por_el_guardrail():
    estado = "He añadido el documento: 'Padron' añadido, 140 trozos ya se pueden buscar."
    messages = [
        HumanMessage("Añade corpus/Padron.pdf"),
        AIMessage("", tool_calls=[{"name": "add_document", "args": {"path": "corpus/Padron.pdf"}, "id": "1"}]),
        ToolMessage("Added 'Padron': 140 chunks are now searchable.", name="add_document", tool_call_id="1"),
        AIMessage(estado),
    ]
    result = agent.summarise(messages, seconds=1.0)
    assert result["answer"] == estado and result["guardrail"] is None
    assert result["tool_results"] == [{"name": "add_document", "text": "Added 'Padron': 140 chunks are now searchable."}]
