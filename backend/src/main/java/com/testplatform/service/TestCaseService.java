package com.testplatform.service;

import com.testplatform.entity.TestCase;
import com.testplatform.repository.TestCaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class TestCaseService {
    
    @Autowired
    private TestCaseRepository testCaseRepository;
    
    public List<TestCase> findAll() {
        return testCaseRepository.findAll();
    }
    
    public Optional<TestCase> findById(Long id) {
        return testCaseRepository.findById(id);
    }
    
    public TestCase save(TestCase testCase) {
        return testCaseRepository.save(testCase);
    }
    
    public void deleteById(Long id) {
        testCaseRepository.deleteById(id);
    }
    
    public List<TestCase> findByStatus(String status) {
        return testCaseRepository.findByStatus(status);
    }
    
    public List<TestCase> findByAssignee(String assignee) {
        return testCaseRepository.findByAssignee(assignee);
    }
}
