package com.testplatform.service;

import com.testplatform.entity.Bug;
import com.testplatform.repository.BugRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class BugService {
    
    @Autowired
    private BugRepository bugRepository;
    
    public List<Bug> findAll() {
        return bugRepository.findAll();
    }
    
    public Optional<Bug> findById(Long id) {
        return bugRepository.findById(id);
    }
    
    public Bug save(Bug bug) {
        return bugRepository.save(bug);
    }
    
    public void deleteById(Long id) {
        bugRepository.deleteById(id);
    }
    
    public List<Bug> findByStatus(String status) {
        return bugRepository.findByStatus(status);
    }
    
    public List<Bug> findByAssignee(String assignee) {
        return bugRepository.findByAssignee(assignee);
    }
}
