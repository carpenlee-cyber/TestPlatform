# TestPlatform 🧪

> 一个面向团队的测试管理平台，涵盖测试用例管理、Bug 跟踪、自动化测试和数据看板，目标是成为开箱即用的轻量级测试基础设施。

[![Build Status](https://github.com/carpenlee-cyber/TestPlatform/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/carpenlee-cyber/TestPlatform/actions)
![Java](https://img.shields.io/badge/Java-17-orange)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.4-green)
![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📸 项目截图

| 登录页 | Dashboard | 测试用例管理 |
| --- | --- | --- |
| ![Login](test-artifacts/screenshots/login.png) | ![Dashboard](test-artifacts/screenshots/dashboard.png) | ![TestCases](test-artifacts/screenshots/testcases.png) |

---

## ✨ 功能特性

- 🔐 **JWT 认证** — 登录鉴权，Token 自动续期，双存储策略（localStorage + sessionStorage）
- 📋 **测试用例管理** — 创建、编辑、删除、分页查询，支持状态和优先级筛选
- 🐛 **Bug 跟踪** — 完整的 Bug 生命周期管理，支持严重级别、指派人、状态流转
- 📊 **数据看板** — 实时统计测试用例数、Bug 数、通过率等核心指标
- 🤖 **自动化测试** — 内置 Python + Playwright E2E 测试套件，10 个 API 用例 100% 通过
- 🌐 **前后端分离** — Vue3 + Vite 前端，Spring Boot 后端，Nginx 反向代理

---

## 🏗️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Element Plus + Pinia |
| 后端 | Spring Boot 3.2.4 + Spring Security + JPA |
| 数据库 | SQLite（轻量嵌入式，零配置） |
| 认证 | JWT（jjwt 0.11.5） |
| 自动化测试 | Python + pytest + Playwright |
| 容器化 | Docker + Docker Compose |
| CI/CD | GitHub Actions |

---

## 🚀 快速启动

### 方式一：Docker Compose（推荐）

```bash
git clone https://github.com/carpenlee-cyber/TestPlatform.git
cd TestPlatform
docker compose up -d
```

访问：http://localhost:5173  
默认账号：`admin` / `admin123`

### 方式二：本地开发

**后端**
```bash
cd backend
mvn spring-boot:run
# 服务启动在 http://localhost:8080
```

**前端**
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

---

## 📁 项目结构

```
TestPlatform/
├── frontend/               # Vue3 前端
│   ├── src/
│   │   ├── views/          # 页面（Login、Dashboard、TestCases、Bugs）
│   │   ├── layouts/        # 布局组件（MainLayout 含可折叠侧边栏）
│   │   ├── api/            # API 请求封装
│   │   ├── stores/         # Pinia 状态管理（auth）
│   │   └── router/         # 路由配置（含导航守卫）
│   └── Dockerfile
├── backend/                # Spring Boot 后端
│   ├── src/main/java/com/testplatform/
│   │   ├── controller/     # REST 控制器
│   │   ├── service/        # 业务逻辑
│   │   ├── entity/         # JPA 实体
│   │   ├── repository/     # 数据访问层
│   │   ├── security/       # JWT 过滤器 & Security 配置
│   │   ├── common/         # 统一响应封装 Result<T>
│   │   └── exception/      # 全局异常处理
│   └── Dockerfile
├── tests/                  # Python 自动化测试套件
│   ├── test_cases/         # 测试用例
│   └── utils/              # 工具类（API Helper、DB Helper）
├── test-artifacts/         # 测试产物
│   ├── test-cases/         # pytest 脚本
│   ├── test-results/       # 测试结果 JSON
│   └── reports/            # 测试报告 Markdown
└── .github/workflows/      # CI/CD 流水线
```

---

## 🔌 API 接口

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | `/api/auth/login` | 用户登录，返回 JWT Token | ❌ |
| GET | `/api/testcases` | 获取测试用例列表 | ✅ |
| POST | `/api/testcases` | 创建测试用例 | ✅ |
| PUT | `/api/testcases/{id}` | 更新测试用例 | ✅ |
| DELETE | `/api/testcases/{id}` | 删除测试用例 | ✅ |
| GET | `/api/bugs` | 获取 Bug 列表 | ✅ |
| POST | `/api/bugs` | 创建 Bug | ✅ |
| PUT | `/api/bugs/{id}` | 更新 Bug | ✅ |
| DELETE | `/api/bugs/{id}` | 删除 Bug | ✅ |
| GET | `/api/dashboard/stats` | 获取统计数据 | ✅ |

---

## 🧪 测试报告

最新测试结果（2026-04-03）：

| 阶段 | 用例数 | 通过 | 通过率 |
|------|--------|------|--------|
| API 自动化测试 | 10 | 10 | **100%** ✅ |

完整报告：[test-artifacts/reports/test-report-final.md](test-artifacts/reports/test-report-final.md)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT License — 自由使用，记得给个 ⭐
