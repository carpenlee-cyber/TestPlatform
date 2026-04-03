package com.testplatform.controller;

import com.testplatform.common.Result;
import com.testplatform.entity.TestCase;
import com.testplatform.service.TestCaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/testcases")
public class TestCaseController {
    
    @Autowired
    private TestCaseService testCaseService;
    
    @GetMapping
    public Result<List<TestCase>> getAllTestCases() {
        return Result.success(testCaseService.findAll());
    }

    @GetMapping("/page")
    public Result<Page<TestCase>> getTestCasesPage(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String assignee) {
        return Result.success(testCaseService.findPage(PageRequest.of(current - 1, size), status, assignee));
    }
    
    @GetMapping("/{id}")
    public Result<TestCase> getTestCaseById(@PathVariable Long id) {
        return testCaseService.findById(id)
                .map(Result::success)
                .orElse(Result.error(404, "Test case not found"));
    }
    
    @PostMapping
    public Result<TestCase> createTestCase(@RequestBody TestCase testCase) {
        return Result.success(testCaseService.save(testCase));
    }
    
    @PutMapping("/{id}")
    public Result<TestCase> updateTestCase(@PathVariable Long id, @RequestBody TestCase testCase) {
        return testCaseService.findById(id)
                .map(existing -> {
                    testCase.setId(id);
                    return Result.success(testCaseService.save(testCase));
                })
                .orElse(Result.error(404, "Test case not found"));
    }
    
    @DeleteMapping("/{id}")
    public Result<Void> deleteTestCase(@PathVariable Long id) {
        return testCaseService.findById(id)
                .map(testCase -> {
                    testCaseService.deleteById(id);
                    return Result.<Void>success();
                })
                .orElse(Result.error(404, "Test case not found"));
    }
    
    @GetMapping("/status/{status}")
    public Result<List<TestCase>> getTestCasesByStatus(@PathVariable String status) {
        return Result.success(testCaseService.findByStatus(status));
    }
}