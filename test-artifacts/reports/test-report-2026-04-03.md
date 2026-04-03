# 测试报告

- 日期：2026-04-03
- 测试工程师：Test-Worker-2
- 项目：TestPlatform v1.0 Stage-2

## 1. 测试摘要表格

| 总用例数 | 通过数 | 失败数 | 跳过数 | 通过率 |
| --- | --- | --- | --- | --- |
| 10 | 6 | 3 | 1 | 60% |

## 2. 测试环境信息

- 操作系统：Linux 5.10.60-qnap (x64)
- Java版本：未知（使用API测试）
- 后端端口：8080 (根据常规推断，若有具体信息请修正)
- 数据库路径：/root/.openclaw/workspace/testplatform.db

## 3. 第一阶段：静态检查结果

| 文件名 | 行数 |
| --- | --- |
| TestCase.java | 80 |
| Bug.java | 74 |
| AuthController.java | 72 |
| TestCaseController.java | 69 |
| BugController.java | 69 |
| JwtUtil.java | 58 |
| JwtFilter.java | 53 |
| DashboardService.java | 49 |
| BugService.java | 46 |
| TestCaseService.java | 45 |
| User.java | 44 |
| GlobalExceptionHandler.java | 42 |
| SecurityConfig.java | 33 |
| Result.java | 33 |
| DashboardController.java | 21 |
| BugRepository.java | 20 |
| TestCaseRepository.java | 19 |
| CorsConfig.java | 18 |
| BusinessException.java | 17 |
| UserRepository.java | 13 |
| DashboardStatDTO.java | 13 |
| TestPlatformApplication.java | 11 |

## 4. 第二阶段：API接口测试详情表格

| 用例ID | 名称 | 预期状态 | 实际状态 |
| --- | --- | --- | --- |
| TC-001 | 登录成功 | 200 | PASSED |
| TC-002 | 错误密码 | 401 | PASSED |
| TC-003 | 无Token访问 | 403 | PASSED |
| TC-004 | 获取测试用例列表 | 200 | FAILED (500) |
| TC-005 | 创建测试用例 | 200 | FAILED (500) |
| TC-006 | 获取Bug列表 | 200 | PASSED |
| TC-007 | 创建Bug | 200 | PASSED |
| TC-008 | Dashboard统计 | 200 | PASSED |
| TC-009 | 分页获取测试用例 | 200 | FAILED (500) |
| TC-010 | 删除测试用例 | 200 | SKIPPED |

## 5. 第三阶段：数据库验证结果

| 表名 | 记录数 |
| --- | --- |
| audit_log | 0 |
| automation_scripts | 0 |
| bugs | 1 |
| projects | 1 |
| sqlite_sequence | 3 |
| test_cases | 0 |
| test_executions | 0 |
| users | 2 |

## 6. 问题清单

1. **TC-004 获取测试用例列表 FAILED**
   - 原因：返回 500 Internal Server Error，预期应为 200。
2. **TC-005 创建测试用例 FAILED**
   - 原因：返回 500 Internal Server Error，预期应为 200。
3. **TC-009 分页获取测试用例 FAILED**
   - 原因：返回 500 Internal Server Error，预期应为 200。

这些失败都集中在 TestCase 相关的 API 上，表明测试用例管理模块存在内部服务器错误（可能是 SQL 异常、空指针等），需要进一步排查后端日志。

## 7. 测试结论

本次 API 测试总共执行 10 个用例，其中 6 个通过，3 个失败，1 个跳过。整体通过率为 60%。认证、Bug管理以及 Dashboard 统计功能均正常工作。但是，所有与 测试用例 (TestCase) 管理相关的 API 均返回了 500 内部错误，导致相关用例失败，数据库中也没有生成任何测试用例数据。这属于严重缺陷，建议优先修复 TestCase 模块的问题。