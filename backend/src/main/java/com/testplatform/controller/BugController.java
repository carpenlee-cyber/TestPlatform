package com.testplatform.controller;

import com.testplatform.entity.Bug;
import com.testplatform.service.BugService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bugs")
@CrossOrigin(origins = "*")
public class BugController {
    
    @Autowired
    private BugService bugService;
    
    @GetMapping
    public List<Bug> getAllBugs() {
        return bugService.findAll();
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Bug> getBugById(@PathVariable Long id) {
        return bugService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public Bug createBug(@RequestBody Bug bug) {
        return bugService.save(bug);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Bug> updateBug(@PathVariable Long id, @RequestBody Bug bug) {
        return bugService.findById(id)
                .map(existing -> {
                    bug.setId(id);
                    return ResponseEntity.ok(bugService.save(bug));
                })
                .orElse(ResponseEntity.notFound().build());
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteBug(@PathVariable Long id) {
        return bugService.findById(id)
                .map(bug -> {
                    bugService.deleteById(id);
                    return ResponseEntity.ok().<Void>build();
                })
                .orElse(ResponseEntity.notFound().build());
    }
    