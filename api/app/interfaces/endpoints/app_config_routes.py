#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/17 10:39
@Author  : thezehui@gmail.com
@File    : app_config_routes.py
"""
import logging
from typing import Optional, Dict

from fastapi import APIRouter, Depends, Body

from app.application.services.app_config_service import AppConfigService
from app.domain.models.app_config import LLMConfig, AgentConfig, MCPConfig
from app.interfaces.schemas.app_config import ListMCPServerResponse, ListA2AServerResponse, ListSkillsResponse
from app.interfaces.schemas.base import Response
from app.interfaces.service_dependencies import get_app_config_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/app-config", tags=["设置模块"])


@router.get(
    path="/llm",
    response_model=Response[LLMConfig],
    summary="获取LLM配置信息",
    description="包含LLM提供商的base_url、temperature、model_name、max_tokens"
)
async def get_llm_config(
        app_config_service: AppConfigService = Depends(get_app_config_service)
) -> Response[LLMConfig]:
    """获取LLM配置信息"""
    llm_config = await app_config_service.get_llm_config()
    return Response.success(data=llm_config.model_dump(exclude={"api_key"}))


@router.post(
    path="/llm",
    response_model=Response[LLMConfig],
    summary="更新LLM配置信息",
    description="更新LLM配置信息，当api_key为空的时候表示不更新该字段"
)
async def update_llm_config(
        new_llm_config: LLMConfig,
        app_config_service: AppConfigService = Depends(get_app_config_service)
) -> Response[LLMConfig]:
    """更新LLM配置信息"""
    updated_llm_config = await app_config_service.update_llm_config(new_llm_config)
    return Response.success(
        msg="更新LLM信息配置成功",
        data=updated_llm_config.model_dump(exclude={"api_key"})
    )


@router.get(
    path="/agent",
    response_model=Response[AgentConfig],
    summary="获取Agent通用配置信息",
    description="包含最大迭代次数、最大重试次数、最大搜索结果数"
)
async def get_agent_config(
        app_config_service: AppConfigService = Depends(get_app_config_service)
) -> Response[AgentConfig]:
    """获取Agent通用配置信息"""
    agent_config = await app_config_service.get_agent_config()
    return Response.success(data=agent_config.model_dump())


@router.post(
    path="/agent",
    response_model=Response[AgentConfig],
    summary="更新Agent通用配置信息",
    description="更新Agent通用配置信息"
)
async def update_llm_config(
        new_agent_config: AgentConfig,
        app_config_service: AppConfigService = Depends(get_app_config_service)
) -> Response[AgentConfig]:
    """更新Agent配置信息"""
    updated_agent_config = await app_config_service.update_agent_config(new_agent_config)
    return Response.success(
        msg="更新Agent信息配置成功",
        data=updated_agent_config.model_dump()
    )


@router.get(
    path="/mcp-servers",
    response_model=Response[ListMCPServerResponse],
    summary="获取MCP服务器工具列表",
    description="获取当前系统的MCP服务器列表，包含MCP服务名字、工具列表、启用状态等",
)
async def get_mcp_servers(
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[ListMCPServerResponse]:
    """获取当前系统的MCP服务器工具列表"""
    mcp_servers = await app_config_service.get_mcp_servers()
    return Response.success(
        msg="获取mcp服务器列表成功",
        data=ListMCPServerResponse(mcp_servers=mcp_servers)
    )


@router.post(
    path="/mcp-servers",
    response_model=Response[Optional[Dict]],
    summary="新增MCP服务配置，支持传递一个或者多个配置",
    description="传递MCP配置信息为系统新增MCP工具",
)
async def create_mcp_servers(
        mcp_config: MCPConfig,
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """根据传递的配置信息创建mcp服务"""
    await app_config_service.update_and_create_mcp_servers(mcp_config)
    return Response.success(msg="新增MCP服务配置成功")


@router.post(
    path="/mcp-servers/{server_name}/delete",
    response_model=Response[Optional[Dict]],
    summary="删除MCP服务配置",
    description="根据传递的MCP服务名字删除指定的MCP服务",
)
async def delete_mcp_server(
        server_name: str,
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """根据服务名字删除MCP服务器"""
    await app_config_service.delete_mcp_server(server_name)
    return Response.success(msg="删除MCP服务配置成功")


@router.post(
    path="/mcp-servers/{server_name}/enabled",
    response_model=Response[Optional[Dict]],
    summary="更新MCP服务的启用状态",
    description="根据传递的server_name+enabled更新指定MCP服务的启用状态",
)
async def set_mcp_server_enabled(
        server_name: str,
        enabled: bool = Body(..., embed=True),
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """根据传递的server_name+enabled更新服务的启用状态"""
    await app_config_service.set_mcp_server_enabled(server_name, enabled)
    return Response.success(msg="更新MCP服务启用状态成功")


@router.get(
    path="/a2a-servers",
    response_model=Response[ListA2AServerResponse],
    summary="获取a2a服务器列表",
    description="获取MoocManus项目中的所有已配置的a2a服务列表",
)
async def get_a2a_servers(
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[ListA2AServerResponse]:
    """获取a2a服务列表"""
    a2a_servers = await app_config_service.get_a2a_servers()
    return Response.success(
        msg="获取a2a服务列表成功",
        data=ListA2AServerResponse(a2a_servers=a2a_servers)
    )


@router.post(
    path="/a2a-servers",
    response_model=Response[Optional[Dict]],
    summary="新增a2a服务器",
    description="为MoocManus项目新增a2a服务器",
)
async def create_a2a_server(
        base_url: str = Body(..., embed=True),
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """新增a2a服务器"""
    await app_config_service.create_a2a_server(base_url)
    return Response.success(msg="新增A2A服务配置成功")


@router.post(
    path="/a2a-servers/{a2a_id}/delete",
    response_model=Response[Optional[Dict]],
    summary="删除a2a服务器",
    description="根据A2A服务id标识删除指定的A2A服务"
)
async def delete_a2a_server(
        a2a_id: str,
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """删除a2a服务器"""
    await app_config_service.delete_a2a_server(a2a_id)
    return Response.success(msg="删除a2a服务器成功")


@router.post(
    path="/a2a-servers/{a2a_id}/enabled",
    response_model=Response[Optional[Dict]],
    summary="更新A2A服务的启用状态",
    description="启动or禁用A2A服务的状态",
)
async def set_a2a_server_enabled(
        a2a_id: str,
        enabled: bool = Body(..., embed=True),
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """更新A2A服务的启用状态"""
    await app_config_service.set_a2a_server_enabled(a2a_id, enabled)
    return Response.success(msg="更新a2a服务器启用状态成功")


# ==================== Skills 技能接口 ====================


@router.get(
    path="/skills",
    response_model=Response[ListSkillsResponse],
    summary="获取Skills技能列表",
    description="获取当前系统已配置的Skills技能列表",
)
async def get_skills(
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[ListSkillsResponse]:
    """获取Skills技能列表"""
    skills = await app_config_service.get_skills()
    return Response.success(
        msg="获取Skills技能列表成功",
        data=ListSkillsResponse(skills=skills)
    )


@router.post(
    path="/skills",
    response_model=Response[Optional[Dict]],
    summary="新增Skill技能",
    description="为MoocManus项目新增Skill技能",
)
async def create_skill(
        name: str = Body(..., embed=True),
        description: str = Body("", embed=True),
        content: str = Body("", embed=True),
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """新增Skill技能"""
    await app_config_service.create_skill(name, description, content)
    return Response.success(msg="新增Skill技能配置成功")


@router.post(
    path="/skills/{skill_id}/delete",
    response_model=Response[Optional[Dict]],
    summary="删除Skill技能",
    description="根据Skill技能id标识删除指定的Skill技能",
)
async def delete_skill(
        skill_id: str,
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """删除Skill技能"""
    await app_config_service.delete_skill(skill_id)
    return Response.success(msg="删除Skill技能成功")


@router.post(
    path="/skills/{skill_id}/enabled",
    response_model=Response[Optional[Dict]],
    summary="更新Skill技能的启用状态",
    description="启动or禁用Skill技能的状态",
)
async def set_skill_enabled(
        skill_id: str,
        enabled: bool = Body(..., embed=True),
        app_config_service: AppConfigService = Depends(get_app_config_service),
) -> Response[Optional[Dict]]:
    """更新Skill技能的启用状态"""
    await app_config_service.set_skill_enabled(skill_id, enabled)
    return Response.success(msg="更新Skill技能启用状态成功")
