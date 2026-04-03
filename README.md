# TestPlatform 🚀 (v1.0 Stage-2)

**TestPlatform** 是一款准商用级的测试管理平台，旨在为中小型团队提供高效、美观、全链路的测试用例管理与缺陷追踪解决方案。

---

## ✨ 核心特性

- **🎭 专业级 UI/UX**：采用 Vue3 + Element Plus 打造的分栏式布局，支持侧边栏折叠、实时统计仪表盘。
- **🧪 全链路测试管理**：
  - **用例中心 (TestCases)**：支持用例的分级管理、分页检索及自动化执行状态追踪。
  - **缺陷追踪 (Bugs)**：完整的 Bug 生命周期管理，支持状态流转与严重程度统计。
- **📊 动态数据看板**：实时汇总用例通过率、Bug 修复进度，助力管理决策。
- **🔒 企业级鉴权**：基于 JWT 的安全体系，支持“记住我”登录状态双存储策略（LocalStorage/SessionStorage）。
- **🐳 生产就绪 (Production-Ready)**：
  - 完美支持 Docker Compose 一键部署。
  - **数据库自动感知**：开发环境自动切换 SQLite，NAS 生产环境自动对接 MySQL 8.0。

---

## 🛠️ 技术架构

- **前端 (Frontend)**：Vue 3.x + Vite + Element Plus + Pinia
- **后端 (Backend)**：Spring Boot 3.x + Spring Data JPA + JWT + Maven
- **数据库 (Database)**：MySQL 8.0 (生产) / SQLite (本地开发)
- **部署 (DevOps)**：Docker + Docker Compose + GitHub Actions (CI/CD)
- **测试 (QA)**：pytest + requests + Playwright 自动化验证

---

## 📸 界面预览

| 登录页面 | 控制面板 |
| :---: | :---: |
| ![Login](./screenshots/login.png) | ![Dashboard](./screenshots/dashboard.png) |

*(图片正在通过 Playwright 自动化生成中...)*

---

## 🚀 快速开始 (NAS/服务器部署)

1. **环境要求**：已安装 Docker & Docker Compose。
2. **下载并拉起**：
   ```bash
   mkdir TestPlatform && cd TestPlatform
   # 获取项目文件
   curl -O https://raw.githubusercontent.com/carpenlee-cyber/TestPlatform/main/docker-compose.yml
   # 一键部署
   docker-compose up -d
   ```
3. **访问地址**：`http://<您的NAS_IP>:8080`
4. **默认凭据**：
   - 用户名：`admin`
   - 密  码：`admin123`

---

## ✅ 质量保障报告 (QA Report)

本版本已通过 **Stage-2 全量回归测试**：
- **API 接口测试**：10/10 PASS (100% 成功率)
- **数据库迁移**：MySQL 8.0 自动初始化验证通过
- **构建测试**：GitHub Actions 构建通过

---
*Generated with ❤️ by 小龙虾 for Boss.*
