package com.testplatform.service;

import com.testplatform.dto.DashboardStatDTO;
import com.testplatform.entity.Bug;
import com.testplatform.entity.TestCase;
import com.testplatform.repository.BugRepository;
import com.testplatform.repository.TestCaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class DashboardService {

    @Autowired
    private TestCaseRepository testCaseRepository;

    @Autowired
    private BugRepository bugRepository;

    public DashboardStatDTO getDashboardStats() {
        DashboardStatDTO stats = new DashboardStatDTO();
        
        List<TestCase> allTestCases = testCaseRepository.findAll();
        List<Bug> allBugs = bugRepository.findAll();

        stats.setTotalTestCases(allTestCases.size());
        stats.setTotalBugs(allBugs.size());

        Map<String, Long> testCaseStatusCount = allTestCases.stream()
                .filter(tc -> tc.getStatus() != null)
                .collect(Collectors.groupingBy(TestCase::getStatus, Collectors.counting()));
        stats.setTestCaseStatusCount(testCaseStatusCount);

        Map<String, Long> bugStatusCount = allBugs.stream()
                .filter(bug -> bug.getStatus() != null)
                .collect(Collectors.groupingBy(Bug::getStatus, Collectors.counting()));
        stats.setBugStatusCount(bugStatusCount);

        Map<String, Long> bugSeverityCount = allBugs.stream()
                .filter(bug -> bug.getSeverity() != null)
                .collect(Collectors.groupingBy(Bug::getSeverity, Collectors.counting()));
        stats.setBugSeverityCount(bugSeverityCount);

        return stats;
    }
}