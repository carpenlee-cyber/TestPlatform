package com.testplatform.dto;

import lombok.Data;

import java.util.Map;

@Data
public class DashboardStatDTO {
    private long totalTestCases;
    private long totalBugs;
    private Map<String, Long> testCaseStatusCount;
    private Map<String, Long> bugStatusCount;
    private Map<String, Long> bugSeverityCount;
}