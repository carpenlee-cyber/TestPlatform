package com.testplatform.controller;

import com.testplatform.common.Result;
import com.testplatform.dto.DashboardStatDTO;
import com.testplatform.service.DashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    @Autowired
    private DashboardService dashboardService;

    @GetMapping("/stats")
    public Result<DashboardStatDTO> getStats() {
        return Result.success(dashboardService.getDashboardStats());
    }
}