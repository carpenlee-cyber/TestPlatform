package com.testplatform.controller;

import com.testplatform.entity.TestCase;
import com.testplatform.service.TestCaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/test-cases")
@CrossOrigin(origins = "*")
public class TestCaseController {
    
    @Autowired
    private TestCaseService testCaseService;
    
    @GetMapping
    public List<TestCase> getAllTestCases() {
        return testCaseService.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<TestCase> getTestCaseById(@PathVariable Long id) {
        return testCaseService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public TestCase createTestCase(@RequestBody TestCase testCase) {
        return testCaseService.save(testCase);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<TestCase> updateTestCase(@PathVariable Long id, @RequestBody TestCase testCase) {
        return testCaseService.findById(id)
                .map(existing -> {
                    testCase.setId(id);
                    return ResponseEntity.ok(testCaseService.save(testCase));
                })
                .orElse(ResponseEntity.notFound().build());
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTestCase(@PathVariable Long id) {
        return testCaseService.findById(id)
                .map(testCase -> {
                    testCaseService.deleteById(id);
                    return ResponseEntity.ok().<Void>build();
                })
                .orElse(ResponseEntity.notFound().build());
    }
    
    @GetMapping("/status/{status}")
    public List<TestCase> getTestCasesByStatus(@PathVariable String status) {
        return testCaseService.findByStatus(status);
    }
}
