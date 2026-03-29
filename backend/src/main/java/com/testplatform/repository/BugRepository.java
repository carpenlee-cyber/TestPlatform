package com.testplatform.repository;

import com.testplatform.entity.Bug;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BugRepository extends JpaRepository<Bug, Long> {
    List<Bug> findByStatus(String status);
    List<Bug> findByAssignee(String assignee);
    List<Bug> findBySeverity(String severity);
}
