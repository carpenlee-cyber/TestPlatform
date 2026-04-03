package com.testplatform.repository;

import com.testplatform.entity.TestCase;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TestCaseRepository extends JpaRepository<TestCase, Long> {
    List<TestCase> findByStatus(String status);
    List<TestCase> findByAssignee(String assignee);

    @Query("SELECT t FROM TestCase t WHERE (:status IS NULL OR t.status = :status) AND (:assignee IS NULL OR t.assignee = :assignee)")
    Page<TestCase> findByCondition(@Param("status") String status, @Param("assignee") String assignee, Pageable pageable);
}