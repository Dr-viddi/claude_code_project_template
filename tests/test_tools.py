"""Tool validation, contracts, and the code_search path-traversal guard."""

from __future__ import annotations

import pytest

from agent.tools import CodeSearchTool, CrmTool, ToolError, WebSearchTool


@pytest.mark.asyncio
async def test_crm_get_known_customer():
    crm = CrmTool()

    customer = await crm.get_customer("cus_001")

    assert customer["name"] == "Ada Lovelace"


@pytest.mark.asyncio
async def test_crm_unknown_customer_raises():
    crm = CrmTool()

    with pytest.raises(ToolError):
        await crm.get_customer("nope")


@pytest.mark.asyncio
async def test_crm_create_ticket_returns_id():
    crm = CrmTool()

    ticket = await crm.create_ticket("cus_001", "cannot log in")

    assert ticket["id"].startswith("tkt_")
    assert ticket["customer_id"] == "cus_001"


@pytest.mark.asyncio
async def test_web_search_returns_k_results():
    tool = WebSearchTool()

    results = await tool("agent frameworks", k=3)

    assert len(results) == 3
    assert {"url", "title", "snippet"} <= results[0].keys()


@pytest.mark.asyncio
async def test_web_search_empty_query_raises():
    tool = WebSearchTool()

    with pytest.raises(ToolError):
        await tool("   ")


@pytest.mark.asyncio
async def test_code_search_rejects_path_traversal():
    tool = CodeSearchTool(".")

    with pytest.raises(ToolError):
        await tool("../etc/passwd")


@pytest.mark.asyncio
async def test_code_search_finds_known_symbol():
    tool = CodeSearchTool(".")

    results = await tool("class Harness", k=5)

    assert isinstance(results, list)
    assert any("adrian_init.py" in r["file"] for r in results)
