package com.testplatform.repository;

import com.testplatform.entity.Bug;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BugRepository extends JpaRepository<Bug, Long> {
    List<Bug> findByStatus(String status);
    List<Bug> findByAssignee(String assignee);
    List<Bug> findBySeverity(String severity);

    @Query("SELECT b FROM Bug b WHERE (:status IS NULL OR b.status = :status) AND (:assignee IS NULL OR b.assignee = :assignee)")
    Page<Bug> findByCondition(@Param("status") String status, @Param("assignee") String assignee, Pageable pageable);
}