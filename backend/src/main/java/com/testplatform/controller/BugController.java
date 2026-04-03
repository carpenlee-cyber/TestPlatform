package com.testplatform.controller;

import com.testplatform.common.Result;
import com.testplatform.entity.Bug;
import com.testplatform.service.BugService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bugs")
public class BugController {
    
    @Autowired
    private BugService bugService;
    
    @GetMapping
    public Result<List<Bug>> getAllBugs() {
        return Result.success(bugService.findAll());
    }

    @GetMapping("/page")
    public Result<Page<Bug>> getBugsPage(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String assignee) {
        return Result.success(bugService.findPage(PageRequest.of(current - 1, size), status, assignee));
    }
    
    @GetMapping("/{id}")
    public Result<Bug> getBugById(@PathVariable Long id) {
        return bugService.findById(id)
                .map(Result::success)
                .orElse(Result.error(404, "Bug not found"));
    }
    
    @PostMapping
    public Result<Bug> createBug(@RequestBody Bug bug) {
        return Result.success(bugService.save(bug));
    }
    
    @PutMapping("/{id}")
    public Result<Bug> updateBug(@PathVariable Long id, @RequestBody Bug bug) {
        return bugService.findById(id)
                .map(existing -> {
                    if (bug.getStatus() != null) {
                        existing.setStatus(bug.getStatus());
                    }
                    return Result.success(bugService.save(existing));
                })
                .orElse(Result.error(404, "Bug not found"));
    }
    
    @DeleteMapping("/{id}")
    public Result<Void> deleteBug(@PathVariable Long id) {
        return bugService.findById(id)
                .map(bug -> {
                    bugService.deleteById(id);
                    return Result.<Void>success();
                })
                .orElse(Result.error(404, "Bug not found"));
    }
    
    @GetMapping("/status/{status}")
    public Result<List<Bug>> getBugsByStatus(@PathVariable String status) {
        return Result.success(bugService.findByStatus(status));
    }
}